from stripe import PaymentMethod, PaymentIntent, Customer
import stripe
from config.config import settings
from utils.oauth2 import get_current_user
from database.database_queries import read_query, manage_db_transaction
from decimal import Decimal
from asyncmy.connection import Connection

stripe.api_key = settings.stripe_secret_key


async def create_customer(email: str, user_id: str, first_name: str, last_name: str):
    full_name = f"{first_name} {last_name}"
    customer = Customer.create(email=email,
                               name=full_name,
                               metadata={'user_id': user_id})
    return customer.id


@manage_db_transaction
async def attach_payment_method(conn: Connection, payment_method_id: str, token: str) -> PaymentMethod:
    customer_id = get_stripe_id(conn, token)
    return PaymentMethod.attach(payment_method_id, customer=customer_id)


async def detach_payment_method(payment_method_id: str) -> PaymentMethod:
    return PaymentMethod.detach(payment_method_id)


@manage_db_transaction
async def list_payment_methods(conn: Connection, token: str) -> list[PaymentMethod]:
    customer_id = get_stripe_id(conn, token)
    return PaymentMethod.list(customer=customer_id, type='card')


@manage_db_transaction
async def create_payment_intent(conn: Connection, amount: str, payment_method_id: str, currency: str,
                                token: str) -> PaymentIntent:
    user_id = get_current_user(token)
    amount_decimal = Decimal(amount)
    amount_in_cents = int(amount_decimal * 100)
    stripe_customer_id = await read_query(conn, "SELECT stripe_id from users WHERE id = %s", (user_id,))
    payment_intent = PaymentIntent.create(
        amount=amount_in_cents,
        currency=currency.lower(),
        description="Wallet - " + currency.upper(),
        payment_method=payment_method_id,
        customer=stripe_customer_id[0][0],
        confirm=True,
    )
    return payment_intent


async def get_stripe_id(conn: Connection, token: str):
    user_id = get_current_user(token)
    stripe_id = await read_query(conn, "SELECT stripe_id FROM users WHERE id=%s", (user_id,))
    if not stripe_id:
        return None
    return stripe_id[0][0]
