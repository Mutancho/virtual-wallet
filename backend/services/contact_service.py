from database.database_queries import read_query, update_query, insert_query, manage_db_transaction
from utils import oauth2
from schemas.user_models import Username
from asyncmy.connection import Connection


@manage_db_transaction
async def add_contact(conn: Connection, username: str, token):
    id = oauth2.get_current_user(token)
    contact_id = await read_query(conn, '''SELECT id from users where username = %s''', (username,))

    await insert_query(conn, '''insert into contacts(user_id, contact_id) values(%s,%s)''', (id, contact_id[0][0]))

    return 'Contact added'


@manage_db_transaction
async def remove_contact(conn: Connection, username, token):
    id = oauth2.get_current_user(token)
    contact_id = await read_query(conn, '''SELECT id from users where username = %s''', (username,))

    await update_query(conn, '''DELETE FROM contacts WHERE user_id =%s and contact_id = %s''', (id, contact_id[0][0]))

    return 'Contact removed'


@manage_db_transaction
async def get_contacts(conn: Connection, token):
    id = oauth2.get_current_user(token)
    usernames = await read_query(
        conn,
        '''select username,photo_selfie from users where id in (SELECT contact_id from contacts where user_id = %s)''',
        (id,))

    return (Username(username=u[0], photo_selfie=None if u[1] is None else u[1]) for u in usernames)


@manage_db_transaction
async def is_contact(conn: Connection, username: str, token: str):
    id = oauth2.get_current_user(token)
    data = await read_query(conn, '''select c.user_id,c.contact_id from contacts as c 
    where c.user_id = %s and c.contact_id = (select id from users where username = %s)''', (id, username))
    return len(data) > 0
