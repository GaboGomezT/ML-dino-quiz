import scrapy
import requests
from bs4 import BeautifulSoup
import pandas as pd
import json

from scrapy.crawler import CrawlerProcess


class DinoScraper(scrapy.Spider):
    name = "DinoScraper"

    def start_requests(self):
        global dino_query
        yield scrapy.Request(
            url=f"https://www.nhm.ac.uk/discover/dino-directory/{dino_query}.html",
            callback=self.parse_pagination,
        )

    def parse_pagination(self, response):
        global dino_url
        image_url = response.css("img.dinosaur--image::attr(src)").extract_first()
        dino_url = image_url


async def get_dino_url(dino_name: str) -> dict:
    page = requests.get(
        f"https://www.nhm.ac.uk/discover/dino-directory/{dino_name}.html"
    )
    soup = BeautifulSoup(page.content, "html.parser")
    image = soup.find_all("img", class_="dinosaur--image")[0]
    print(image)
    return image["src"]


def get_all_dino_names() -> list:
    dino_df = pd.read_csv("data.csv")
    return dino_df.name.to_list()


async def create_dino_file(dino_names: list):
    dino_dict = {}
    for dino in dino_names:
        dino_dict[dino] = await get_dino_url(dino)

    with open("dino.json", "w") as outfile:
        json.dump(dino_dict, outfile)


if __name__ == "__main__":
    dino_names = get_all_dino_names()
    create_dino_file(dino_names)
