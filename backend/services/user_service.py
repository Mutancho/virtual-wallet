import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from database.database_queries import read_query,update_query,insert_query
from schemas.user_models import RegisterUser
from utils.passwords import hash_password
from datetime import datetime,date

async def create(user:RegisterUser) -> RegisterUser:
    hashed = await hash_password(user.password)
    # user.date_of_birth = datetime.strptime(user.date_of_birth,'%d.%M.%Y')

    generate_id = await insert_query('''INSERT INTO users(username,password) VALUES (%s,%s)''',
                                     (user.username, hashed))
    await insert_query('''
    INSERT INTO user_details(title, first_name, last_name, gender, dob, address, email, phone_number, photo_selfie, identity_document, user_id)
    VALUES (%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)''',
    (user.title,user.first_name,user.last_name,user.gender,user.date_of_birth,user.address,user.email,user.phone_number,user.photo_selfie,user.identity_document,generate_id))

    user.id = generate_id
    subject = "Virtual Wallet Account Confirmation"
    confirmation_link = f'http://127.0.0.1:8000/users/confirmation/{generate_id}'
    message = f"Please click the link below to confirm your email address:\n\n{confirmation_link}"

    await send_email(user.email,confirmation_link,subject,message)

    return user

async def confirm(id):

    await update_query('''UPDATE users set email_verified = 1 where id = %s''',(id,))

    return 'Verified'





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



