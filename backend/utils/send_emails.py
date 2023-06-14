import smtplib
from email.mime.text import MIMEText


async def send_email(recipient_email, confirmation_link=None, subject=None, message=None):
    sender_email = "virtual.wallet.team1@gmail.com"
    sender_password = "nowqjgrjcgbnhuvu"

    msg = MIMEText(message)

    msg["From"] = sender_email
    msg["To"] = recipient_email
    msg["Subject"] = subject

    try:
        server = smtplib.SMTP_SSL("smtp.gmail.com", 465)
        server.ehlo()

        server.login(sender_email, sender_password)

        server.sendmail(sender_email, recipient_email, msg.as_string())
        print("Confirmation email sent successfully!")

        server.close()

    except Exception as e:
        print("Failed to send confirmation email.")
        print(e)
