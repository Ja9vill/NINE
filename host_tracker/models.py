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
