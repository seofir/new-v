from flask import Blueprint, render_template, request, redirect, url_for, flash, current_app
from models import Event, db
from flask_wtf import FlaskForm
from wtforms import StringField, DateField, IntegerField, SubmitField
from wtforms.validators import DataRequired, Optional
import uuid

events = Blueprint('events', __name__)

class EventForm(FlaskForm):
    name = StringField('שם האירוע', validators=[DataRequired()])
    date = DateField('תאריך', validators=[Optional()])
    expected_participants = IntegerField('משתתפים צפויים', validators=[Optional()])
    contact_name = StringField('שם איש קשר', validators=[Optional()])
    contact_number = StringField('מספר טלפון של איש קשר', validators=[Optional()])
    submit = SubmitField('צור אירוע')

@events.route('/create_event', methods=['GET', 'POST'])
def create_event():
    form = EventForm()
    if form.validate_on_submit():
        try:
            new_event = Event(
                name=form.name.data,
                date=form.date.data,
                expected_participants=form.expected_participants.data,
                unique_id=str(uuid.uuid4())[:8],
                contact_name=form.contact_name.data,
                contact_number=form.contact_number.data
            )
            db.session.add(new_event)
            db.session.commit()
            flash('האירוע נוצר בהצלחה!', 'success')
            return redirect(url_for('events.event_list'))
        except Exception as e:
            db.session.rollback()
            current_app.logger.error(f"Error creating event: {str(e)}")
            flash('An error occurred while creating the event. Please try again.', 'error')
    return render_template('create_event.html', form=form)

@events.route('/event_list')
def event_list():
    ongoing_events = Event.query.filter_by(is_done=False).all()
    finished_events = Event.query.filter_by(is_done=True).all()
    return render_template('event_list.html', ongoing_events=ongoing_events, finished_events=finished_events)

@events.route('/event_details/<int:event_id>')
def event_details(event_id):
    event = Event.query.get_or_404(event_id)
    return render_template('event_details.html', event=event)

@events.route('/edit_event/<int:event_id>', methods=['GET', 'POST'])
def edit_event(event_id):
    event = Event.query.get_or_404(event_id)
    form = EventForm(obj=event)

    if form.validate_on_submit():
        form.populate_obj(event)
        try:
            db.session.commit()
            flash('האירוע עודכן בהצלחה!', 'success')
            return redirect(url_for('events.event_details', event_id=event.id))
        except Exception as e:
            db.session.rollback()
            current_app.logger.error(f"Error updating event: {str(e)}")
            flash('An error occurred while updating the event. Please try again.', 'error')

    return render_template('edit_event.html', form=form, event=event)

@events.route('/delete_event/<int:event_id>', methods=['POST'])
def delete_event(event_id):
    event = Event.query.get_or_404(event_id)
    try:
        db.session.delete(event)
        db.session.commit()
        flash('האירוע נמחק בהצלחה!', 'success')
    except Exception as e:
        db.session.rollback()
        current_app.logger.error(f"Error deleting event: {str(e)}")
        flash('An error occurred while deleting the event. Please try again.', 'error')
    return redirect(url_for('events.event_list'))