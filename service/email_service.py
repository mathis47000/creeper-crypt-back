import os
import smtplib, ssl
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart


def send_room_link(receiver_email, room_url):
    print("send_room_link")
    sender_email = os.environ["EMAIL"]
    receiver_email = receiver_email
    password = os.environ["EMAIL_PASSWORD"]


    message = MIMEMultipart("alternative")
    message["Subject"] = "Rejoindre une salle sur Creeper Crypt"
    message["From"] = sender_email
    message["To"] = receiver_email

    text = """\
    Bonjour,
    Vous recevez cet e-mail car vous avez été invité à rejoindre une salle.
    Vous pouvez rejoindre la salle en cliquant sur le lien suivant :
    {}
    
    Meilleures salutations,
    L'équipe Creeper
    """.format(room_url)

    # Turn these into plain/html MIMEText objects
    body = MIMEText(text, "plain")

    # Add HTML/plain-text parts to MIMEMultipart message
    # The email client will try to render the last part first
    message.attach(body)

    # Create secure connection with server and send email
    context = ssl.create_default_context()

    try:
        context = ssl.create_default_context()
        with smtplib.SMTP("smtp.gmail.com", 587) as server:
            server.ehlo()  # Can be omitted
            server.starttls(context=context)
            server.ehlo()  # Can be omitted
            server.login(sender_email, password)
            server.sendmail(sender_email, receiver_email, message.as_string())
    except Exception as e:
        print(e)
        return False