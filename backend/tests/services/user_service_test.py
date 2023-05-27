import unittest
from unittest.mock import Mock, patch
from schemas.user_models import RegisterUser, EmailLogin, UsernameLogin, DisplayUser, UpdateUser, AfterUpdateUser, BlockUnblock, Username
from services import user_service
from utils.passwords import hash_password, verify_password
from utils import oauth2
from asyncio import run

USERNAME='DeanWinchester'
PASSWORD='Deans10?'
FIRST_NAME='Dean'
LAST_NAME='Winchester'
EMAIL='dean@gmail.com'
PHONE_NUMBER='0888123456'
DATE_OF_BIRTH='24.01.1979'
ADDRESS='Lawrence, Kansas'
TWO_FACTOR = None
TITLE = 'Mr'
GENDER = 'male'
TOKEN = 'Bearer "'+oauth2.create_access_token(1)+'"'


class UserService_Should(unittest.TestCase):
    @patch('services.user_service.insert_query', autospec=True)
    def test_create_createsUser(self, mock_insert_query):
        async def async_test():
            user = RegisterUser(
                username=USERNAME,password=PASSWORD,first_name=FIRST_NAME,last_name=LAST_NAME,
            email=EMAIL, phone_number=PHONE_NUMBER, date_of_birth=DATE_OF_BIRTH, address=ADDRESS )
            mock_insert_query.return_value = 1
            result = await user_service.create(user)

            self.assertEqual(RegisterUser, type(result))
            self.assertEqual(1, result.id)
        run(async_test())

    @patch('services.user_service.update_query', autospec=True)
    def test_confirm(self, mock_update_query):
        async def async_test():
            result = await user_service.confirm(1)

            self.assertEqual('Verified',result)

        run(async_test())

    @patch('services.user_service.insert_query', autospec=True)
    def test_login_EmailLogin(self, mock_insert_query):
        async def async_test():
            with patch('services.user_service.read_query') as mock_read_query:
                credentials = EmailLogin(email=EMAIL, password=PASSWORD)
                mock_read_query.return_value = [(1,EMAIL)]
                token = oauth2.create_access_token(1)

                result_emailLogin = await user_service.login(credentials)

                self.assertEqual(EmailLogin,type(credentials))
                self.assertEqual(dict(access_token=token, token_type="bearer"),result_emailLogin)


        run(async_test())

    @patch('services.user_service.insert_query', autospec=True)
    def test_login_UsernameLogin(self, mock_insert_query):
        async def async_test():
            with patch('services.user_service.read_query') as mock_read_query:
                credentials = UsernameLogin(username=USERNAME,password=PASSWORD)
                mock_read_query.return_value = [(1, USERNAME)]
                token = oauth2.create_access_token(1)

                result_usernameLogin = await user_service.login(credentials)

                self.assertEqual(UsernameLogin, type(credentials))
                self.assertEqual(dict(access_token=token, token_type="bearer"), result_usernameLogin)

        run(async_test())

    @patch('services.user_service.update_query', autospec=True)
    def test_logout(self, mock_update_query):
        async def async_test():
            token = TOKEN
            result = await user_service.logout(token)

            self.assertEqual('Logged out successfully',result)

        run(async_test())

    @patch('services.user_service.read_query', autospec=True)
    def test_all(self, mock_read_query):
        async def async_test():
            user = DisplayUser(username=USERNAME, email=EMAIL, phone_number=PHONE_NUMBER, first_name=FIRST_NAME, last_name=LAST_NAME, address=ADDRESS)
            mock_read_query.return_value = [(USERNAME,EMAIL,PHONE_NUMBER,FIRST_NAME,LAST_NAME,ADDRESS)]

            result = await user_service.all(USERNAME,PHONE_NUMBER,EMAIL,None,None)


            self.assertEqual(user,next(result,None))
        run(async_test())

    @patch('services.user_service.update_query', autospec=True)
    def test_delete(self, mock_update_query):
        async def async_test():
            with patch('services.user_service.read_query') as mock_read_query:
                user = DisplayUser(username=USERNAME, email=EMAIL, phone_number=PHONE_NUMBER, first_name=FIRST_NAME,
                                   last_name=LAST_NAME, address=ADDRESS)
                mock_read_query.return_value = [
                    (USERNAME,EMAIL,PHONE_NUMBER,FIRST_NAME,LAST_NAME,ADDRESS)]
                result = await user_service.delete(1)

                self.assertEqual(user,result)

        run(async_test())

    @patch('services.user_service.update_query', autospec=True)
    def test_update(self, mock_update_query):
        async def async_test():
            with patch('services.user_service.read_query') as mock_read_query:
                user = UpdateUser(new_password='Newpass10!',repeat_password='Newpass10!',old_password=PASSWORD,email=EMAIL,
                                  first_name=FIRST_NAME,last_name=LAST_NAME)
                mock_read_query.return_value = [
                    (PASSWORD, EMAIL, FIRST_NAME, LAST_NAME,PHONE_NUMBER,TWO_FACTOR,TITLE,GENDER,None,None,
                     ADDRESS,USERNAME,1)]
                result = await user_service.update(1,user)
                expected = AfterUpdateUser(username=USERNAME,password='Newpass10!',email=EMAIL,
                                           first_name=FIRST_NAME,last_name=LAST_NAME,phone_number=PHONE_NUMBER,
                                           two_factor_method=TWO_FACTOR,title=TITLE,gender=GENDER,address=ADDRESS)

                self.assertEqual(expected, result)

        run(async_test())

    @patch('services.user_service.update_query', autospec=True)
    def test_block_unblock_Blocks(self, mock_update_query):
        async def async_test():
            command = BlockUnblock(action='block')
            result = await user_service.block_unblock(1,command)

            self.assertEqual('User was blocked',result)

        run(async_test())

    @patch('services.user_service.update_query', autospec=True)
    def test_block_unblock_Unblocks(self, mock_update_query):
        async def async_test():
            command = BlockUnblock(action='unblock')
            result = await user_service.block_unblock(1, command)

            self.assertEqual('User was unblocked', result)

        run(async_test())

    @patch('services.user_service.read_query', autospec=True)
    def test_getUser_returnsUsername(self, mock_read_query):
        async def async_test():
            user = Username(username=USERNAME)
            mock_read_query.return_value = [(USERNAME,)]

            result = await user_service.get_user(USERNAME,EMAIL,PHONE_NUMBER)

            self.assertEqual(user,result)

        run(async_test())

    @patch('services.user_service.read_query', autospec=True)
    def test_getUser_returnsNotFoundMessage(self, mock_read_query):
        async def async_test():

            mock_read_query.return_value = []

            result = await user_service.get_user(USERNAME, EMAIL, PHONE_NUMBER)

            self.assertEqual("User not found", result)

        run(async_test())