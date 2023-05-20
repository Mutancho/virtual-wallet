from database.database_queries import read_query,update_query,insert_query
from utils import oauth2


async def add_contact(username: str,token):
    id = oauth2.get_current_user(token)
    contact_id = await read_query('''SELECT id from users where username = %s''',(username,))

    await insert_query('''insert into contacts(user_id, contact_id) values(%s,%s)''',(id,contact_id[0][0]))

    return 'Contact added'

async def is_contact(username: str,token: str):
    id = oauth2.get_current_user(token)
    data = await read_query('''select c.user_id,c.contact_id from contacts as c 
    where c.user_id = %s and c.contact_id = (select id from users where username = %s)''', (id,username))
    return len(data) > 0