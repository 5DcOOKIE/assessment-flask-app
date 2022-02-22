from click import command, echo
from flask_sqlalchemy import SQLAlchemy
from flask.cli import with_appcontext
from datetime import datetime

db = SQLAlchemy()


class User(db.Model):
    """A blog post."""
    id: int
    name: str
    email: str
    password: str
    created: datetime

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.Text, nullable=True)
    email = db.Column(db.Text, nullable=False)
    password = db.Column(db.Text, nullable=False)
    created = db.Column(db.DateTime, default=datetime.utcnow)


@command("init-db")
@with_appcontext
def init_db_command():
    """Initialize the database."""
    db.create_all()
    echo("Initialized the database.")


def init_app(app):
    """Initialize the Flask app for database usage."""
    db.init_app(app)
    app.cli.add_command(init_db_command)
