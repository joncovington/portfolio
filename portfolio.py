import os
import requests
from dotenv import load_dotenv
from flask import Flask, json, render_template, request, flash, jsonify
from flask_mail import Mail, Message
from flask_wtf.csrf import CSRFProtect
from flask_recaptcha import ReCaptcha


load_dotenv()

app = Flask(__name__)
mail = Mail(app) # instantiate the mail class
csrf = CSRFProtect(app) # instantiate CSRF protection
recaptcha = ReCaptcha()

app.config['SECRET_KEY'] = os.getenv('SECRET_KEY')

# configuration of mail
app.config['MAIL_SERVER'] = os.getenv('SMTP_SERVER')
app.config['MAIL_PORT'] = os.getenv('SMTP_PORT')
app.config['MAIL_USERNAME'] = os.getenv('SMTP_USERNAME')
app.config['MAIL_PASSWORD'] = os.getenv('SMTP_PASSWORD')
app.config['MAIL_USE_TLS'] = False
app.config['MAIL_USE_SSL'] = True
mail = Mail(app)
csrf.init_app(app)
recaptcha.init_app(app)


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
            msg = Message(
                    f'A portfolio msg from {form_data["name"]} <{form_data["email"]}>',
                    sender = os.getenv('SMTP_FROM'),
                    recipients = [os.getenv('SMTP_TO'), ]
                )
            msg.body = form_data["message"]
            mail.send(msg)
            success_data = {}
            success_data['message'] = 'Thank you for contacting me. I look forward to getting in touch with you!'
            success_data['success'] = True
            return jsonify(**success_data), 200, {'ContentType':'application/json'}
    return jsonify({'error': 'Something went wrong'}), 400, {'ContentType':'application/json'}


if __name__ == "__main__":
    app.run(host='0.0.0.0')
