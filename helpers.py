from bs4 import BeautifulSoup
import sqlite3
from urllib import parse



def get_links(p_list):
    """
    This function takes in the list of tuples returned by the fetch / main function and returns a set with all the links to other wikipedia pages it finds.
    """
    print("parsing......")
    new_links = set()
    for page in p_list:
        soup = BeautifulSoup(page[1], "html.parser")
        links = soup.find_all("a")
        li = []
        for link in links:
            if "title" in link.attrs and "class" not in link.attrs and "[" not in link.text:
                url = link.get("href")
                if ":" not in url and not url.startswith("http"):
                    url = parse.urljoin(page[0], url)
                    li.append(url)
        new_links.update(li)

    return new_links


def add_to_database(pages, links):
    print("Inserting into database.....")
    conn = sqlite3.connect("data.db")
    cur = conn.cursor()

    # Add the links 
    count = 0 
    for link in links:
        cur.execute("INSERT OR IGNORE INTO wiki (link) VALUES (?)", (link,))
        count += 1 
        if count == 100:
            conn.commit()
            count = 0
    conn.commit()

    for page in pages:
        cur.execute("UPDATE wiki SET page = ? WHERE link = ?", (page[1], page[0]))
    conn.commit()