from playwright.async_api import async_playwright
import psycopg2
from psycopg2.extras import execute_values
import asyncio

website='https://coinmarketcap.com'
list=[]

async def scrape():
    async with async_playwright() as sp:
        browser = await sp.chromium.launch(headless=False)
        page = await browser.new_page()
        await page.goto(website)

        for i in range(5):
            await page.mouse.wheel(0, 2000)
            await page.wait_for_timeout(1000)

        trs_xpath = "//table[@class='sc-7b3ac367-3 etbcea cmc-table']/tbody/tr"
        trs_list = await page.query_selector_all(trs_xpath)

        result_list = []
        for tr in trs_list:
            tr_dict = {}
            tds = await tr.query_selector_all('td')
            tr_dict['id'] = await tds[1].inner_text()
            tr_dict['name'] = await tds[2].inner_text()
            tr_dict['priceUSD'] = await tds[3].inner_text()
            tr_dict['marketCapUSD'] = await tds[7].inner_text()
            result_list.append(tr_dict)
            for r in result_list:
               r['name']= r['name'].split('\n')[0]
       
     
        tuples=[tuple(dic.values()) for dic in list]
        pg_cnx=psycopg2.connect(
            host='',
            database='',
            user='',
            password=''
        )
        pg_cursor=pg_cnx.cursor()
        execute_values(pg_cursor,"INSERT INTO cyptodata (id,name,priceUSD,marketCapUSD) VALUES %s",tuples)
        pg_cnx.commit()
        pg_cnx.close()
        await browser.close()


# Wrapper function to run the async function
def main():
    # Use asyncio to run the scrape function
   asyncio.run(scrape())
    


if __name__ == "__main__":
    main()