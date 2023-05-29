import unittest
from schemas.transaction_models import Transaction,DisplayTransaction,DisplayTransactionInfo
from utils import oauth2
from asyncio import run
from services import transaction_service
from unittest.mock import Mock, patch


class TransactionService_Should(unittest.TestCase):
    @patch('services.transaction_service.read_query', autospec=True)
    def test_(self, mock_read_query):
        async def async_test():
            mock_read_query.return_value = []



        run(async_test())


