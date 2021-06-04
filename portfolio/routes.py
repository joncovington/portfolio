import os
import requests
from flask import request, flash, render_template, jsonify, make_response
from flask import current_app as app
from flask_mail import Message
from mailjet_rest import Client
from portfolio.models import db, Contact
from portfolio import mail

API_KEY = os.getenv('MJ_API_KEY')
API_SECRET = os.getenv('MJ_SECRET_KEY')

mailjet = Client(auth=(API_KEY, API_SECRET), version='v3.1')


@app.route('/', methods=['GET', 'POST'])
def portfolio():
    if request.method == 'POST':
        context = {}
        if (request.form['Email']) and (request.form['Name']):
            msg = Message(
                f'A portfolio msg from {request.form["Name"]} <{request.form["Email"]}>',
                sender = os.getenv('SMTP_FROM'),
                recipients = [os.getenv('SMTP_TO'), ]
               )
            msg.body = request.form['Message']
            mail.send(msg)
            flash('Thank you for contacting me. I look forward to getting in touch with you!', 'message')
            context['load_modal'] = True
            return render_template("index.html", **context)
    return render_template("./index.html")


@app.route('/_send_mail', methods=['POST'])
def send_mail():
    form_data = request.get_json()
    google_data = {
        'secret': os.getenv('G_SECRET_KEY'),
        'response': form_data['token'],
    }
    resp = requests.post(
        'https://www.google.com/recaptcha/api/siteverify',
        data=google_data
    )
    print(resp.json())
    if resp.json()['success']:
        if form_data:
            data = {
                'Messages': [
                    {
                        "From": {
                            "Email": os.getenv('SMTP_FROM'),
                            "Name": "Portfolio"
                        },
                        "To": [
                            {
                            "Email": os.getenv('SMTP_TO'),
                            "Name": "You"
                            }
                        ],
                        "Subject": f'A portfolio msg from {form_data["name"]} <{form_data["email"]}>',
                        "TextPart": form_data["message"],
                        "HTMLPart": f'<p>{form_data["message"]}</p>'
                    }
                ]
            }
            result = mailjet.send.create(data=data)
            
            new_user = Contact(name=form_data["name"],
                email=form_data["email"],
                comment=form_data["message"],
                )
            db.session.add(new_user)
            db.session.commit()
            success_data = {}
            success_data['message'] = 'Thank you for contacting me. I look forward to getting in touch with you!'
            success_data['success'] = True
            return jsonify(**success_data), 200, {'ContentType':'application/json'}
    return jsonify({'error': 'Something went wrong'}), 400, {'ContentType':'application/json'}

@app.route('/test', methods=['GET'])
def entry():
    """Endpoint to create a user."""
    new_user = Contact(name='test',
                    email='myuser@example.com',
                    comment="In West Philadelphia born and raised, on the playground is where I spent most of my days",
                    )
    db.session.add(new_user)
    db.session.commit()
    return make_response("User created!")