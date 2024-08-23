import os
from flask import Flask, render_template, request, redirect, url_for, flash, jsonify, abort
from flask_sqlalchemy import SQLAlchemy
from flask_wtf.csrf import CSRFProtect
from datetime import datetime

app = Flask(__name__)

# Configuration
app.config['SECRET_KEY'] = os.environ.get('SECRET_KEY', 'your_secret_key_here')
app.config['WTF_CSRF_SECRET_KEY'] = os.environ.get('WTF_CSRF_SECRET_KEY', 'your_csrf_secret_key')
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

# Database configuration
database_url = os.environ.get('DATABASE_URL')
if database_url:
    if database_url.startswith("postgres://"):
        database_url = database_url.replace("postgres://", "postgresql://", 1)
    app.config['SQLALCHEMY_DATABASE_URI'] = database_url
else:
    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///events.db'

# Initialize extensions
db = SQLAlchemy(app)
csrf = CSRFProtect(app)

# Import models after db is defined
from models import Event, HealthDeclaration

# Routes
@app.route('/')
def home():
    events = Event.query.all()
    return render_template('event_list.html', events=events)

@app.route('/health_declaration/<event_id>', methods=['GET', 'POST'])
def health_declaration(event_id):
    event = Event.query.get_or_404(event_id)
    if request.method == 'POST':
        # Process the health declaration form
        declaration = HealthDeclaration(
            event_id=event.id,
            name=request.form['name'],
            email=request.form['email'],
            phone=request.form['phone'],
            # Add other fields as necessary
        )
        db.session.add(declaration)
        db.session.commit()
        return redirect(url_for('thank_you', event_id=event_id))
    return render_template('health_declaration.html', event=event)

@app.route('/thank_you/<event_id>')
def thank_you(event_id):
    event = Event.query.get_or_404(event_id)
    return render_template('thank_you.html', event=event)

@app.route('/dashboard/<event_id>')
def dashboard(event_id):
    event = Event.query.get_or_404(int(event_id))
    declarations = HealthDeclaration.query.filter_by(event_id=event.id).all()
    total_declarations = len(declarations)
    current_year = datetime.now().year
    
    return render_template('dashboard.html', 
                           event=event, 
                           declarations=declarations, 
                           total_declarations=total_declarations,
                           current_year=current_year)

@app.errorhandler(404)
def not_found_error(error):
    return render_template('404.html'), 404

@app.errorhandler(500)
def internal_error(error):
    db.session.rollback()
    return render_template('500.html'), 500

@app.before_first_request
def create_tables():
    db.create_all()

if __name__ == '__main__':
    app.run(debug=True)