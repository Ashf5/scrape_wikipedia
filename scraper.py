import aiohttp 
import asyncio 
from bs4 import BeautifulSoup
from helpers import add_to_database, get_links
import time 
import sqlite3 

class Wiki():
    def __init__(self):
        asyncio.run(self.main())


    def get_links(self):
        """
        Returns a list of up to 500 links that weren't yet downloaded.
        """
        conn = sqlite3.connect("data.db")
        cur = conn.cursor()

        cur.execute("SELECT link FROM wiki WHERE page IS NULL LIMIT 500;")
        fetched = cur.fetchall()
        links = [i[0] for i in fetched]
        return links  


    async def fetch(self, session, url):
        """
        This is an asyncronous function that takes an aiohttp session and a url and returns a tuple of the url and the html of the page.
        """
        print(f"Downloading {url}")
        async with session.get(url) as response:
            text = await response.text()

            return url, text


    async def main(self):
        """
        This function is the main runner for the program, it calls all the other functions.
        """
        start = time.time()
        links = self.get_links()
        if len(links) == 0:
            return None  

        loops = int(len(links) / 20)
        if loops == 0:
            # If there is only one item in the database then this formula will return 0, so set the loops variable to 1.
            loops = 1

        for i in range(loops):
            urls = links[i * 20: i * 20 + 20]



            headers = {
                "user-agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/114.0.0.0 Safari/537.36"
            }
            async with aiohttp.ClientSession(headers=headers) as session:
                tasks = [self.fetch(session, url) for url in urls]
                data = await asyncio.gather(*tasks)

                # TODO add the functions designed for parsing and adding to the database 
                new_links = get_links(data)
                add_to_database(data, new_links)

        print(f" Time: {time.time() - start}")




Wiki()