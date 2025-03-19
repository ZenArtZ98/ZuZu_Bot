from telethon import TelegramClient, events, Button
import pandas as pd
import sqlite3
import os
import requests
import re
from parsel import Selector

api_id = 22091115
api_hash = 'ad61ed7590068f7c6c07ff13e1a3f006'
bot_token = '7750357166:AAFPdHY24FbLB_FsecOLllTYGC_6xX4h3gM'

client = TelegramClient('bot', api_id, api_hash)


def init_db():
    conn = sqlite3.connect('sites.db')
    c = conn.cursor()
    c.execute('''CREATE TABLE IF NOT EXISTS sites 
                 (title TEXT, url TEXT, xpath TEXT)''')
    conn.commit()
    conn.close()


@client.on(events.NewMessage(pattern='/start'))
async def start(event):
    await event.respond(
        "Привет! Нажми кнопку ниже, чтобы загрузить Excel-файл с сайтами.",
        buttons=[Button.inline("Загрузить файл", b"upload")]
    )


@client.on(events.CallbackQuery(data=b"upload"))
async def handle_upload_button(event):
    await event.respond("Пожалуйста, прикрепите Excel-файл с колонками: title, url, xpath")


@client.on(events.NewMessage(incoming=True))
async def handle_file(event):
    if event.message.document and event.message.document.mime_type in [
        'application/vnd.openxmlformats-officedocument.spreadsheetml.sheet', 'application/vnd.ms-excel']:
        try:
            file_path = await event.message.download_media(
                file=f"uploads/{event.message.document.attributes[0].file_name}")
            os.makedirs('uploads', exist_ok=True)

            df = pd.read_excel(file_path)
            required_columns = ['title', 'url', 'xpath']

            if not all(col in df.columns for col in required_columns):
                await event.respond("Ошибка: файл должен содержать колонки title, url, xpath")
                return

            response = "Содержимое файла:\n\n"
            for index, row in df.iterrows():
                response += f"Title: {row['title']}\nURL: {row['url']}\nXPath: {row['xpath']}\n\n"
            await event.respond(response)

            conn = sqlite3.connect('sites.db')
            df.to_sql('sites', conn, if_exists='append', index=False)
            conn.close()

            prices_by_site = await parse_prices(df)
            price_response = "Средние цены зюзюбликов:\n\n"
            for title, avg_price in prices_by_site.items():
                price_response += f"{title}: {avg_price:.2f} руб.\n"
            await event.respond(price_response)

        except Exception as e:
            await event.respond(f"Произошла ошибка: {str(e)}")
    else:
        if event.message.text != '/start':
            await event.respond("Пожалуйста, отправьте Excel-файл после нажатия кнопки.")


async def parse_prices(df):
    prices_by_site = {}

    for index, row in df.iterrows():
        try:
            response = requests.get(row['url'])
            selector = Selector(text=response.text)
            price_elements = selector.xpath(row['xpath']).getall()

            prices = []
            for price_text in price_elements:
                price_text = price_text.strip()
                price_clean = re.sub(r'[^\d.,]', '', price_text)
                price_clean = price_clean.replace(',', '.')
                if price_clean:
                    prices.append(float(price_clean))

            if prices:
                avg_price = sum(prices) / len(prices)
                prices_by_site[row['title']] = avg_price

        except Exception as e:
            print(f"Ошибка при парсинге {row['url']}: {str(e)}")

    return prices_by_site


async def main():
    init_db()
    await client.start(bot_token=bot_token)
    print("Бот запущен!")
    await client.run_until_disconnected()


if __name__ == '__main__':
    with client:
        client.loop.run_until_complete(main())