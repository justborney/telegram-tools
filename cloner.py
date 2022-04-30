import asyncio
from telethon import TelegramClient, events, errors
from config import API_ID, API_HASH, session

INPUT_CHANNEL = "testdonor112"
OUTPUT_CHANNEL = "testtarget11"

ignored_keys = ["биткоин", "nft", "донат", "ставки", "казино"]
message_text = "измененный текст"

with TelegramClient(session, API_ID, API_HASH) as client:
    print("telethon started")


    @client.on(events.NewMessage(INPUT_CHANNEL))
    async def new_message(event):
        if not event.grouped_id and not event.message.forward:
            try:
                await client.send_message(
                    entity=OUTPUT_CHANNEL,
                    file=event.message.media,
                    parse_mode="md",
                    link_preview=False,
                )
            except errors.FloodWaitError as e:
                print(f"FloodWaitError: {e.seconds} sec remaining")
                await asyncio.sleep(e.seconds)
            except Exception as e:
                print(f"Error: {e}")
        elif event.message.text and not event.message.media and not event.grouped_id:
            try:
                await client.send_message(
                    entity=OUTPUT_CHANNEL,
                    text=message_text,
                    parse_mode="md",
                    link_preview=False,
                )
            except errors.FloodWaitError as e:
                print(f"FloodWaitError: {e.seconds} sec remaining")
                await asyncio.sleep(e.seconds)
            except Exception as e:
                print(f"Error: {e}")
        elif event.message.forward:
            try:
                await event.message.forward_to(OUTPUT_CHANNEL)
            except errors.FloodWaitError as e:
                print(f"FloodWaitError: {e.seconds} sec remaining")
                await asyncio.sleep(e.seconds)
            except Exception as e:
                print(f"Error: {e}")


    @client.on(events.Album(INPUT_CHANNEL))
    async def new_album(event):
        raw_text = event.original_update
        print(raw_text)
        try:
            await client.send_message(
                entity=OUTPUT_CHANNEL,
                file=event.messages,
                message=raw_text,
                parse_mode="md",
                link_preview=False,
            )
        except errors.FloodWaitError as e:
            print(f"FloodWaitError: {e.seconds} sec remaining")
            await asyncio.sleep(e.seconds)
        except Exception as e:
            print(f"Error: {e}")


    client.run_until_disconnected()
