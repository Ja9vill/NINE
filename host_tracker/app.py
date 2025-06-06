from datetime import datetime
from flask import Flask, request, jsonify, render_template
from apscheduler.schedulers.background import BackgroundScheduler

from .models import db, Host

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///hosts.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db.init_app(app)


@app.before_first_request
def create_tables():
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


@app.route('/progress_form')
def progress_form():
    hosts = Host.query.all()
    return render_template('progress_form.html', hosts=hosts)


if __name__ == '__main__':
    app.run(debug=True)
