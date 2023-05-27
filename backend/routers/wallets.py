from fastapi import HTTPException, status, APIRouter, Header, Response
from schemas.wallet_models import NewWallet, WalletSettings
from services.wallets import create, wallet_by_id, all_wallets, delete, set_default_wallet, settings
from services.custom_errors.wallets import BalanceNotNull, NotWalletAdmin, \
    CannotRemoveWalletAdmin, UserAlreadyInGroup

wallets_router = APIRouter(prefix="/users/wallets", tags=["Wallets"])


@wallets_router.post("/")
async def create_wallet(wallet: NewWallet, token: str = Header(alias="Authorization")):
    await create(wallet, token)
    return Response(status_code=status.HTTP_201_CREATED)


@wallets_router.get("")
async def get_all(token: str = Header(alias="Authorization")):
    wallets = await all_wallets(token)
    if not wallets.wallets:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND)
    return wallets


@wallets_router.get("/{wallet_id}")
async def get_by_id(wallet_id: int, token: str = Header(alias="Authorization")):
    wallet = await wallet_by_id(wallet_id, token)
    if not wallet:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND)
    return wallet


@wallets_router.delete("/{wallet_id}")
async def delete_wallet(wallet_id: int, token: str = Header(alias="Authorization")):
    try:
        is_deleted = await delete(wallet_id, token)
        if is_deleted:
            return Response(status_code=status.HTTP_204_NO_CONTENT)
        else:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND)
    except BalanceNotNull:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=BalanceNotNull.error_message)


@wallets_router.patch("/{wallet_id}")
async def make_default_wallet(wallet_id: int, token: str = Header(alias="Authorization")):
    defaulted_wallet = await set_default_wallet(wallet_id, token)
    if not defaulted_wallet:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND)
    return Response(status_code=status.HTTP_200_OK)


@wallets_router.put("/{wallet_id}/settings")
async def wallet_settings(wallet: WalletSettings, wallet_id: int, token: str = Header(alias="Authorization")):
    try:
        set_settings = await settings(wallet, wallet_id, token)
        if not set_settings:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND)
        return Response(status_code=status.HTTP_200_OK)
    except NotWalletAdmin:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail=NotWalletAdmin.error_message)
    except UserAlreadyInGroup:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=UserAlreadyInGroup.error_message)
    except CannotRemoveWalletAdmin:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=CannotRemoveWalletAdmin.error_message)
