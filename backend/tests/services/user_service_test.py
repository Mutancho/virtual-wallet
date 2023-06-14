import unittest
from unittest.mock import Mock, patch
from schemas.user_models import RegisterUser, EmailLogin, UsernameLogin, DisplayUser, UpdateUser, AfterUpdateUser, \
    BlockUnblock, Username
from services import user_service
from utils import oauth2
from asyncio import run
from asyncmy.connection import Connection
import responses

USERNAME = 'DeanWinchester'
PASSWORD = 'Deans10?'
FIRST_NAME = 'Dean'
LAST_NAME = 'Winchester'
EMAIL = 'dean@gmail.com'
PHONE_NUMBER = '0888123456'
DATE_OF_BIRTH = '1979-01-24'
ADDRESS = 'Lawrence, Kansas'
TWO_FACTOR = None
TITLE = 'Mr'
GENDER = 'male'
TOKEN = 'Bearer "' + oauth2.create_access_token(1) + '"'
CONNECTION = Mock(spec=Connection)


class UserService_Should(unittest.TestCase):

    @patch('services.user_service.insert_query', autospec=True)
    @patch('services.user_service.update_query', autospec=True)
    @patch('services.user_service.manage_db_transaction', lambda x: CONNECTION).start()
    def test_create_createsUser(self, mock_manage_db_transaction, mock_update_query, mock_insert_query):
        async def async_test():
            user = RegisterUser(
                username=USERNAME, password=PASSWORD, first_name=FIRST_NAME, last_name=LAST_NAME,
                email=EMAIL, phone_number=PHONE_NUMBER, date_of_birth=DATE_OF_BIRTH, address=ADDRESS,
                identity_document='photo'
            )
            mock_insert_query.return_value = 1
            mock_manage_db_transaction.return_value = CONNECTION
            result = await user_service.create(user)

            self.assertEqual(RegisterUser, type(result))
            self.assertEqual(1, result.id)

        run(async_test())

    @patch('services.user_service.update_query', autospec=True)
    @patch('services.user_service.manage_db_transaction', lambda x: CONNECTION).start()
    def test_confirm(self, manage_db_transaction, mock_update_query):
        async def async_test():
            expected_html = '''
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
            manage_db_transaction.return_value = CONNECTION
            result = await user_service.confirm(1)

            self.assertEqual(expected_html, result)

        run(async_test())

    @patch('services.user_service.insert_query', autospec=True)
    @patch('services.user_service.manage_db_transaction', lambda x: CONNECTION).start()
    def test_login_EmailLogin(self, manage_db_transaction, mock_insert_query):
        @responses.activate
        async def async_test():
            with patch('services.user_service.read_query') as mock_read_query:
                credentials = EmailLogin(email=EMAIL, password=PASSWORD)
                mock_read_query.return_value = [(1, EMAIL, 0)]
                token = oauth2.create_access_token(1)
                responses.get(url='https://api.chatengine.io/users/me/', status=200,
                              json={'username': EMAIL, 'secret': PASSWORD})
                response = {'username': EMAIL, 'secret': PASSWORD}

                result_emailLogin = await user_service.login(credentials)

                self.assertEqual(EmailLogin, type(credentials))
                self.assertEqual(dict(access_token=token, token_type="bearer", is_admin=False, response_data=response),
                                 result_emailLogin)

        run(async_test())

    @patch('services.user_service.insert_query', autospec=True)
    @patch('services.user_service.manage_db_transaction', lambda x: CONNECTION).start()
    def test_login_UsernameLogin(self, manage_db_transaction, mock_insert_query):
        @responses.activate
        async def async_test():
            with patch('services.user_service.read_query') as mock_read_query:
                credentials = UsernameLogin(username=USERNAME, password=PASSWORD)
                mock_read_query.return_value = [(1, USERNAME, 1)]
                token = oauth2.create_access_token(1)

                responses.get(url='https://api.chatengine.io/users/me/', status=200,
                              json={'username': USERNAME, 'secret': PASSWORD})
                response = {'username': USERNAME, 'secret': PASSWORD}

                result_usernameLogin = await user_service.login(credentials)

                self.assertEqual(UsernameLogin, type(credentials))
                self.assertEqual(dict(access_token=token, token_type="bearer", is_admin=True, response_data=response),
                                 result_usernameLogin)

        run(async_test())

    @patch('services.user_service.update_query', autospec=True)
    @patch('services.user_service.manage_db_transaction', lambda x: CONNECTION).start()
    def test_logout(self, manage_db_transaction, mock_update_query):
        async def async_test():
            token = TOKEN
            result = await user_service.logout(token)

            self.assertEqual('Logged out successfully', result)

        run(async_test())

    @patch('services.user_service.read_query', autospec=True)
    @patch('services.user_service.manage_db_transaction', lambda x: CONNECTION).start()
    def test_all(self, manage_db_transaction, mock_read_query):
        async def async_test():
            user = DisplayUser(username=USERNAME, email=EMAIL, phone_number=PHONE_NUMBER, first_name=FIRST_NAME,
                               last_name=LAST_NAME, address=ADDRESS)
            mock_read_query.return_value = [(USERNAME, EMAIL, PHONE_NUMBER, FIRST_NAME, LAST_NAME, ADDRESS)]

            result = await user_service.all(USERNAME, PHONE_NUMBER, EMAIL, None, None)

            self.assertEqual(user, next(result, None))

        run(async_test())

    @patch('services.user_service.update_query', autospec=True)
    @patch('services.user_service.manage_db_transaction', lambda x: CONNECTION).start()
    def test_delete(self, manage_db_transaction, mock_update_query):
        async def async_test():
            with patch('services.user_service.read_query') as mock_read_query:
                user = DisplayUser(username=USERNAME, email=EMAIL, phone_number=PHONE_NUMBER, first_name=FIRST_NAME,
                                   last_name=LAST_NAME, address=ADDRESS)
                mock_read_query.return_value = [
                    (USERNAME, EMAIL, PHONE_NUMBER, FIRST_NAME, LAST_NAME, ADDRESS)]
                result = await user_service.delete(1)

                self.assertEqual(user, result)

        run(async_test())

    @patch('services.user_service.update_query', autospec=True)
    @patch('services.user_service.manage_db_transaction', lambda x: CONNECTION).start()
    def test_update(self, manage_db_transaction, mock_update_query):
        async def async_test():
            with patch('services.user_service.read_query') as mock_read_query:
                user = UpdateUser(new_password='Newpass10!', repeat_password='Newpass10!', old_password=PASSWORD,
                                  email=EMAIL,
                                  first_name=FIRST_NAME, last_name=LAST_NAME)
                mock_read_query.return_value = [
                    (PASSWORD, EMAIL, FIRST_NAME, LAST_NAME, PHONE_NUMBER, TWO_FACTOR, TITLE, GENDER, None, None,
                     ADDRESS, USERNAME, 1)]
                result = await user_service.update(1, user)
                expected = AfterUpdateUser(username=USERNAME, password='Newpass10!', email=EMAIL,
                                           first_name=FIRST_NAME, last_name=LAST_NAME, phone_number=PHONE_NUMBER,
                                           two_factor_method=TWO_FACTOR, title=TITLE, gender=GENDER, address=ADDRESS)

                self.assertEqual(expected, result)

        run(async_test())

    @patch('services.user_service.update_query', autospec=True)
    @patch('services.user_service.manage_db_transaction', lambda x: CONNECTION).start()
    def test_block_unblock_Blocks(self, manage_db_transaction, mock_update_query):
        async def async_test():
            command = BlockUnblock(action='block')
            result = await user_service.block_unblock(USERNAME, command)

            self.assertEqual('User was blocked', result)

        run(async_test())

    @patch('services.user_service.update_query', autospec=True)
    @patch('services.user_service.manage_db_transaction', lambda x: CONNECTION).start()
    def test_block_unblock_Unblocks(self, manage_db_transaction, mock_update_query):
        async def async_test():
            command = BlockUnblock(action='unblock')
            result = await user_service.block_unblock(1, command)

            self.assertEqual('User was unblocked', result)

        run(async_test())

    @patch('services.user_service.read_query', autospec=True)
    @patch('services.user_service.manage_db_transaction', lambda x: CONNECTION).start()
    def test_getUser_returnsUsername(self, manage_db_transaction, mock_read_query):
        async def async_test():
            user = Username(username=USERNAME)
            mock_read_query.return_value = [(USERNAME,)]

            result = await user_service.get_user(USERNAME, EMAIL, PHONE_NUMBER)

            self.assertEqual(user, result)

        run(async_test())

    @patch('services.user_service.read_query', autospec=True)
    @patch('services.user_service.manage_db_transaction', lambda x: CONNECTION).start()
    def test_getUser_returnsNotFoundMessage(self, manage_db_transaction, mock_read_query):
        async def async_test():
            mock_read_query.return_value = []

            result = await user_service.get_user(USERNAME, EMAIL, PHONE_NUMBER)

            self.assertEqual("User not found", result)

        run(async_test())
