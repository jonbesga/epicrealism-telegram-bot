from telegram import Update
from telegram.ext import CallbackContext
from telegram.constants import ParseMode
from datetime import datetime
from . import replicate_wrapper as replicate
from . import billing
from . import db

async def get_user_balance(telegram_user_id: str):
    async with db.async_session() as session:
        async with session.begin():
            topups = await db.get_user_topups(session, telegram_user_id)
            if len(topups) == 0:
                return 0

            usage_history = await db.get_user_usage_history(session, telegram_user_id)
            total_topups_in_seconds = sum(map(lambda t: t.amount, topups)) # Make it with the DB
            total_usage_in_seconds = sum(map(lambda u: u.predict_time, usage_history)) # Make it with the DB
            return total_topups_in_seconds - total_usage_in_seconds


async def user_has_credits(telegram_user_id: str) -> bool:
    async with db.async_session() as session:
        async with session.begin():
            topups = await db.get_user_topups(session, telegram_user_id)
            if len(topups) == 0:
                return False

            usage_history = await db.get_user_usage_history(session, telegram_user_id)
            total_topups_in_seconds = sum(map(lambda t: t.amount, topups)) # Make it with the DB
            total_usage_in_seconds = sum(map(lambda u: u.predict_time, usage_history)) # Make it with the DB
            print(total_usage_in_seconds, total_topups_in_seconds, total_usage_in_seconds < total_topups_in_seconds)
            return total_usage_in_seconds < total_topups_in_seconds

async def add_usage_to_user(telegram_user_id: str, predict_time, prediction_id):
    async with db.async_session() as session:
        async with session.begin():
            await db.insert_usage(session, telegram_user_id, predict_time, prediction_id, datetime.now())


async def imagine_handler(update: Update, _: CallbackContext):
    telegram_user_id = str(update.message.from_user.id)
    prompt = update.message.text.removeprefix("/imagine").removeprefix("/i").strip()
    
    if not await user_has_credits(telegram_user_id):
        await update.message.reply_text("You have used all your credits! 😔 To buy more use /topup", quote=True)
        return

    processing_message = await update.message.reply_text("⏳ AI is dreaming...", quote=True)
    # prediction = FakePrediction("fake-id", {"predict_time": round(random.random() * 10, 2)})
    prediction = replicate.run_replicate(prompt)
    
    prediction_time = prediction.metrics['predict_time']
    
    await add_usage_to_user(telegram_user_id, prediction_time, prediction.id)

    await update.message.chat.send_photo(
        prediction.output,
        caption=f"{prompt} | Credits used: {round(prediction_time, 2)}",
        reply_to_message_id=update.message.id
    )
    await processing_message.delete()


async def topup10_handler(update: Update, _: CallbackContext):
    telegram_user_id = str(update.message.from_user.id)
    
    payment_url = billing.create_checkout_session(telegram_user_id)

    await update.message.reply_text(
        f"""To get more credits use the [following link]({payment_url})""",
        quote=True,
        parse_mode='MarkdownV2')

async def topup5_handler(update: Update, _: CallbackContext):
    telegram_user_id = str(update.message.from_user.id)
    
    payment_url = billing.create_checkout_session(telegram_user_id, price=5)

    await update.message.reply_text(
        f"""To get more credits use the [following link]({payment_url})""",
        quote=True,
        parse_mode='MarkdownV2')

async def topup1_handler(update: Update, _: CallbackContext):
    telegram_user_id = str(update.message.from_user.id)
    
    payment_url = billing.create_checkout_session(telegram_user_id, price=1)

    await update.message.reply_text(
        f"""To get more credits use the [following link]({payment_url})""",
        quote=True,
        parse_mode='MarkdownV2')

async def credits_handler(update: Update, _: CallbackContext):
    telegram_user_id = str(update.message.from_user.id)
    
    balance = await get_user_balance(telegram_user_id)

    await update.message.reply_text(f"""You have {round(balance, 2)} credits.""", quote=True)

async def start_handler(update: Update, _: CallbackContext):
    await update.message.reply_text("""
Hi\! I'm a bot similar to Midjourney but for Telegram\. I'm very easy to use:

• Use `/imagine prompt` or `/i prompt` to generate images\.
• Use `/topup` or `/t` to get a link to buy 2,000 credits\.
• Use `/topup5` or `/t5` to get a link to buy 1,000 credits\.
• Use `/topup1` or `/t1` to get a link to buy 200 credits\.
• Use `/credits` or `/c` to see how many credits you have left\.

One /topup is $10 and will give you 2,000 credits\.
One /topup5 is $5 and will give you 1,000 credits\.
One /topup1 is $1 and will give you 200 credits\.

On average, images usually costs 5 credits, so you can get approximately 400 images\.

Enjoy\!
""", quote=True, parse_mode=ParseMode.MARKDOWN_V2)

async def whoami_handler(update: Update, _: CallbackContext):
    await update.message.reply_text(update.message.from_user.id, quote=True)
