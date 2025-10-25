from flask_sqlalchemy import SQLAlchemy
from datetime import datetime

db = SQLAlchemy()

class Host(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(128), nullable=False)
    progress = db.Column(db.Integer, default=0)
    profile_last_updated = db.Column(db.DateTime, default=datetime.utcnow)

    def __repr__(self):
        return f"<Host {self.name}>"


class Contestant(db.Model):
    """Represents a contestant in the singing competition."""
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(128), nullable=False)
    performance_number = db.Column(db.Integer, unique=True, nullable=False)
    song_title = db.Column(db.String(256))
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

    # Relationship to scores
    scores = db.relationship('Score', backref='contestant', lazy=True, cascade='all, delete-orphan')

    def to_dict(self):
        return {
            'id': self.id,
            'name': self.name,
            'performance_number': self.performance_number,
            'song_title': self.song_title,
            'created_at': self.created_at.isoformat() if self.created_at else None
        }

    def __repr__(self):
        return f"<Contestant {self.name} #{self.performance_number}>"


class Judge(db.Model):
    """Represents a judge in the singing competition."""
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(128), nullable=False, unique=True)
    credentials = db.Column(db.String(256))
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

    # Relationship to scores
    scores = db.relationship('Score', backref='judge', lazy=True, cascade='all, delete-orphan')

    def to_dict(self):
        return {
            'id': self.id,
            'name': self.name,
            'credentials': self.credentials,
            'created_at': self.created_at.isoformat() if self.created_at else None
        }

    def __repr__(self):
        return f"<Judge {self.name}>"


class Score(db.Model):
    """Represents a score given by a judge to a contestant."""
    id = db.Column(db.Integer, primary_key=True)
    contestant_id = db.Column(db.Integer, db.ForeignKey('contestant.id'), nullable=False)
    judge_id = db.Column(db.Integer, db.ForeignKey('judge.id'), nullable=False)

    # Score categories (out of 10 each)
    vocals = db.Column(db.Float, nullable=False)  # Vocal ability, pitch, tone
    stage_presence = db.Column(db.Float, nullable=False)  # Performance, charisma
    song_choice = db.Column(db.Float, nullable=False)  # Song selection appropriateness
    overall = db.Column(db.Float, nullable=False)  # Overall impression

    # Optional notes from judge
    notes = db.Column(db.Text)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

    # Unique constraint: one score per judge per contestant
    __table_args__ = (db.UniqueConstraint('contestant_id', 'judge_id', name='_contestant_judge_uc'),)

    def total_score(self):
        """Calculate total score (out of 40)."""
        return self.vocals + self.stage_presence + self.song_choice + self.overall

    def average_score(self):
        """Calculate average score (out of 10)."""
        return self.total_score() / 4

    def to_dict(self):
        return {
            'id': self.id,
            'contestant_id': self.contestant_id,
            'contestant_name': self.contestant.name if self.contestant else None,
            'judge_id': self.judge_id,
            'judge_name': self.judge.name if self.judge else None,
            'vocals': self.vocals,
            'stage_presence': self.stage_presence,
            'song_choice': self.song_choice,
            'overall': self.overall,
            'total_score': self.total_score(),
            'average_score': self.average_score(),
            'notes': self.notes,
            'created_at': self.created_at.isoformat() if self.created_at else None
        }

    def __repr__(self):
        return f"<Score Judge:{self.judge_id} Contestant:{self.contestant_id} Total:{self.total_score()}>"
