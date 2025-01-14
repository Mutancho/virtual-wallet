import pytest
from unittest.mock import patch, AsyncMock, Mock
from pydantic import ValidationError
from schemas.wallet_models import NewWallet, ViewAllWallets, ViewWallet, WalletSettings, Member
from services.custom_errors.wallets import NotWalletAdmin, UserAlreadyInGroup, NoWithdrawalAccess, NoTopUpAccess, \
    WithdrawMoreThanBalance
from services.wallets import create, all_wallets, wallet_by_id, settings, update_wallet_balance
import tests.constants as C
from asyncmy.connection import Connection

CONNECTION = Mock(spec=Connection)


class TestCreateWalletShould:

    @pytest.mark.asyncio
    @patch("services.wallets.get_current_user")
    @patch("services.wallets.select_currency", new_callable=AsyncMock)
    @patch("services.wallets.insert_query", new_callable=AsyncMock)
    @patch("services.wallets._user_has_wallet", new_callable=AsyncMock)
    @patch("services.wallets._create_joint_wallet", new_callable=AsyncMock)
    @patch('services.wallets.manage_db_transaction', lambda x: CONNECTION).start()
    async def test_successful(self, mock_manage_db_transaction, mock_create_joint_wallet, mock_user_has_wallet,
                              mock_insert_query,
                              mock_select_currency, mock_get_current_user):
        mock_get_current_user.return_value = C.CURRENT_USER_ID
        mock_select_currency.return_value = C.WALLET_CURRENCY_BGN
        mock_insert_query.return_value = C.SUCCESSFUL_WALLET_CREATION
        mock_user_has_wallet.return_value = C.USER_NO_WALLET
        mock_create_joint_wallet.return_value = C.SUCCESSFUL_WALLET_CREATION
        mock_manage_db_transaction.return_value = CONNECTION

        created_wallet = await create(C.NEW_PERSONAL_WALLET, C.TOKEN)
        assert created_wallet == C.SUCCESSFUL_WALLET_CREATION

        created_wallet = await create(C.NEW_JOINT_WALLET, C.TOKEN)
        assert created_wallet == C.SUCCESSFUL_WALLET_CREATION

    @pytest.mark.asyncio
    @patch("services.wallets.get_current_user")
    @patch("services.wallets.select_currency", new_callable=AsyncMock)
    @patch("services.wallets.insert_query", new_callable=AsyncMock)
    @patch("services.wallets._user_has_wallet", new_callable=AsyncMock)
    @patch("services.wallets._create_joint_wallet", new_callable=AsyncMock)
    @patch('services.wallets.manage_db_transaction', lambda x: CONNECTION).start()
    async def test_unsuccessful(self, mock_manage_db_transaction, mock_create_joint_wallet, mock_user_has_wallet,
                                mock_insert_query,
                                mock_select_currency, mock_get_current_user):
        mock_get_current_user.return_value = C.CURRENT_USER_ID
        mock_select_currency.return_value = C.WALLET_CURRENCY_BGN
        mock_insert_query.return_value = C.SUCCESSFUL_WALLET_CREATION
        mock_user_has_wallet.return_value = C.USER_NO_WALLET
        mock_create_joint_wallet.return_value = C.UNSUCCESSFUL_WALLET_CREATION
        mock_manage_db_transaction.return_value = CONNECTION

        with pytest.raises(ValidationError) as context:
            await create(NewWallet(type="personal", name="Regular", currency="SFK"), C.TOKEN)
        assert "string does not match regex" in str(context.value)

        with pytest.raises(ValidationError) as context:
            await create(NewWallet(type="joint", name="Joint", currency="SFK"), C.TOKEN)
        assert "string does not match regex" in str(context.value)

        with pytest.raises(ValidationError):
            await create(NewWallet(type="invalid", name="Joint", currency="BGN"), C.TOKEN)


class TestViewWalletsShould:

    @pytest.mark.asyncio
    @patch("services.wallets.get_current_user")
    @patch("services.wallets.read_query", new_callable=AsyncMock)
    @patch("services.wallets._view_group_members", new_callable=AsyncMock)
    @patch('services.wallets.manage_db_transaction', lambda x: CONNECTION).start()
    async def test_successful(self, mock_manage_db_transaction, mock_view_group_members, mock_read_query,
                              mock_get_current_user):
        mock_get_current_user.return_value = C.CURRENT_USER_ID
        mock_read_query.side_effect = [
            C.SUCCESSFUL_WALLET_QUERY_RESULT,
            C.SUCCESSFUL_OWNER_QUERY_RESULT
        ]
        mock_view_group_members.return_value = C.SUCCESSFUL_GROUP_MEMBERS_RESULT
        mock_manage_db_transaction.return_value = CONNECTION

        result = await all_wallets(C.TOKEN)
        expected_result = ViewAllWallets(
            owner=C.SUCCESSFUL_OWNER_QUERY_RESULT[0][0],
            wallets=[
                ViewWallet.from_query_result(*wallet) for wallet in C.SUCCESSFUL_WALLET_QUERY_RESULT
            ]
        )

        expected_result.wallets[1].members = C.SUCCESSFUL_GROUP_MEMBERS_RESULT

        assert result == expected_result


class TestWalletByIdShould:
    @pytest.mark.asyncio
    @patch("services.wallets.get_current_user")
    @patch("services.wallets.read_query", new_callable=AsyncMock)
    @patch("services.wallets._view_group_members", new_callable=AsyncMock)
    @patch('services.wallets.manage_db_transaction', lambda x: CONNECTION).start()
    async def test_return_wallet_when_found(self, mock_manage_db_transaction, mock_view_group_members, mock_read_query,
                                            mock_get_current_user):
        mock_get_current_user.return_value = C.CURRENT_USER_ID
        mock_read_query.return_value = C.SUCCESSFUL_WALLET_QUERY_RESULT
        mock_view_group_members.return_value = C.SUCCESSFUL_GROUP_MEMBERS_RESULT
        mock_manage_db_transaction.return_value = CONNECTION

        result = await wallet_by_id(C.VALID_WALLET_ID, C.TOKEN)
        expected_result = ViewWallet.from_query_result(*C.SUCCESSFUL_WALLET_QUERY_RESULT[0])
        expected_result.members = C.SUCCESSFUL_GROUP_MEMBERS_RESULT

        assert result == expected_result

    @pytest.mark.asyncio
    @patch("services.wallets.get_current_user")
    @patch("services.wallets.read_query", new_callable=AsyncMock)
    @patch("services.wallets._view_group_members", new_callable=AsyncMock)
    @patch('services.wallets.manage_db_transaction', lambda x: CONNECTION).start()
    async def test_return_wallet_when_found(self, mock_manage_db_transaction, mock_view_group_members, mock_read_query,
                                            mock_get_current_user):
        mock_get_current_user.return_value = C.CURRENT_USER_ID
        mock_read_query.return_value = C.SUCCESSFUL_WALLET_QUERY_RESULT
        mock_view_group_members.return_value = C.SUCCESSFUL_GROUP_MEMBERS_RESULT
        mock_manage_db_transaction.return_value = CONNECTION

        result = await wallet_by_id(C.VALID_WALLET_ID, C.TOKEN)
        expected_result = ViewWallet.from_query_result(*C.SUCCESSFUL_WALLET_QUERY_RESULT[0])
        expected_result.members = C.SUCCESSFUL_GROUP_MEMBERS_RESULT if expected_result.type == 'JOINT' else None

        assert result == expected_result


class TestWalletSettingsShould:
    @pytest.mark.asyncio
    @patch("services.wallets.get_current_user")
    @patch("services.wallets._wallet_exists", new_callable=AsyncMock)
    @patch('services.wallets.manage_db_transaction', lambda x: CONNECTION).start()
    async def test_return_none_when_wallet_does_not_exist(self, mock_manage_db_transaction, mock_wallet_exists,
                                                          mock_get_current_user):
        mock_get_current_user.return_value = C.CURRENT_USER_ID
        mock_wallet_exists.return_value = False
        mock_manage_db_transaction.return_value = CONNECTION

        result = await settings(C.WALLET_SETTINGS, C.VALID_WALLET_ID, C.TOKEN)

        assert result is None

    @pytest.mark.asyncio
    @patch("services.wallets.get_current_user")
    @patch("services.wallets._wallet_exists", new_callable=AsyncMock)
    @patch("services.wallets._is_wallet_admin", new_callable=AsyncMock)
    @patch('services.wallets.manage_db_transaction', lambda x: CONNECTION).start()
    async def test_raise_error_when_not_wallet_admin(self, mock_manage_db_transaction, mock_is_wallet_admin,
                                                     mock_wallet_exists,
                                                     mock_get_current_user):
        mock_get_current_user.return_value = C.CURRENT_USER_ID
        mock_wallet_exists.return_value = True
        mock_is_wallet_admin.return_value = False
        mock_manage_db_transaction.return_value = CONNECTION

        with pytest.raises(NotWalletAdmin):
            await settings(C.WALLET_SETTINGS, C.VALID_WALLET_ID, C.TOKEN)

    @pytest.mark.asyncio
    @patch("services.wallets.get_current_user")
    @patch("services.wallets._wallet_exists", new_callable=AsyncMock)
    @patch("services.wallets._is_wallet_admin", new_callable=AsyncMock)
    @patch("services.wallets._change_wallet_name", new_callable=AsyncMock)
    @patch('services.wallets.manage_db_transaction', lambda x: CONNECTION).start()
    async def test_change_wallet_name(self, mock_manage_db_transaction, mock_change_wallet_name, mock_is_wallet_admin,
                                      mock_wallet_exists,
                                      mock_get_current_user):
        mock_get_current_user.return_value = C.CURRENT_USER_ID
        mock_wallet_exists.return_value = True
        mock_is_wallet_admin.return_value = True
        mock_change_wallet_name.return_value = True
        mock_manage_db_transaction.return_value = CONNECTION

        wallet_settings = WalletSettings(
            change_wallet_name=True,
            name="new_name",
        )

        result = await settings(wallet_settings, C.VALID_WALLET_ID, C.TOKEN)

        mock_get_current_user.assert_called_once_with(C.TOKEN)
        mock_wallet_exists.assert_called_once_with(C.VALID_WALLET_ID)
        mock_is_wallet_admin.assert_called_once_with(C.CURRENT_USER_ID)
        mock_change_wallet_name.assert_called_once_with(wallet_settings.name, C.VALID_WALLET_ID)

        assert result is True

    @pytest.mark.asyncio
    @patch("services.wallets.get_current_user")
    @patch("services.wallets._is_wallet_admin", new_callable=AsyncMock)
    @patch("services.wallets._wallet_exists", new_callable=AsyncMock)
    @patch("services.wallets._change_wallet_name", new_callable=AsyncMock)
    @patch("services.wallets._wallet_status", new_callable=AsyncMock)
    @patch('services.wallets.manage_db_transaction', lambda x: CONNECTION).start()
    async def test_status_wallet_change(self, mock_manage_db_transaction, mock_wallet_status, mock_wallet_name,
                                        mock_wallet_exists,
                                        mock_is_wallet_admin,
                                        mock_get_current_user):
        mock_get_current_user.return_value = C.CURRENT_USER_ID
        mock_is_wallet_admin.return_value = True
        mock_wallet_exists.return_value = True
        mock_wallet_name.return_value = None
        mock_wallet_status.return_value = True
        mock_manage_db_transaction.return_value = CONNECTION

        wallet_settings = WalletSettings(status=True)
        result = await settings(wallet_settings, C.VALID_WALLET_ID, C.TOKEN)

        assert result is True
        mock_get_current_user.assert_called_once_with(C.TOKEN)
        mock_is_wallet_admin.assert_called_once_with(C.CURRENT_USER_ID)
        mock_wallet_exists.assert_called_once_with(C.VALID_WALLET_ID)
        mock_wallet_status.assert_called_once_with(True, C.VALID_WALLET_ID)
        mock_wallet_name.assert_not_called()

    @pytest.mark.asyncio
    @patch("services.wallets.get_current_user")
    @patch("services.wallets._is_wallet_admin", new_callable=AsyncMock)
    @patch("services.wallets._wallet_exists", new_callable=AsyncMock)
    @patch("services.wallets.get_user_id_from_username", new_callable=AsyncMock)
    @patch("services.wallets._add_user_to_joint_wallet", new_callable=AsyncMock)
    @patch('services.wallets.manage_db_transaction', lambda x: CONNECTION).start()
    async def test_add_user_to_wallet(self, mock_manage_db_transaction, mock_add_user, mock_get_user_id,
                                      mock_wallet_exists, mock_is_wallet_admin,
                                      mock_get_current_user):
        mock_get_current_user.return_value = C.CURRENT_USER_ID
        mock_is_wallet_admin.return_value = True
        mock_wallet_exists.return_value = True
        mock_get_user_id.return_value = C.USER_ID
        mock_add_user.return_value = True
        mock_manage_db_transaction.return_value = CONNECTION

        wallet_settings = WalletSettings(add_username=C.USERNAME)
        result = await settings(wallet_settings, C.VALID_WALLET_ID, C.TOKEN)

        assert result is True
        mock_get_current_user.assert_called_once_with(C.TOKEN)
        mock_is_wallet_admin.assert_called_once_with(C.CURRENT_USER_ID)
        mock_wallet_exists.assert_called_once_with(C.VALID_WALLET_ID)
        mock_get_user_id.assert_called_once_with(C.USERNAME)
        mock_add_user.assert_called_once_with(C.USER_ID, C.VALID_WALLET_ID)

    @pytest.mark.asyncio
    @patch("services.wallets.get_current_user")
    @patch("services.wallets._is_wallet_admin", new_callable=AsyncMock)
    @patch("services.wallets._wallet_exists", new_callable=AsyncMock)
    @patch("services.wallets.get_user_id_from_username", new_callable=AsyncMock)
    @patch("services.wallets._add_user_to_joint_wallet", new_callable=AsyncMock)
    @patch('services.wallets.manage_db_transaction', lambda x: CONNECTION).start()
    async def test_add_user_to_wallet_raise_error_already_exists(self, mock_manage_db_transaction, mock_add_user,
                                                                 mock_get_user_id,
                                                                 mock_wallet_exists, mock_is_wallet_admin,
                                                                 mock_get_current_user):
        mock_get_current_user.return_value = C.CURRENT_USER_ID
        mock_is_wallet_admin.return_value = True
        mock_wallet_exists.return_value = True
        mock_get_user_id.return_value = C.USER_ID
        mock_add_user.return_value = True
        mock_manage_db_transaction.return_value = CONNECTION

        wallet_settings = WalletSettings(add_username=C.USERNAME)

        mock_add_user.side_effect = UserAlreadyInGroup()

        with pytest.raises(UserAlreadyInGroup):
            await settings(wallet_settings, C.VALID_WALLET_ID, C.TOKEN)

        mock_get_current_user.assert_called_once_with(C.TOKEN)
        mock_is_wallet_admin.assert_called_once_with(C.CURRENT_USER_ID)
        mock_wallet_exists.assert_called_once_with(C.VALID_WALLET_ID)
        mock_get_user_id.assert_called_once_with(C.USERNAME)
        mock_add_user.assert_called_once_with(C.USER_ID, C.VALID_WALLET_ID)

    @pytest.mark.asyncio
    @patch("services.wallets.get_current_user")
    @patch("services.wallets._is_wallet_admin", new_callable=AsyncMock)
    @patch("services.wallets._wallet_exists", new_callable=AsyncMock)
    @patch("services.wallets.get_user_id_from_username", new_callable=AsyncMock)
    @patch("services.wallets._remove_user_from_joint_wallet", new_callable=AsyncMock)
    @patch('services.wallets.manage_db_transaction', lambda x: CONNECTION).start()
    async def test_remove_user_from_wallet(self, mock_manage_db_transaction, mock_remove_username, mock_get_user_id,
                                           mock_wallet_exists,
                                           mock_is_wallet_admin,
                                           mock_get_current_user):
        mock_get_current_user.return_value = C.CURRENT_USER_ID
        mock_is_wallet_admin.return_value = True
        mock_wallet_exists.return_value = True
        mock_get_user_id.return_value = C.USER_ID
        mock_remove_username.return_value = True
        mock_manage_db_transaction.return_value = CONNECTION

        wallet_settings = WalletSettings(remove_username=C.USERNAME)
        result = await settings(wallet_settings, C.VALID_WALLET_ID, C.TOKEN)

        assert result is True
        mock_get_current_user.assert_called_once_with(C.TOKEN)
        mock_is_wallet_admin.assert_called_once_with(C.CURRENT_USER_ID)
        mock_wallet_exists.assert_called_once_with(C.VALID_WALLET_ID)
        mock_get_user_id.assert_called_once_with(C.USERNAME)
        mock_remove_username.assert_called_once_with(C.USER_ID, C.VALID_WALLET_ID)

    @pytest.mark.asyncio
    @patch("services.wallets.get_current_user")
    @patch("services.wallets._is_wallet_admin", new_callable=AsyncMock)
    @patch("services.wallets._wallet_exists", new_callable=AsyncMock)
    @patch("services.wallets.get_user_id_from_username", new_callable=AsyncMock)
    @patch("services.wallets._amend_user_access_joint_wallet", new_callable=AsyncMock)
    @patch('services.wallets.manage_db_transaction', lambda x: CONNECTION).start()
    async def test_change_user_access(self, mock_manage_db_transaction, mock_amend_user_access, mock_get_user_id,
                                      mock_wallet_exists,
                                      mock_is_wallet_admin, mock_get_current_user):
        mock_get_current_user.return_value = C.CURRENT_USER_ID
        mock_is_wallet_admin.return_value = True
        mock_wallet_exists.return_value = True
        mock_get_user_id.return_value = C.USER_ID
        mock_manage_db_transaction.return_value = CONNECTION

        wallet_settings = WalletSettings(username=C.USERNAME, change_user_access=C.WALLET_NULL_ACCESS)
        result = await settings(wallet_settings, C.VALID_WALLET_ID, C.TOKEN)

        assert result is True
        mock_get_current_user.assert_called_once_with(C.TOKEN)
        mock_is_wallet_admin.assert_called_once_with(C.CURRENT_USER_ID)
        mock_wallet_exists.assert_called_once_with(C.VALID_WALLET_ID)
        mock_get_user_id.assert_called_once_with(C.USERNAME)
        mock_amend_user_access.assert_called_once_with(C.WALLET_NULL_ACCESS, C.USER_ID, C.VALID_WALLET_ID)

    @pytest.mark.asyncio
    @patch("services.wallets.get_current_user")
    @patch("services.wallets._wallet_exists", new_callable=AsyncMock)
    @patch("services.wallets._is_wallet_admin", new_callable=AsyncMock)
    @patch("services.wallets.get_user_id_from_username", new_callable=AsyncMock)
    @patch("services.wallets._amend_user_access_joint_wallet", new_callable=AsyncMock)
    @patch("services.wallets._add_user_to_joint_wallet", new_callable=AsyncMock)
    @patch('services.wallets.manage_db_transaction', lambda x: CONNECTION).start()
    async def test_amend_user_access(self, mock_manage_db_transaction, mock_add_user, mock_amend_user_access,
                                     mock_get_user_id,
                                     mock_is_wallet_admin, mock_wallet_exists,
                                     mock_get_current_user):
        mock_get_current_user.return_value = C.CURRENT_USER_ID
        mock_wallet_exists.return_value = True
        mock_is_wallet_admin.return_value = True
        mock_get_user_id.return_value = C.OTHER_USER_ID
        mock_amend_user_access.return_value = True
        mock_add_user.return_value = True
        mock_manage_db_transaction.return_value = CONNECTION

        wallet_settings = WalletSettings(
            change_user_access="full",
            username="other_user"
        )

        result = await settings(wallet_settings, C.VALID_WALLET_ID, C.TOKEN)
        assert result is True
        mock_get_current_user.assert_called_once_with(C.TOKEN)
        mock_wallet_exists.assert_called_once_with(C.VALID_WALLET_ID)
        mock_is_wallet_admin.assert_called_once_with(C.CURRENT_USER_ID)
        mock_get_user_id.assert_called_once_with(wallet_settings.username)
        mock_amend_user_access.assert_called_once_with(wallet_settings.change_user_access, C.OTHER_USER_ID,
                                                       C.VALID_WALLET_ID)
        mock_manage_db_transaction.return_value = CONNECTION
        mock_add_user.assert_not_called()

    @pytest.mark.asyncio
    @patch("services.wallets.get_current_user")
    @patch("services.wallets._is_wallet_admin", new_callable=AsyncMock)
    @patch("services.wallets._wallet_exists", new_callable=AsyncMock)
    @patch('services.wallets.manage_db_transaction', lambda x: CONNECTION).start()
    async def test_not_admin(self, mock_manage_db_transaction, mock_wallet_exists, mock_is_wallet_admin,
                             mock_get_current_user):
        mock_get_current_user.return_value = C.CURRENT_USER_ID
        mock_is_wallet_admin.return_value = False
        mock_wallet_exists.return_value = True
        mock_manage_db_transaction.return_value = CONNECTION

        wallet_settings = WalletSettings(status=True)

        with pytest.raises(NotWalletAdmin):
            await settings(wallet_settings, C.VALID_WALLET_ID, C.TOKEN)

        mock_get_current_user.assert_called_once_with(C.TOKEN)
        mock_is_wallet_admin.assert_called_once_with(C.CURRENT_USER_ID)
        mock_wallet_exists.assert_called_once_with(C.VALID_WALLET_ID)

    @pytest.mark.asyncio
    @patch("services.wallets.get_current_user")
    @patch("services.wallets._is_wallet_admin", new_callable=AsyncMock)
    @patch("services.wallets._wallet_exists", new_callable=AsyncMock)
    @patch('services.wallets.manage_db_transaction', lambda x: CONNECTION).start()
    async def test_status_wallet_change(self, mock_manage_db_transaction, mock_wallet_exists, mock_is_wallet_admin,
                                        mock_get_current_user):
        mock_get_current_user.return_value = C.CURRENT_USER_ID
        mock_is_wallet_admin.return_value = True
        mock_wallet_exists.return_value = False
        mock_manage_db_transaction.return_value = CONNECTION

        wallet_settings = WalletSettings(status=True)

        result = await settings(wallet_settings, C.VALID_WALLET_ID, C.TOKEN)

        assert result is None
        mock_get_current_user.assert_called_once_with(C.TOKEN)
        mock_is_wallet_admin.assert_called_once_with(C.CURRENT_USER_ID)
        mock_wallet_exists.assert_called_once_with(C.VALID_WALLET_ID)


class TestViewGroupMembersShould:
    def test_member_model(self):
        member_data = {
            "user_id": C.USER_ID,
            "name": C.USERNAME,
            "access_level": C.ACCESS_LEVEL
        }

        member = Member(**member_data)

        assert member.user_id == C.USER_ID
        assert member.name == C.USERNAME
        assert member.access_level == C.ACCESS_LEVEL

        invalid_member_data = [
            {"name": C.USERNAME, "access_level": C.ACCESS_LEVEL},
            {"user_id": C.USER_ID, "access_level": C.ACCESS_LEVEL},
            {"user_id": C.USER_ID, "name": C.USERNAME, "access_level": C.INVALID_WALLET_TYPE},
        ]
        for data in invalid_member_data:
            try:
                Member(**data)
            except ValidationError:
                pass
            else:
                assert False, "ValidationError not raised"


class TestUpdateWalletBalance:
    @pytest.mark.asyncio
    @patch('services.wallets.get_current_user')
    @patch('services.wallets.read_query', new_callable=AsyncMock)
    @patch('services.wallets.update_query', new_callable=AsyncMock)
    @patch('services.wallets.manage_db_transaction', lambda x: CONNECTION).start()
    async def test_update_wallet_balance(self, mock_manage_db_transaction, mock_update_query, mock_read_query,
                                         mock_get_current_user):
        mock_get_current_user.return_value = C.CURRENT_USER_ID
        mock_read_query.return_value = [(C.NEW_PERSONAL_WALLET.type,)]
        mock_update_query.return_value = C.SUCCESSFUL_WALLET_CREATION
        mock_manage_db_transaction.return_value = CONNECTION

        result = await update_wallet_balance(C.VALID_WALLET_ID, C.WALLET_BALANCE_100, C.TOKEN, C.TOP_UP)
        assert result is True

    @pytest.mark.asyncio
    @patch('services.wallets.get_current_user')
    @patch('services.wallets.read_query', new_callable=AsyncMock)
    @patch('services.wallets.update_query', new_callable=AsyncMock)
    @patch('services.wallets.manage_db_transaction', lambda x: CONNECTION).start()
    async def test_update_wallet_balance_joint_no_withdrawal_access(self, mock_manage_db_transaction, mock_update_query,
                                                                    mock_read_query,
                                                                    mock_get_current_user):
        mock_get_current_user.return_value = C.CURRENT_USER_ID
        mock_read_query.side_effect = [[(C.NEW_JOINT_WALLET.type,)], [(C.WALLET_NULL_ACCESS,)]]
        mock_manage_db_transaction.return_value = CONNECTION

        with pytest.raises(NoWithdrawalAccess):
            await update_wallet_balance(C.VALID_WALLET_ID, -C.WALLET_BALANCE_100, C.TOKEN, C.WITHDRAW)

    @pytest.mark.asyncio
    @patch('services.wallets.get_current_user')
    @patch('services.wallets.read_query', new_callable=AsyncMock)
    @patch('services.wallets.update_query', new_callable=AsyncMock)
    @patch('services.wallets.manage_db_transaction', lambda x: CONNECTION).start()
    async def test_update_wallet_balance_joint_no_top_up_access(self, mock_manage_db_transaction, mock_update_query,
                                                                mock_read_query,
                                                                mock_get_current_user):
        mock_get_current_user.return_value = C.CURRENT_USER_ID
        mock_read_query.side_effect = [[(C.NEW_JOINT_WALLET.type,)], [(C.WALLET_NULL_ACCESS,)]]
        mock_manage_db_transaction.return_value = CONNECTION

        with pytest.raises(NoTopUpAccess):
            await update_wallet_balance(C.VALID_WALLET_ID, C.WALLET_BALANCE_100, C.TOKEN, C.TOP_UP)

    @pytest.mark.asyncio
    @patch('services.wallets.get_current_user')
    @patch('services.wallets.read_query', new_callable=AsyncMock)
    @patch('services.wallets.update_query', new_callable=AsyncMock)
    @patch('services.wallets.manage_db_transaction', lambda x: CONNECTION).start()
    async def test_update_wallet_balance_withdraw_more_than_balance(self, mock_manage_db_transaction, mock_update_query,
                                                                    mock_read_query,
                                                                    mock_get_current_user):
        mock_get_current_user.return_value = C.CURRENT_USER_ID
        mock_read_query.side_effect = [[(C.NEW_PERSONAL_WALLET.type,)]]

        withdrawal_amount = C.WITHDRAWAL_AMOUNT
        current_balance = C.CURRENT_BALANCE_50
        mock_read_query.side_effect.append([(current_balance,)])

        with pytest.raises(WithdrawMoreThanBalance):
            await update_wallet_balance(C.VALID_WALLET_ID, withdrawal_amount, C.TOKEN, C.WITHDRAW)
