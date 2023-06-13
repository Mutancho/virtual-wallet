from datetime import datetime, date

from schemas.referrals import ViewReferrals
from schemas.wallet_models import NewWallet, WalletSettings
from config.config import settings

NEW_PERSONAL_WALLET = NewWallet(type="personal", name="Regular", currency="BGN")
NEW_JOINT_WALLET = NewWallet(type="joint", name="GROUP SAVINGS", currency="BGN")
INVALID_WALLET_TYPE = "Hybrid"
CURRENT_USER_ID = 1
WALLET_CURRENCY_BGN = "BGN"
SUCCESSFUL_WALLET_CREATION = 1
UNSUCCESSFUL_WALLET_CREATION = 0
USER_HAS_WALLET = True
USER_NO_WALLET = False
TOKEN = "dummy_token"
VALID_WALLET_ID = 1
INVALID_WALLET_ID = 99999
OTHER_USER_ID = 2
NEW_WALLET_NAME = "Awesome Wallet"
USER_ID = 123
USERNAME = "example_username"
WALLET_NULL_ACCESS = "null"
ACCESS_LEVEL = "full"
SUCCESSFUL_INSERT_QUERY = 0
WALLET_BALANCE_100 = 100
CURRENT_BALANCE_50 = 50
WITHDRAWAL_AMOUNT = -100
SUCCESSFUL_WALLET_QUERY_RESULT = [
    (1, "Wallet 1", "personal", "USD", 100.0, True, True, "2023-05-25 12:00:00"),
    (2, "Wallet 2", "joint", "EUR", 200.0, False, False, "2023-05-24 10:00:00"),
]

SUCCESSFUL_OWNER_QUERY_RESULT = [("JohnDoe",)]

SUCCESSFUL_GROUP_MEMBERS_RESULT = [
    (1, "User1", "full"),
    (2, "User2", "top_up_only"),
]

UNSUCCESSFUL_WALLET_QUERY_RESULT = []
VALID_USERNAME = "test_user"
INVALID_USERNAME = "invalid_user"
WALLET_SETTINGS = WalletSettings(
    name="New name",
    status=False,
    add_username=VALID_USERNAME,
    remove_username=INVALID_USERNAME,
    change_user_access="full",
    username=VALID_USERNAME
)

WITHDRAW = True
TOP_UP = False
FIRST_QUERY_RESULT = [[0]]
SECOND_QUERY_RESULT = []
THIRD_QUERY_RESULT = [[1]]
TEST_EMAIL = 'test@test.com'
EXPECTED_LINK = f'{settings.base_url}/registrations/2'
QUERY_RESULT_USER_ALREADY_REFERRED = [[1]]


QUERY_RESULT_REFERRALS = [
    (1, "john@example.com", "2023-06-01 10:00:00", "2023-06-08", "example.com/referral1", False),
    (2, "jane@example.com", "2023-06-02 12:00:00", "2023-06-09", "example.com/referral2", True),
    (3, "alex@example.com", "2023-06-03 15:00:00", "2023-06-10", "example.com/referral3", False)
]

EXPECTED_REFERRALS = [
    ViewReferrals(
        id=1,
        email="john@example.com",
        created_at=datetime(2023, 6, 1, 10, 0, 0),
        expiry_date=date(2023, 6, 8),
        link="example.com/referral1",
        is_used=False
    ),
    ViewReferrals(
        id=2,
        email="jane@example.com",
        created_at=datetime(2023, 6, 2, 12, 0, 0),
        expiry_date=date(2023, 6, 9),
        link="example.com/referral2",
        is_used=True
    ),
    ViewReferrals(
        id=3,
        email="alex@example.com",
        created_at=datetime(2023, 6, 3, 15, 0, 0),
        expiry_date=date(2023, 6, 10),
        link="example.com/referral3",
        is_used=False
    )
]

DELETE_RESULT_COUNT = 3
