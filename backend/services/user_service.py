from database.database_queries import read_query,update_query,insert_query
from schemas.user_models import RegisterUser, EmailLogin, UsernameLogin, DisplayUser, UpdateUser, AfterUpdateUser
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
        where_clauses.append(f"ud.phone_number regexp '{phone}'")
        # where_clauses.append(f"LOCATE('{phone}',ud.phone_number) > 0")
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

async def delete(id:int) -> DisplayUser:
    user = [DisplayUser.from_query_result(*row) for row in await read_query('''
            SELECT u.username,ud.email,ud.phone_number,ud.first_name,ud.last_name,ud.address 
            FROM users as u join user_details as ud on u.id = ud.user_id WHERE u.id = %s''',(id,))][0]

    await update_query('''DELETE FROM users WHERE id = %s''',(id,))

    return user

async def update(id:int,user:UpdateUser):
    old_user_data = await read_query('''
    SELECT password, email,first_name, last_name, phone_number, two_factor_method,title,gender,photo_selfie,identity_document,address,username,email_verified
    FROM users as u join user_details as ud on u.id = ud.user_id WHERE u.id = %s''',(id,))

    old =UpdateUser.from_query_result(*old_user_data[0][:-2])
    email_verified = old_user_data[0][-1]

    if user.password:
        unhashed = user.password
        user.password = await hash_password(user.password)

    merged = UpdateUser(password=user.password or old.password, email=user.email or old.email,
                        phone_number=user.phone_number or old.phone_number, first_name=user.first_name or old.first_name,
                        last_name=user.last_name or old.last_name, address=user.address or old.address,
                        two_factor_method=user.two_factor_method or old.two_factor_method,title=user.title or old.title,
                        gender=user.gender or old.gender,photo_selfie=user.photo_selfie or old.photo_selfie,identity_document=user.identity_document or old.identity_document)
    if user.email and user.email != old.email:
        email_verified = 0
        subject = "Virtual Wallet Account Confirmation"
        confirmation_link = f'http://127.0.0.1:8000/users/confirmation/{id}'
        message = f"Please click the link below to confirm your email address:\n\n{confirmation_link}"

        await send_email(user.email, confirmation_link, subject, message)


    await update_query('''
    UPDATE users as u,user_details as ud 
    SET u.password = %s,u.email_verified = %s,ud.email = %s,ud.phone_number = %s,ud.first_name = %s,ud.last_name = %s,ud.address = %s,
    u.two_factor_method = %s,ud.title = %s,ud.gender = %s,ud.photo_selfie = %s,ud.identity_document = %s Where u.id = %s and ud.user_id = %s''',
    (merged.password, email_verified, merged.email, merged.phone_number, merged.first_name, merged.last_name,
     merged.address, merged.two_factor_method,merged.title, merged.gender, merged.photo_selfie, merged.identity_document, id,id))

    return AfterUpdateUser.from_query_result(old_user_data[0][-2],unhashed, merged.email,  merged.first_name, merged.last_name,merged.phone_number,
     merged.two_factor_method,merged.title, merged.gender, merged.photo_selfie, merged.identity_document,merged.address)








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
    data = await read_query('''SELECT u.username,ud.email,ud.phone_number FROM users as u JOIN user_details as ud on u.id = ud.user_id 
    WHERE u.username = %s or ud.email = %s or ud.phone_number = %s ''',(user.username,user.email,user.phone_number))

    return len(data) > 0

async def check_exists_by_email_phone_for_updating(id:int,user: UpdateUser):
    data = await read_query('''SELECT ud.email,ud.phone_number FROM users as u JOIN user_details as ud on u.id = ud.user_id 
    WHERE (ud.email = %s or ud.phone_number = %s ) and u.id <> %s''',(user.email,user.phone_number,id))

    return len(data) > 0

async def is_admin(token: str):
    user_id = oauth2.get_current_user(token)
    data = await read_query('''SELECT is_admin FROM users WHERE id = %s''',
                            (user_id,))
    role = data[0][0]
    return role == 1

async def auth_exists_by_id(token):
    id = oauth2.get_current_user(token)
    data = await read_query('''SELECT id FROM users WHERE id = %s''',
                            (id,))

    return len(data) > 0

async def exists_by_id(id):
    data = await read_query('''SELECT id FROM users WHERE id = %s''',
                            (id,))

    return len(data) > 0

async def is_user_authorized_to_delete(token:str,id:int):
    user_id = oauth2.get_current_user(token)
    data = await read_query('''SELECT is_admin FROM users WHERE id = %s''',
               (user_id,))
    role = data[0][0]
    return user_id == id or role == 1

async def can_update(id: int,token: str):
    '''
    This function checks if the user exists and
    if he exists checks whether that user is the same as the logged in user.
    :param id: int
    :param token: str
    :return: bool
    '''
    auth_id = oauth2.get_current_user(token)
    data = await read_query('''SELECT id FROM users WHERE id = %s''',
                            (id,))

    return len(data) > 0 and auth_id == id




