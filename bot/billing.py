import stripe
import os

stripe.api_key = os.getenv("STRIPE_API_KEY")

PRICE_10 = os.getenv("STRIPE_PRODUCT_PRICE_10")
PRICE_5 = os.getenv("STRIPE_PRODUCT_PRICE_5")
PRICE_1 = os.getenv("STRIPE_PRODUCT_PRICE_1")

def create_checkout_session(telegram_user_id, price=10):    
    if price == 5:
        price = PRICE_5
    elif price == 1:
        price = PRICE_1
    else:
        price = PRICE_10

    checkout_session = stripe.checkout.Session.create(
        success_url="https://babelgram.app/success",
        client_reference_id=telegram_user_id,
        line_items=[
            {
            "price": price,
            "quantity": 1,
            },
        ],
        mode="payment",
    )
    return checkout_session.url