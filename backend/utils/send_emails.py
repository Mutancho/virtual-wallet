import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
async def send_email(recipient_email,confirmation_link = None ,subject=None, message = None ):
    sender_email = "virtual.wallet.team1@gmail.com"
    sender_password = "nowqjgrjcgbnhuvu"

    msg = MIMEText(message)

    msg["From"] = sender_email
    msg["To"] = recipient_email
    msg["Subject"] = subject

    try:
        # Create a secure connection with the SMTP server

        server = smtplib.SMTP_SSL("smtp.gmail.com", 465)
        server.ehlo()

        # Login to the sender's email account
        server.login(sender_email, sender_password)

        # Send the email
        server.sendmail(sender_email, recipient_email, msg.as_string())
        print("Confirmation email sent successfully!")

        # Close the connection
        server.close()
    except Exception as e:
        print("Failed to send confirmation email.")
        print(e)