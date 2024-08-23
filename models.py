from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

class Event(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    date = db.Column(db.Date, nullable=True)
    expected_participants = db.Column(db.Integer, nullable=True)
    unique_id = db.Column(db.String(8), unique=True, nullable=False)
    contact_name = db.Column(db.String(100), nullable=True)
    contact_number = db.Column(db.String(20), nullable=True)
    is_done = db.Column(db.Boolean, default=False)
    # Remove the created_at field if it's not in your database
    # created_at = db.Column(db.DateTime, default=datetime.utcnow)

class HealthDeclaration(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    event_id = db.Column(db.String(8), db.ForeignKey('event.unique_id'), nullable=False)
    full_name = db.Column(db.String(100), nullable=False)
    phone_number = db.Column(db.String(20), nullable=False)
    year_of_birth = db.Column(db.Integer, nullable=False)
    symptoms = db.Column(db.String(200))
    autoimmune_disease = db.Column(db.String(100))
    other_medical_condition = db.Column(db.String(100))
    medication = db.Column(db.String(3), nullable=False)
    allergies = db.Column(db.String(100))
    pregnant = db.Column(db.String(3), nullable=False)
    additional_info = db.Column(db.Text)
    flagged = db.Column(db.Boolean, default=False)
    instructor_checked = db.Column(db.Boolean, default=False)
    # Remove the created_at field if it's not in your database
    # created_at = db.Column(db.DateTime, default=datetime.utcnow)

    event = db.relationship('Event', backref=db.backref('health_declarations', lazy=True))