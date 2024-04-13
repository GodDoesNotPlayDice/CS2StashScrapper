import asyncio, os, time
from playwright.async_api import async_playwright
from playwright_stealth import stealth_async

base_market_url = "https://steamcommunity.com/market/"

cs2_url = "search?appid=730"
cases_url = "search?q=&category_730_ItemSet%5B%5D=any&category_730_ProPlayer%5B%5D=any&category_730_StickerCapsule%5B%5D=any&category_730_Tournament%5B%5D=any&category_730_TournamentTeam%5B%5D=any&category_730_Type%5B%5D=tag_CSGO_Type_WeaponCase&category_730_Weapon%5B%5D=any&appid=730"


async def main():
    min_pages = 1
    max_pages = 0
    
    
    async with async_playwright() as p:
        print('Launching browser...')
        browser = await p.firefox.launch()
        page = await browser.new_page()
        await stealth_async(page)
        print("Browser launched.")
        print("Loading Market")
        await page.goto(base_market_url + cases_url + "#p1_price_asc", timeout=80000)
        print("Market loaded.")
        print("Getting pages")
        while True:
            try:
                pages_id_div = await page.query_selector('#searchResults_controls')
                pages_id_items = await pages_id_div.query_selector('#searchResults_links')
                pages_id = await pages_id_items.query_selector_all('.market_paging_pagelink')
                last_item_list = [i for i in pages_id if i == pages_id[-1]]
                last_item = await last_item_list[0].inner_text()
                max_pages = int(last_item)
                break
            except IndexError:
                print("Failed to get pages, retrying...")
                await page.reload()
            except Exception as e:
                print("Failed to get pages, retrying...")
                print(e)
                await page.reload()
                
        print("Getting items")
        while min_pages <= max_pages:
            while True:
                await page.screenshot(path='screenshot.png')
                items = await page.query_selector_all('.market_listing_row_link')
                if len(items) < 1:
                    print("Failed to get items, retrying...")
                    await page.reload()
                else:
                    break
            for item in items:
                item_name = await item.query_selector('span.market_listing_item_name')
                print(await item_name.inner_text())
                
            print("Changing page")    
            await page.goto(base_market_url + cases_url + "#p" + str(min_pages) + "_price_asc", timeout=80000)
            min_pages += 1
            
        await browser.close()

asyncio.run(main())

        

