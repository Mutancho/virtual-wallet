from schemas.wallet_models import NewWallet, WalletSettings

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
