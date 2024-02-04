import os
import stripe

from flask import Flask, jsonify, request, Response
from asgiref.wsgi import WsgiToAsgi
from . import db
from datetime import datetime
from telegram.ext import Application

TELEGRAM_BOT_TOKEN = os.getenv("TELEGRAM_BOT_TOKEN")

PRICE_PER_SECOND = 0.0050 # Original is 0.0023


# The library needs to be configured with your account's secret key.
# Ensure the key is kept out of any version control system you might be using.
stripe.api_key = os.getenv("STRIPE_API_KEY")

# This is your Stripe CLI webhook secret for testing your endpoint locally.
endpoint_secret = os.getenv("STRIPE_SIGNING_SECRET")

app = Flask(__name__)

asgi_app = WsgiToAsgi(app)

application = Application.builder().token(TELEGRAM_BOT_TOKEN).build()

async def fulfill_order(session):
    if "client_reference_id" not in session:
        return Response(status=500)

    amount_total_in_cents = session["amount_total"]
    amount_total_in_dollars = amount_total_in_cents / 100
    telegram_user_id = session["client_reference_id"]
    credits = amount_total_in_dollars / PRICE_PER_SECOND
    async with db.async_session() as session:
        async with session.begin():
            await db.add_credits_to_telegram_user(session, telegram_user_id, credits, datetime.now())
            await application.bot.send_message(telegram_user_id, f"Thanks for your purchase!. {credits} credits have been added to your balance.")
            return Response(status=200)

@app.route('/ping', methods=['GET'])
async def ping():
    return Response("pong", status=200)

@app.route('/webhook', methods=['POST'])
async def webhook():
    event = None
    payload = request.data
    sig_header = request.headers['STRIPE_SIGNATURE']

    try:
        event = stripe.Webhook.construct_event(
            payload, sig_header, endpoint_secret
        )
    except (ValueError, stripe.error.SignatureVerificationError) as e:
        raise e
    
    if event['type'] == 'checkout.session.completed':
        session = event['data']['object']
        if session.payment_status == "paid":
            await fulfill_order(session)
            
    elif event['type'] == 'checkout.session.async_payment_succeeded':
        session = event['data']['object']
        await fulfill_order(session)
    else:
        print('Unhandled event type {}'.format(event['type']))

    return jsonify(success=True)