from datetime import datetime
from flask import Flask, request, jsonify, render_template
from apscheduler.schedulers.background import BackgroundScheduler
from sqlalchemy import func

from .models import db, Host, Contestant, Judge, Score

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


# ============================================================================
# SINGING COMPETITION SCORING SYSTEM ENDPOINTS
# ============================================================================

# -------------------- CONTESTANT ENDPOINTS --------------------

@app.route('/contestants', methods=['POST'])
def create_contestant():
    """Create a new contestant."""
    data = request.get_json()

    # Validation
    if not data or 'name' not in data or 'performance_number' not in data:
        return jsonify({'error': 'name and performance_number are required'}), 400

    # Check if performance number already exists
    existing = Contestant.query.filter_by(performance_number=data['performance_number']).first()
    if existing:
        return jsonify({'error': f'Performance number {data["performance_number"]} already exists'}), 400

    contestant = Contestant(
        name=data['name'],
        performance_number=data['performance_number'],
        song_title=data.get('song_title')
    )

    db.session.add(contestant)
    db.session.commit()

    return jsonify(contestant.to_dict()), 201


@app.route('/contestants', methods=['GET'])
def list_contestants():
    """List all contestants."""
    contestants = Contestant.query.order_by(Contestant.performance_number).all()
    return jsonify([c.to_dict() for c in contestants])


@app.route('/contestants/<int:id>', methods=['GET'])
def get_contestant(id):
    """Get a specific contestant with their scores."""
    contestant = Contestant.query.get_or_404(id)
    result = contestant.to_dict()

    # Include all scores for this contestant
    scores = Score.query.filter_by(contestant_id=id).all()
    result['scores'] = [s.to_dict() for s in scores]

    # Calculate average scores across all judges
    if scores:
        result['average_vocals'] = sum(s.vocals for s in scores) / len(scores)
        result['average_stage_presence'] = sum(s.stage_presence for s in scores) / len(scores)
        result['average_song_choice'] = sum(s.song_choice for s in scores) / len(scores)
        result['average_overall'] = sum(s.overall for s in scores) / len(scores)
        result['average_total'] = sum(s.total_score() for s in scores) / len(scores)

    return jsonify(result)


@app.route('/contestants/<int:id>', methods=['DELETE'])
def delete_contestant(id):
    """Delete a contestant."""
    contestant = Contestant.query.get_or_404(id)
    db.session.delete(contestant)
    db.session.commit()
    return jsonify({'message': 'Contestant deleted successfully'}), 200


# -------------------- JUDGE ENDPOINTS --------------------

@app.route('/judges', methods=['POST'])
def create_judge():
    """Create a new judge."""
    data = request.get_json()

    # Validation
    if not data or 'name' not in data:
        return jsonify({'error': 'name is required'}), 400

    # Check if judge name already exists
    existing = Judge.query.filter_by(name=data['name']).first()
    if existing:
        return jsonify({'error': f'Judge with name {data["name"]} already exists'}), 400

    judge = Judge(
        name=data['name'],
        credentials=data.get('credentials')
    )

    db.session.add(judge)
    db.session.commit()

    return jsonify(judge.to_dict()), 201


@app.route('/judges', methods=['GET'])
def list_judges():
    """List all judges."""
    judges = Judge.query.all()
    return jsonify([j.to_dict() for j in judges])


@app.route('/judges/<int:id>', methods=['GET'])
def get_judge(id):
    """Get a specific judge with their scores."""
    judge = Judge.query.get_or_404(id)
    result = judge.to_dict()

    # Include all scores by this judge
    scores = Score.query.filter_by(judge_id=id).all()
    result['scores'] = [s.to_dict() for s in scores]

    return jsonify(result)


@app.route('/judges/<int:id>', methods=['DELETE'])
def delete_judge(id):
    """Delete a judge."""
    judge = Judge.query.get_or_404(id)
    db.session.delete(judge)
    db.session.commit()
    return jsonify({'message': 'Judge deleted successfully'}), 200


# -------------------- SCORE ENDPOINTS --------------------

@app.route('/scores', methods=['POST'])
def submit_score():
    """Submit a score from a judge for a contestant."""
    data = request.get_json()

    # Validation
    required_fields = ['contestant_id', 'judge_id', 'vocals', 'stage_presence', 'song_choice', 'overall']
    missing_fields = [f for f in required_fields if f not in data]
    if missing_fields:
        return jsonify({'error': f'Missing required fields: {", ".join(missing_fields)}'}), 400

    # Validate contestant and judge exist
    contestant = Contestant.query.get(data['contestant_id'])
    if not contestant:
        return jsonify({'error': f'Contestant with id {data["contestant_id"]} not found'}), 404

    judge = Judge.query.get(data['judge_id'])
    if not judge:
        return jsonify({'error': f'Judge with id {data["judge_id"]} not found'}), 404

    # Validate score ranges (0-10)
    score_fields = ['vocals', 'stage_presence', 'song_choice', 'overall']
    for field in score_fields:
        try:
            value = float(data[field])
            if value < 0 or value > 10:
                return jsonify({'error': f'{field} must be between 0 and 10'}), 400
        except (ValueError, TypeError):
            return jsonify({'error': f'{field} must be a valid number'}), 400

    # Check if score already exists for this judge-contestant pair
    existing_score = Score.query.filter_by(
        contestant_id=data['contestant_id'],
        judge_id=data['judge_id']
    ).first()

    if existing_score:
        # Update existing score
        existing_score.vocals = float(data['vocals'])
        existing_score.stage_presence = float(data['stage_presence'])
        existing_score.song_choice = float(data['song_choice'])
        existing_score.overall = float(data['overall'])
        existing_score.notes = data.get('notes')
        db.session.commit()
        return jsonify(existing_score.to_dict()), 200
    else:
        # Create new score
        score = Score(
            contestant_id=data['contestant_id'],
            judge_id=data['judge_id'],
            vocals=float(data['vocals']),
            stage_presence=float(data['stage_presence']),
            song_choice=float(data['song_choice']),
            overall=float(data['overall']),
            notes=data.get('notes')
        )

        db.session.add(score)
        db.session.commit()

        return jsonify(score.to_dict()), 201


@app.route('/scores', methods=['GET'])
def list_scores():
    """List all scores with optional filtering."""
    contestant_id = request.args.get('contestant_id', type=int)
    judge_id = request.args.get('judge_id', type=int)

    query = Score.query

    if contestant_id:
        query = query.filter_by(contestant_id=contestant_id)

    if judge_id:
        query = query.filter_by(judge_id=judge_id)

    scores = query.all()
    return jsonify([s.to_dict() for s in scores])


@app.route('/scores/<int:id>', methods=['GET'])
def get_score(id):
    """Get a specific score."""
    score = Score.query.get_or_404(id)
    return jsonify(score.to_dict())


@app.route('/scores/<int:id>', methods=['DELETE'])
def delete_score(id):
    """Delete a score."""
    score = Score.query.get_or_404(id)
    db.session.delete(score)
    db.session.commit()
    return jsonify({'message': 'Score deleted successfully'}), 200


# -------------------- LEADERBOARD ENDPOINT --------------------

@app.route('/leaderboard', methods=['GET'])
def get_leaderboard():
    """Get the competition leaderboard with rankings."""
    # Calculate average scores for each contestant
    leaderboard = []

    contestants = Contestant.query.all()

    for contestant in contestants:
        scores = Score.query.filter_by(contestant_id=contestant.id).all()

        if scores:
            avg_vocals = sum(s.vocals for s in scores) / len(scores)
            avg_stage_presence = sum(s.stage_presence for s in scores) / len(scores)
            avg_song_choice = sum(s.song_choice for s in scores) / len(scores)
            avg_overall = sum(s.overall for s in scores) / len(scores)
            avg_total = sum(s.total_score() for s in scores) / len(scores)

            leaderboard.append({
                'contestant_id': contestant.id,
                'name': contestant.name,
                'performance_number': contestant.performance_number,
                'song_title': contestant.song_title,
                'average_vocals': round(avg_vocals, 2),
                'average_stage_presence': round(avg_stage_presence, 2),
                'average_song_choice': round(avg_song_choice, 2),
                'average_overall': round(avg_overall, 2),
                'average_total': round(avg_total, 2),
                'number_of_judges': len(scores)
            })

    # Sort by average total score (descending)
    leaderboard.sort(key=lambda x: x['average_total'], reverse=True)

    # Add rankings
    for index, entry in enumerate(leaderboard, start=1):
        entry['rank'] = index

    return jsonify(leaderboard)


if __name__ == '__main__':
    app.run(debug=True)
