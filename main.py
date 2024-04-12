import asyncio, os, time
from playwright.async_api import async_playwright
from playwright_stealth import stealth_async

async def main():
    async with async_playwright() as p:
        print('Launching browser...')
        browser = await p.firefox.launch()
        page = await browser.new_page()
        await stealth_async(page)
        await page.goto('view-source:https://csgostash.com/')
        await page.screenshot(path='example.png')
        await browser.close()

asyncio.run(main())

        

