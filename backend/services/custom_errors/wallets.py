class BalanceNotNull(Exception):
    error_message = "Wallet still holds cash, needs to be empty before removed!"


class NotWalletAdmin(Exception):
    error_message = "You are not the admin of the wallet!"


class CannotRemoveWalletAdmin(Exception):
    error_message = "Cannot remove wallet admin!"


class UserAlreadyInGroup(Exception):
    error_message = "User already in group!"


class WithdrawMoreThanBalance(Exception):
    error_message = "Cannot withdraw more than current balance!"


class NoWithdrawalAccess(Exception):
    error_message = "No withdrawal access for group wallet!"


class NoTopUpAccess(Exception):
    error_message = "No top-up access!"
