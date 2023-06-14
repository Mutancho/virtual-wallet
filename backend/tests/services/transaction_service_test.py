import unittest
from schemas.transaction_models import Transaction,DisplayTransaction,DisplayTransactionInfo
from utils import oauth2
from asyncio import run
from services import transaction_service
from unittest.mock import Mock, patch,AsyncMock
from asyncmy.connection import Connection

AMOUNT = 1000.00
CATEGORY = 'Rent'
RECIPIENT = 'DeanWinchester'
WALLET = 1
IS_RECURRING = False
SENT_AT = '2023-05-01'
RECEIVED_AT = '2023-05-02'
EMAIL = 'myemail@gmail.com'
INFO1 = "Transaction created successfully. Awaiting your confirmation."
INFO2 = "Transaction created successfully. Awaiting recipient response."
TOKEN = 'Bearer "'+oauth2.create_access_token(1)+'"'
FROM_DATE = '2023-05-01'
TO_DATE = '2023-05-31'
SENDER = 'SamWinchester'
LIMIT = 1
OFFSET = 0
DIRECTION = 'outgoing'
CURRENCY = 'BGN'
CONNECTION = Mock(spec=Connection)


class TransactionService_Should(unittest.TestCase):
    @patch('services.transaction_service.manage_db_transaction', lambda x: CONNECTION).start()
    @patch('services.transaction_service.insert_query', autospec=True)
    def test_createTransaction(self, mock_insert_query, mock_manage_db_transaction):
        async def async_test():
            with patch('services.transaction_service.read_query') as mock_read_query:
                transaction_service.get_user_id_from_username = AsyncMock(return_value= 1)

                display_transaction = DisplayTransaction(
                    information=INFO2,amount=AMOUNT,category=CATEGORY,
                    recipient=RECIPIENT,wallet=WALLET)
                transaction = Transaction(amount=AMOUNT,category=CATEGORY,recipient=RECIPIENT,
                                          wallet=WALLET,is_recurring=IS_RECURRING)
                mock_read_query.side_effect = [[(EMAIL,)],[(EMAIL,)]]

                result = await transaction_service.create_transaction(transaction,TOKEN)

                self.assertEqual(DisplayTransaction,type(result))
                self.assertEqual(display_transaction,result)

                await transaction_service.get_user_id_from_username.reverse_mock()

        run(async_test())

    @patch('services.transaction_service.manage_db_transaction', lambda x: CONNECTION).start()
    @patch('services.transaction_service.read_query', autospec=True)
    def test_all(self, mock_read_query, mock_manage_db_transaction):
        async def async_test():
            transaction = DisplayTransactionInfo(amount=AMOUNT,category=CATEGORY,
                                                 recipient=1,wallet=WALLET,is_recurring=IS_RECURRING,
                                                 sent_at=SENT_AT,accepted=True,received_at=RECEIVED_AT,currency=CURRENCY)
            mock_read_query.return_value = [(AMOUNT,CATEGORY,1,WALLET,IS_RECURRING,SENT_AT,True,RECEIVED_AT)]
            result = await transaction_service.all(FROM_DATE,TO_DATE,SENDER,RECIPIENT,LIMIT,OFFSET)

            self.assertEqual(transaction,next(result,None))


        run(async_test())

    @patch('services.transaction_service.manage_db_transaction', lambda x: CONNECTION).start()
    @patch('services.transaction_service.read_query', autospec=True)
    def test_getTransaction(self, mock_read_query, mock_manage_db_transaction):
        async def async_test():
            transaction = DisplayTransactionInfo(amount=AMOUNT, category=CATEGORY,
                                                 recipient=1, wallet=WALLET, is_recurring=IS_RECURRING,
                                                 sent_at=SENT_AT, accepted=True, received_at=RECEIVED_AT,currency=CURRENCY)
            mock_read_query.return_value = [(AMOUNT, CATEGORY, 1, WALLET, IS_RECURRING, SENT_AT, True, RECEIVED_AT)]
            result = await transaction_service.get_transactions(FROM_DATE, TO_DATE, RECIPIENT, DIRECTION,LIMIT, OFFSET,TOKEN)

            self.assertEqual(transaction, next(result, None))

        run(async_test())





