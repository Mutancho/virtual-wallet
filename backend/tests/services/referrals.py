import pytest
from unittest.mock import patch, AsyncMock
from schemas.referrals import Referral
from services.custom_errors.referrals import UserHasBeenReferredAlready
from services.custom_errors.users import AdminAccessRequired
from services.referrals import create_referral_link, view, delete
import tests.constants as C


class TestCreateShould:
    @pytest.mark.asyncio
    @patch('services.referrals.read_query', new_callable=AsyncMock)
    @patch('services.referrals.get_current_user')
    @patch('services.referrals.insert_query', new_callable=AsyncMock)
    @patch('services.referrals.send_email', new_callable=AsyncMock)
    async def test_successful(self, mock_send_email, mock_insert_query, mock_get_current_user, mock_read_query):
        mock_read_query.side_effect = [
            C.FIRST_QUERY_RESULT,
            C.SECOND_QUERY_RESULT,
            C.THIRD_QUERY_RESULT
        ]
        mock_get_current_user.return_value = C.USER_ID
        mock_insert_query.return_value = None
        mock_send_email.return_value = None

        referral = Referral(email=C.TEST_EMAIL)

        result = await create_referral_link(referral, C.TOKEN)

        assert result == C.EXPECTED_LINK
        mock_get_current_user.assert_called_once_with(C.TOKEN)
        assert mock_read_query.call_count == 3
        mock_insert_query.assert_called_once()
        mock_send_email.assert_called_once()

    @pytest.mark.asyncio
    @patch('services.referrals.read_query', new_callable=AsyncMock)
    @patch('services.referrals.get_current_user')
    async def test_unsuccessful(self, mock_get_current_user, mock_read_query):
        mock_read_query.return_value = C.QUERY_RESULT_USER_ALREADY_REFERRED
        mock_get_current_user.return_value = C.USER_ID

        referral = Referral(email=C.TEST_EMAIL)

        with pytest.raises(UserHasBeenReferredAlready):
            await create_referral_link(referral, C.TOKEN)


class TestViewShould:
    @pytest.mark.asyncio
    @patch('services.referrals.get_current_user')
    @patch('services.referrals.read_query', new_callable=AsyncMock)
    async def test_view_referrals(self, mock_read_query, mock_get_current_user):
        mock_get_current_user.return_value = C.USER_ID
        mock_read_query.return_value = C.QUERY_RESULT_REFERRALS

        token = C.TOKEN
        result = await view(token)

        assert result == C.EXPECTED_REFERRALS


class TestDeleteShould:
    @pytest.mark.asyncio
    @patch('services.referrals.is_admin', new_callable=AsyncMock)
    @patch('services.referrals.update_query', new_callable=AsyncMock)
    async def test_delete_referrals(self, mock_update_query, mock_is_admin):
        mock_is_admin.return_value = True
        mock_update_query.return_value = C.DELETE_RESULT_COUNT

        token = C.TOKEN
        result = await delete(token)

        assert result == C.DELETE_RESULT_COUNT

    @pytest.mark.asyncio
    @patch('services.referrals.is_admin', new_callable=AsyncMock)
    async def test_delete_referrals_admin_access_required(self, mock_is_admin):
        mock_is_admin.return_value = False

        token = C.TOKEN
        with pytest.raises(AdminAccessRequired):
            await delete(token)
        mock_is_admin.assert_called_once_with(token)
