from flask_mail import Mail, Message

mail = Mail()

def send_email(subject, recipient, body):
    msg = Message(subject,
                  sender='your-email@example.com',
                  recipients=[recipient])
    msg.body = body
    mail.send(msg)

def send_flagged_response_alert(instructor_email, participant_name):
    subject = "Flagged Health Declaration"
    body = f"A flagged health declaration has been submitted by {participant_name}. Please review it on the dashboard."
    send_email(subject, instructor_email, body)