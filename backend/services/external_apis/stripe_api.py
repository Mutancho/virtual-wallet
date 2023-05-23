from stripe import PaymentMethod, PaymentIntent, Customer
import stripe
from asyncio import to_thread
from config.config import settings
from utils.oauth2 import get_current_user
from database.database_queries import read_query

stripe.api_key = settings.stripe_secret_key


async def create_customer(email: str, user_id: str, first_name: str, last_name: str):
    full_name = f"{first_name} {last_name}"
    customer = Customer.create(email=email,
                               name=full_name,
                               metadata={'user_id': user_id})
    return customer


async def attach_payment_method(payment_method_id: str, customer_id: str) -> PaymentMethod:
    return PaymentMethod.attach(payment_method_id, customer=customer_id)


async def list_payment_methods(customer_id: str) -> list[PaymentMethod]:
    return PaymentMethod.list(customer=customer_id, type='card')

async def detach_payment_method(payment_method_id: str) -> PaymentMethod:
    return await PaymentMethod.detach(payment_method_id)


# todo add constants for wallet descriptions
async def create_payment_intent(amount: int, payment_method_id: str) -> PaymentIntent:
    payment_intent = PaymentIntent.create(
        amount=amount * 100,
        currency="usd",
        description="Wallet - BGN",
        payment_method=payment_method_id,
        confirm=True,
    )
    return payment_intent


async def get_stripe_id(token: str):
    user_id = get_current_user(token)
    stripe_id = await read_query("SELECT stripe_id FROM users WHERE id=%s", (user_id,))
    if not stripe_id:
        return None
    return stripe_id[0][0]