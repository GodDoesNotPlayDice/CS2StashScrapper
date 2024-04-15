import asyncio, os, time
from playwright.async_api import async_playwright
from playwright_stealth import stealth_async

base_market_url = "https://steamcommunity.com/market/"
cs2_url = "search?appid=730"

test_url = "https://steamcommunity.com/market/listings/730/M4A4%20%7C%20Hellfire%20%28Factory%20New%29"


async def main():
    async with async_playwright() as p:
        print('Launching browser...')
        browser = await p.firefox.launch()
        page = await browser.new_page()
        await stealth_async(page)
        print("Browser launched.")
        print("Loading Market")
        await page.goto(test_url, timeout=80000)
        get_canvas_div = await page.query_selector('div.jqplot-target')
        # need get the canvas content jqplot-series-canvas
        canvas = await get_canvas_div.query_selector('canvas.jqplot-series-canvas')
        await canvas.screenshot(path='test.png')
        await browser.close()
        
asyncio.run(main())