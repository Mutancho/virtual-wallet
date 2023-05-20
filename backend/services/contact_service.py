from database.database_queries import read_query,update_query,insert_query
from utils import oauth2
from schemas.user_models import Username


async def add_contact(username: str,token):
    id = oauth2.get_current_user(token)
    contact_id = await read_query('''SELECT id from users where username = %s''',(username,))

    await insert_query('''insert into contacts(user_id, contact_id) values(%s,%s)''',(id,contact_id[0][0]))

    return 'Contact added'

async def remove_contact(username,token):
    id = oauth2.get_current_user(token)
    contact_id = await read_query('''SELECT id from users where username = %s''', (username,))

    await update_query('''DELETE FROM contacts WHERE user_id =%s and contact_id = %s''', (id, contact_id[0][0]))

    return 'Contact removed'

async def get_contacts(token):
    id = oauth2.get_current_user(token)
    usernames = await read_query('''select username from users where id in (SELECT contact_id from contacts where user_id = %s)''',(id,))

    return (Username(username=u[0]) for u in usernames)



async def is_contact(username: str,token: str):
    id = oauth2.get_current_user(token)
    data = await read_query('''select c.user_id,c.contact_id from contacts as c 
    where c.user_id = %s and c.contact_id = (select id from users where username = %s)''', (id,username))
    return len(data) > 0