import unittest
from schemas.contact_models import Contact
from schemas.user_models import Username
from utils import oauth2
from asyncio import run
from services import contact_service
from unittest.mock import Mock, patch

USERNAME='DeanWinchester'
TOKEN = 'Bearer "'+oauth2.create_access_token(1)+'"'

class ContactService_Should(unittest.TestCase):
    @patch('services.contact_service.insert_query', autospec=True)
    def test_addContact(self, mock_insert_query):
        async def async_test():
            with patch('services.contact_service.read_query') as mock_read_query:
                mock_read_query.return_value = [(1,)]

                result = await contact_service.add_contact(USERNAME,TOKEN)
                expected = 'Contact added'
                self.assertEqual(expected, result)
        run(async_test())

    @patch('services.contact_service.update_query', autospec=True)
    def test_removeContact(self, mock_update_query):
        async def async_test():
            with patch('services.contact_service.read_query') as mock_read_query:
                mock_read_query.return_value = [(1,)]

                result = await contact_service.remove_contact(USERNAME, TOKEN)
                expected = 'Contact removed'
                self.assertEqual(expected, result)

        run(async_test())

    @patch('services.contact_service.read_query', autospec=True)
    def test_getContacts(self, mock_read_query):
        async def async_test():
            user1 = Username(username=USERNAME,photo_selfie='Photo')
            mock_read_query.return_value = [(USERNAME,'Photo')]

            result = await contact_service.get_contacts(TOKEN)

            self.assertEqual([user1,], list(result))


        run(async_test())

    @patch('services.contact_service.read_query', autospec=True)
    def test_isContact_returns_True_whenThereIsContact(self, mock_read_query):
        async def async_test():
            mock_read_query.return_value = [(1,2)]

            result = await contact_service.is_contact(USERNAME,TOKEN)

            self.assertEqual(True, result)

        run(async_test())

    @patch('services.contact_service.read_query', autospec=True)
    def test_isContact_returns_False_whenThereIsNoContact(self, mock_read_query):
        async def async_test():
            mock_read_query.return_value = []

            result = await contact_service.is_contact(USERNAME, TOKEN)

            self.assertEqual(False, result)

        run(async_test())





