from database.database_queries import read_query,update_query,insert_query
from schemas.user_models import RegisterUser, EmailLogin, UsernameLogin, DisplayUser
from utils.passwords import hash_password, verify_password
from utils import oauth2
from utils.send_emails import send_email

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

async def login(credentials: EmailLogin | UsernameLogin):
    if isinstance(credentials, EmailLogin):
        data = await read_query('''SELECT user_id,email FROM user_details WHERE email = %s''',
                                (credentials.email,))
    if isinstance(credentials, UsernameLogin):
        data = await read_query('''SELECT id,username,password FROM users WHERE username = %s''',
                                (credentials.username,))
    id = data[0][0]


    return oauth2.create_access_token(id)


async def all(username,phone,email,limit,offset):

    sql = '''SELECT u.username,ud.email,ud.phone_number,ud.first_name,ud.last_name,ud.address FROM users as u join user_details as ud on u.id = ud.user_id'''

    where_clauses = []
    if username:
        where_clauses.append(f"LOCATE('{username}',u.username) > 0")
        # where_clauses.append(f"u.username like '%{username}%'")
    if email:
        where_clauses.append(f"LOCATE('{email}',ud.email) > 0")
        # where_clauses.append(f"ud.email like '%{email}%'")
    if phone:
        where_clauses.append(f"LOCATE('{phone}',ud.phone_number) > 0")
        # where_clauses.append(f"ud.phone_number like '%{phone}%'")
    if where_clauses:
        sql += ' WHERE ' + ' AND '.join(where_clauses)
    if limit:
        if offset:
            sql += f" limit {offset},{limit}"
        else:
            sql += f" limit {limit}"
    data = await read_query(sql)

    return (DisplayUser.from_query_result(*row) for row in data)








async def verify_credentials(credentials: EmailLogin | UsernameLogin):
    data = None
    if isinstance(credentials, EmailLogin):
        data = await read_query('''SELECT ud.email FROM user_details as ud join users as u on ud.user_id = u.id WHERE email = %s''',
                                (credentials.email,))
    if isinstance(credentials, UsernameLogin):
        data = await read_query('''SELECT username FROM users WHERE username = %s''',
                                (credentials.username,))
    return len(data) > 0


async def valid_password(credentials: EmailLogin | UsernameLogin):
    actual_password = None
    if isinstance(credentials, EmailLogin):
        result = await read_query('''SELECT u.password FROM user_details as ud join users as u on ud.user_id = u.id WHERE email = %s''', (credentials.email,))
        actual_password = result[0][0]
    elif isinstance(credentials, UsernameLogin):
        result = await read_query('''SELECT password FROM users WHERE username = %s ''', (credentials.username,))
        actual_password = result[0][0]

    return await verify_password(credentials.password, actual_password)


async def exists_by_username_email_phone(user: RegisterUser):
    data = await read_query('''SELECT username FROM users WHERE username =%s ''',
                            (user.username, ))
    data2 = await read_query('''SELECT email,phone_number FROM user_details WHERE phone_number =%s or email = %s''',
                            (user.phone_number, user.email))
    if len(data) > 0 or len(data2) > 0:
        return True
    return False

async def is_admin(token: str):
    user_id = oauth2.get_current_user(token)
    data = await read_query('''SELECT is_admin FROM users WHERE id = %s''',
                            (user_id,))
    role = data[0][0]
    return role == 1

async def exists_by_id(token):
    id = oauth2.get_current_user(token)
    data = await read_query('''SELECT id FROM users WHERE id = %s''',
                            (id,))

    return len(data) > 0




