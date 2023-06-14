from database.database_queries import read_query, update_query, insert_query, manage_db_transaction
from schemas.user_models import RegisterUser, EmailLogin, UsernameLogin, DisplayUser, UpdateUser, AfterUpdateUser, \
    BlockUnblock, Username
from utils.passwords import hash_password, verify_password
from utils import oauth2
from utils.send_emails import send_email
from services.external_apis.stripe_api import create_customer
from config.config import settings
from asyncmy.connection import Connection
import requests

base_url = settings.base_url
chat_project_id = settings.chat_project_id
chat_private_key = settings.chat_private_key


@manage_db_transaction
async def create(conn: Connection, user: RegisterUser) -> RegisterUser:
    hashed = await hash_password(user.password)
    if user.identity_document:
        anti_money_laundry_checked = 1

    generate_id = await insert_query(conn, '''
    INSERT INTO users(username,password,title, first_name, last_name, gender, dob, address, email, phone_number, photo_selfie, identity_document,anti_money_laundry_checked) 
    VALUES (%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)''',
                                     (user.username, hashed, user.title, user.first_name, user.last_name, user.gender,
                                      user.date_of_birth, user.address, user.email, user.phone_number,
                                      user.photo_selfie, user.identity_document, anti_money_laundry_checked))

    user.id = generate_id
    subject = "Virtual Wallet Account Confirmation"
    confirmation_link = f'{base_url}/users/confirmations/{generate_id}'
    message = f"Please click the link below to confirm your email address:\n\n{confirmation_link}"

    await send_email(user.email, confirmation_link, subject, message)
    stripe_id = await create_customer(user.email, str(generate_id), user.first_name, user.last_name)
    await update_query(conn, "UPDATE users SET stripe_id = %s WHERE id = %s", (stripe_id, generate_id))

    response = requests.post('https://api.chatengine.io/users/',
                             data={
                                 "username": user.username,
                                 "secret": user.password,
                                 "email": user.email,
                                 "first_name": user.first_name,
                                 "last_name": user.last_name,
                             },
                             headers={"Private-Key": chat_private_key}
                             )
    # return response.json()

    return user


@manage_db_transaction
async def login(conn: Connection, credentials: EmailLogin | UsernameLogin):
    if isinstance(credentials, EmailLogin):
        data = await read_query(conn, '''SELECT id,email,is_admin FROM users WHERE email = %s''',
                                (credentials.email,))
    if isinstance(credentials, UsernameLogin):
        data = await read_query(conn, '''SELECT id,username,is_admin FROM users WHERE username = %s''',
                                (credentials.username,))
    id = data[0][0]
    admin = data[0][2]
    token = oauth2.create_access_token(id)
    await insert_query(conn, '''UPDATE users SET token = %s WHERE id = %s''', (token, id))

    response = requests.get('https://api.chatengine.io/users/me/',
                            headers={
                                "Project-ID": chat_project_id,
                                "User-Name": credentials.username,
                                "User-Secret": credentials.password
                            }
                            )
    # return response.json()
    return dict(access_token=token, token_type="bearer", is_admin=bool(admin),response_data= response.json())


@manage_db_transaction
async def logout(conn: Connection, token):
    id = oauth2.get_current_user(token)
    await update_query(conn, '''UPDATE users SET token = NULL WHERE id = %s''', (id,))

    return 'Logged out successfully'


@manage_db_transaction
async def all(conn: Connection, username, phone, email, limit, offset):
    sql = '''SELECT u.username,u.email,u.phone_number,u.first_name,u.last_name,u.address FROM users as u '''

    where_clauses = []
    if username:
        where_clauses.append(f"LOCATE('{username}',u.username) > 0")
    if email:
        where_clauses.append(f"LOCATE('{email}',u.email) > 0")
    if phone:
        where_clauses.append(f"u.phone_number regexp '{phone}'")
    if where_clauses:
        sql += ' WHERE ' + ' AND '.join(where_clauses)
    if limit:
        if offset:
            sql += f" limit {offset},{limit}"
        else:
            sql += f" limit {limit}"
    data = await read_query(conn, sql)

    return (DisplayUser.from_query_result(*row) for row in data)


@manage_db_transaction
async def delete(conn: Connection, id: int) -> DisplayUser:
    user = [DisplayUser.from_query_result(*row) for row in await read_query(conn, '''
            SELECT u.username,u.email,u.phone_number,u.first_name,u.last_name,u.address 
            FROM users as u WHERE u.id = %s''', (id,))][0]

    await update_query(conn, '''DELETE FROM users WHERE id = %s''', (id,))
    return user


@manage_db_transaction
async def update(conn: Connection, id: int, user: UpdateUser):
    old_user_data = await read_query(conn, '''
    SELECT password, email,first_name, last_name, phone_number, two_factor_method,title,gender,photo_selfie,identity_document,address,username,email_verified
    FROM users as u WHERE u.id = %s''', (id,))

    old = UpdateUser.from_query_result(*old_user_data[0][:-2])

    email_verified = old_user_data[0][-1]
    unhashed = '********'
    if user.new_password:
        unhashed = user.new_password
        user.new_password = await hash_password(user.new_password)

    merged = UpdateUser(new_password=user.new_password or old.old_password, email=user.email or old.email,
                        phone_number=user.phone_number or old.phone_number,
                        first_name=user.first_name or old.first_name,
                        last_name=user.last_name or old.last_name, address=user.address or old.address,
                        two_factor_method=user.two_factor_method or old.two_factor_method,
                        title=user.title or old.title,
                        gender=user.gender or old.gender, photo_selfie=user.photo_selfie or old.photo_selfie,
                        identity_document=user.identity_document or old.identity_document)
    if user.email and user.email != old.email:
        email_verified = 0
        subject = "Virtual Wallet Account Confirmation"
        confirmation_link = f'{base_url}/users/confirmations/{id}'
        message = f"Please click the link below to confirm your email address:\n\n{confirmation_link}"

        await send_email(user.email, confirmation_link, subject, message)

    await update_query(conn, '''
    UPDATE users as u
    SET u.password = %s,u.email_verified = %s,u.email = %s,u.phone_number = %s,u.first_name = %s,u.last_name = %s,u.address = %s,
    u.two_factor_method = %s,u.title = %s,u.gender = %s,u.photo_selfie = %s,u.identity_document = %s Where u.id = %s ''',
                       (merged.new_password, email_verified, merged.email, merged.phone_number, merged.first_name,
                        merged.last_name,
                        merged.address, merged.two_factor_method, merged.title, merged.gender, merged.photo_selfie,
                        merged.identity_document, id))

    return AfterUpdateUser.from_query_result(old_user_data[0][-2], unhashed, merged.email, merged.first_name,
                                             merged.last_name, merged.phone_number,
                                             merged.two_factor_method, merged.title, merged.gender, merged.photo_selfie,
                                             merged.identity_document, merged.address)


@manage_db_transaction
async def block_unblock(conn: Connection, username: str, command: BlockUnblock):

    if command.action == 'block':
        is_blocked = 1
        msg = 'User was blocked'
    else:
        is_blocked = 0
        msg = 'User was unblocked'
    await update_query(conn, '''UPDATE users SET is_blocked = %s WHERE username = %s ''', (is_blocked, username))

    return msg


@manage_db_transaction
async def get_user(conn: Connection, username, email, phone):
    sql = '''SELECT u.username FROM users as u'''

    where_clauses = []
    if username:
        where_clauses.append(f"u.username = '{username}'")
    if email:
        where_clauses.append(f"u.email = '{email}'")
    if phone:
        where_clauses.append(f"u.phone_number = '{phone}'")
    if where_clauses:
        sql += ' WHERE ' + ' AND '.join(where_clauses)

    data = await read_query(conn, sql)
    if data:
        return Username(username=data[0][0])
    else:
        return "User not found"


@manage_db_transaction
async def confirm(conn: Connection, id):
    await update_query(conn, '''UPDATE users set email_verified = 1 where id = %s''', (id,))

    return '''
    <!DOCTYPE html>
    <html>
    <head>
        <title>Email Verification</title>
        <style>
            body {
                font-family: Arial, sans-serif;
                text-align: center;
                margin-top: 100px;
            }

            h1 {
                color: #336699;
            }

            p {
                color: #666666;
            }
        </style>
    </head>
    <body>
        <h1>Your Email was Verified</h1>
        <p></p>
    </body>
    </html>
    '''


@manage_db_transaction
async def verify_credentials(conn: Connection, credentials: EmailLogin | UsernameLogin):
    data = None
    if isinstance(credentials, EmailLogin):
        data = await read_query(conn, '''SELECT u.email FROM users as u WHERE email = %s''',
                                (credentials.email,))
    if isinstance(credentials, UsernameLogin):
        data = await read_query(conn, '''SELECT username FROM users WHERE username = %s''',
                                (credentials.username,))
    return len(data) > 0


@manage_db_transaction
async def valid_password(conn: Connection, credentials: EmailLogin | UsernameLogin):
    actual_password = None
    if isinstance(credentials, EmailLogin):
        result = await read_query(conn, '''SELECT password FROM users WHERE email = %s''', (credentials.email,))
        actual_password = result[0][0]
    elif isinstance(credentials, UsernameLogin):
        result = await read_query(conn, '''SELECT password FROM users WHERE username = %s ''', (credentials.username,))
        actual_password = result[0][0]

    return await verify_password(credentials.password, actual_password)


@manage_db_transaction
async def exists_by_username_email_phone(conn: Connection, user):
    data = await read_query(
        conn,
        '''SELECT u.username,u.email,u.phone_number FROM users as u WHERE u.username = %s or u.email = %s or u.phone_number = %s ''',
        (user.username, user.email, user.phone_number))

    return len(data) > 0


@manage_db_transaction
async def check_exists_by_email_phone_for_updating(conn: Connection, id: int, user: UpdateUser):
    data = await read_query(conn,
                            '''SELECT u.email,u.phone_number FROM users as u WHERE (u.email = %s or u.phone_number = %s ) and u.id <> %s''',
                            (user.email, user.phone_number, id))

    return len(data) > 0


@manage_db_transaction
async def is_admin(conn: Connection, token: str):
    user_id = oauth2.get_current_user(token)
    data = await read_query(conn, '''SELECT is_admin FROM users WHERE id = %s''',
                            (user_id,))
    role = data[0][0]
    return role == 1


@manage_db_transaction
async def exists_by_id(conn: Connection, id):
    data = await read_query(conn, '''SELECT id FROM users WHERE id = %s''', (id,))

    return len(data) > 0


@manage_db_transaction
async def is_logged_in(conn: Connection, token):
    id = oauth2.get_current_user(token)
    db_token = await read_query(conn, '''SELECT token FROM users WHERE id = %s''', (id,))

    if db_token and db_token[0][0] == token[8:-1]:
        return True
    return False


@manage_db_transaction
async def is_user_authorized_to_delete(conn: Connection, token: str, id: int):
    user_id = oauth2.get_current_user(token)
    data = await read_query(conn, '''SELECT is_admin FROM users WHERE id = %s''',
                            (user_id,))
    role = data[0][0]
    return user_id == id or role == 1


@manage_db_transaction
async def is_blocked(conn: Connection, token):
    id = oauth2.get_current_user(token)
    blocked = await read_query(conn, '''SELECT is_blocked FROM users WHERE id = %s''', (id,))

    return bool(blocked[0][0])


@manage_db_transaction
async def can_update(conn: Connection, id: int, token: str, old_password, new_password, repeat_password):
    '''
    This function checks if the user exists and
    if he exists checks whether that user is the same as the logged in user.
    Also whether the provided passwords are correct
    :param conn: Connection
    :param id: int
    :param token: str
    :param old_password: str
    :param new_password: str
    :param repeat_password: str
    :return: bool
    '''
    auth_id = oauth2.get_current_user(token)
    data = await read_query(conn, '''SELECT id,password FROM users WHERE id = %s''',
                            (id,))
    if not old_password and new_password and repeat_password:
        return False
    if data and old_password is not None and not await verify_password(old_password, data[0][1]):
        return False
    if not repeat_password == new_password:
        return False

    return len(data) > 0 and auth_id == id
