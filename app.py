import logging
import os
from flask import Flask, render_template, request, redirect, url_for, flash, jsonify, make_response, abort
from flask_sqlalchemy import SQLAlchemy
from flask_wtf.csrf import CSRFProtect
from flask_mail import Mail
from flask_migrate import Migrate
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

# Email configuration
app.config['MAIL_SERVER'] = os.environ.get('MAIL_SERVER', 'smtp.gmail.com')
app.config['MAIL_PORT'] = int(os.environ.get('MAIL_PORT', 465))
app.config['MAIL_USE_TLS'] = os.environ.get('MAIL_USE_TLS', 'False').lower() == 'true'
app.config['MAIL_USE_SSL'] = os.environ.get('MAIL_USE_SSL', 'True').lower() == 'true'
app.config['MAIL_USERNAME'] = os.environ.get('MAIL_USERNAME')
app.config['MAIL_PASSWORD'] = os.environ.get('MAIL_PASSWORD')
app.config['MAIL_DEFAULT_SENDER'] = os.environ.get('MAIL_DEFAULT_SENDER')

# Initialize extensions
db = SQLAlchemy(app)
csrf = CSRFProtect(app)
mail = Mail(app)

# Initialize Flask-Migrate
migrate = Migrate(app, db)

# Import models after db is defined
from models import Event, HealthDeclaration

# Import and register blueprints
from events import events as events_blueprint
app.register_blueprint(events_blueprint, url_prefix='/events')

# Routes
@app.route('/')
def home():
    return redirect(url_for('events.event_list'))

@app.route('/health_declaration/<event_id>', methods=['GET', 'POST'])
def health_declaration(event_id):
    # Placeholder for health_declaration route
    pass

@app.route('/thank_you/<event_id>')
def thank_you(event_id):
    # Placeholder for thank_you route
    pass

@app.route('/dashboard/<event_id>')
def dashboard(event_id):
    try:
        event = Event.query.get_or_404(int(event_id))
    except ValueError:
        abort(404)  # If event_id is not a valid integer, return a 404 error
    
    declarations = HealthDeclaration.query.filter_by(event_id=event.id).all()
    total_declarations = len(declarations)
    flagged_declarations = sum(1 for d in declarations if d.flagged)
    checked_declarations = sum(1 for d in declarations if d.instructor_checked)
    current_year = datetime.now().year
    
    return render_template('dashboard.html', 
                           event=event, 
                           declarations=declarations, 
                           total_declarations=total_declarations,
                           flagged_declarations=flagged_declarations,
                           checked_declarations=checked_declarations,
                           current_year=current_year)

@app.route('/toggle_checked/<int:declaration_id>', methods=['POST'])
def toggle_checked(declaration_id):
    # Placeholder for toggle_checked route
    pass

@app.route('/export/<event_id>')
def export_data(event_id):
    # Placeholder for export_data route
    pass

@app.route('/mark_event_done/<int:event_id>', methods=['POST'])
def mark_event_done(event_id):
    event = Event.query.get_or_404(event_id)
    event.is_done = True
    try:
        db.session.commit()
        return jsonify({'success': True, 'message': 'Event marked as finished'})
    except Exception as e:
        db.session.rollback()
        app.logger.error(f"Error marking event as done: {str(e)}")
        return jsonify({'success': False, 'message': 'An error occurred while marking the event as finished'}), 500

@app.errorhandler(404)
def not_found_error(error):
    return render_template('404.html'), 404

@app.errorhandler(500)
def internal_error(error):
    db.session.rollback()
    app.logger.error(f"Internal Server Error: {str(error)}")
    return render_template('500.html'), 500

# Logging configuration
if not app.debug:
    file_handler = logging.FileHandler('app.log')
    file_handler.setLevel(logging.INFO)
    app.logger.addHandler(file_handler)
    app.logger.setLevel(logging.INFO)
    app.logger.info('Application startup')
else:
    logging.basicConfig(level=logging.DEBUG)

if __name__ == '__main__':
    with app.app_context():
        db.create_all()
    app.run(debug=True)