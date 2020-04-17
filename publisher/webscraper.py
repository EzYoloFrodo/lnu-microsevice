import pika
import asyncio
from pyppeteer import launch
from publisher import send_message
from publisher import close_connection
import os
import time
import json


async def main():

    browser = await launch(headless=True,
                           executablePath="/usr/bin/chromium-browser",
                           args=['--no-sandbox', '--disable-gpu'])
    page = await browser.newPage()
    await page.goto('https://zaxid.net/')

    elements = await page.querySelectorAll('a')

    links = []
    for element in elements:
        link = await page.evaluate('(element) => element.href', element)
        try:
            if len(link.split('/')) == 4 and link[-1].isdigit():
                print(link)
                links.append(link)
        except IndexError:
            pass

    print(len(links))
    link_page = await browser.newPage()

    for link in links:
        print(link)
        try:
            await link_page.goto(link)
            element = await link_page.querySelector('#newsName')
            title = await link_page.evaluate('(element) => element.textContent', element)
            print(title)

            element = await link_page.querySelector('#newsSummary')
            text = await link_page.evaluate('(element) => element.innerText', element)
            print(text)

            element = await link_page.querySelector('#author_name')
            try:
                author_name = await link_page.evaluate('(element) => element.innerText', element)
                print(author_name)
            except Exception:
                author_name = "None"

            data_to_send = {"link": link,
                            "title": title,
                            "text": text,
                            "author_name": author_name}

            send_message(json.dumps(data_to_send))
            time.sleep(10)
        except Exception as e:
            browser = await launch(headless=True,
                                   executablePath="/usr/bin/chromium-browser",
                                   args=['--no-sandbox', '--disable-gpu'])
            link_page = await browser.newPage()
            print(e)
            pass

    await browser.close()

asyncio.get_event_loop().run_until_complete(main())
