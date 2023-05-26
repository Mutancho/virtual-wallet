from unittest import TestCase
from unittest.mock import patch
from asyncio import run
from services.wallets import create, all_wallets, wallet_by_id, delete, set_default_wallet, settings, \
    update_wallet_balance, get_user_id_from_username


class TestWalletCreation(TestCase):

    @patch("services.wallets.get_current_user")
    @patch("services.wallets.select_currency")
    @patch("services.wallets.insert_query")
    @patch("services.wallets._user_has_wallet")
    @patch("services.wallets._create_joint_wallet")
    def test_create_successfully(self, _create_joint_wallet, _user_has_wallet, insert_query,
                                 select_currency, get_current_user):
        async def async_test():
            mock_get_current_user.return_value = 