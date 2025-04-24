from telethon import events, Button
from data.config import GIFT_BOT_USERNAME

async def run_claimer(client):
    @client.on(events.NewMessage(from_users=GIFT_BOT_USERNAME))
    async def handler(event):
        if event.buttons:
            for row in event.buttons:
                for button in row:
                    if isinstance(button, Button.inline):
                        if "claim" in button.text.lower() or "gift" in button.text.lower():
                            try:
                                await event.click(button=button)
                                print(f"✅ Claimed gift on {client.session.filename}")
                            except Exception as e:
                                print(f"⚠️ Click failed: {e}")
