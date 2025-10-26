from datetime import datetime
import csv
import io
from flask import Flask, request, jsonify, render_template, make_response
from apscheduler.schedulers.background import BackgroundScheduler

from .models import db, Host

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///hosts.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db.init_app(app)

# Create tables on startup
with app.app_context():
    db.create_all()


def update_host_profiles():
    """Scheduled task to refresh host profile timestamps."""
    with app.app_context():
        hosts = Host.query.all()
        for host in hosts:
            host.profile_last_updated = datetime.utcnow()
        db.session.commit()


scheduler = BackgroundScheduler()
scheduler.add_job(update_host_profiles, 'interval', minutes=1)
scheduler.start()


@app.route('/hosts/<int:id>/progress', methods=['POST'])
def update_progress(id):
    """Update host progress and profile timestamp."""
    host = Host.query.get_or_404(id)
    data = request.get_json() or request.form
    if 'progress' not in data:
        return jsonify({'error': 'progress value required'}), 400
    host.progress = int(data['progress'])
    host.profile_last_updated = datetime.utcnow()
    db.session.commit()
    return jsonify({'status': 'updated', 'id': host.id, 'progress': host.progress})


@app.route('/hosts', methods=['GET'])
def list_hosts():
    hosts = Host.query.all()
    result = []
    for h in hosts:
        result.append({
            'id': h.id,
            'name': h.name,
            'progress': h.progress,
            'profile_last_updated': h.profile_last_updated.isoformat() if h.profile_last_updated else None
        })
    return jsonify(result)


@app.route('/')
def dashboard():
    """Main dashboard view."""
    hosts = Host.query.all()
    return render_template('dashboard.html', hosts=hosts)


@app.route('/progress_form')
def progress_form():
    """Legacy form view (kept for backward compatibility)."""
    hosts = Host.query.all()
    return render_template('progress_form.html', hosts=hosts)


@app.route('/hosts', methods=['POST'])
def create_host():
    """Create a new host."""
    data = request.get_json() or request.form
    if 'name' not in data:
        return jsonify({'error': 'name is required'}), 400

    # Check if host with same name already exists
    existing = Host.query.filter_by(name=data['name']).first()
    if existing:
        return jsonify({'error': 'Host with this name already exists'}), 400

    new_host = Host(
        name=data['name'],
        progress=int(data.get('progress', 0)),
        profile_last_updated=datetime.utcnow()
    )
    db.session.add(new_host)
    db.session.commit()

    return jsonify({
        'status': 'created',
        'id': new_host.id,
        'name': new_host.name,
        'progress': new_host.progress
    }), 201


@app.route('/hosts/<int:id>', methods=['DELETE'])
def delete_host(id):
    """Delete a host."""
    host = Host.query.get_or_404(id)
    db.session.delete(host)
    db.session.commit()
    return jsonify({'status': 'deleted', 'id': id})


@app.route('/export/csv')
def export_csv():
    """Export all hosts to CSV."""
    hosts = Host.query.all()

    # Create CSV in memory
    si = io.StringIO()
    writer = csv.writer(si)
    writer.writerow(['ID', 'Name', 'Progress', 'Last Updated'])

    for host in hosts:
        writer.writerow([
            host.id,
            host.name,
            host.progress,
            host.profile_last_updated.isoformat() if host.profile_last_updated else 'Never'
        ])

    output = make_response(si.getvalue())
    output.headers["Content-Disposition"] = "attachment; filename=hosts_export.csv"
    output.headers["Content-type"] = "text/csv"
    return output


@app.route('/export/json')
def export_json():
    """Export all hosts to JSON."""
    hosts = Host.query.all()
    result = []
    for h in hosts:
        result.append({
            'id': h.id,
            'name': h.name,
            'progress': h.progress,
            'profile_last_updated': h.profile_last_updated.isoformat() if h.profile_last_updated else None
        })

    response = make_response(jsonify(result))
    response.headers["Content-Disposition"] = "attachment; filename=hosts_export.json"
    return response


if __name__ == '__main__':
    app.run(debug=True)
