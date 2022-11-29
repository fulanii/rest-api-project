

from urllib.request import Request, urlopen
from bs4 import BeautifulSoup

class Scaper:
    """A class used to scrape websites """
    
    def __init__(self, url:str = "https://www.scrapethissite.com/pages/simple/"):
        self.url = url

    def make_request(self) -> BeautifulSoup:
        """Make request to the website and return the full site as a bs4 object"""
        req = Request(self.url, headers={'User-Agent': 'Mozilla/5.0'})
        html = urlopen(req).read()
        website = BeautifulSoup(html, "html.parser")

        return website

    def country_info(self):
        soup = self.make_request()
        countries = soup.find_all("div" , class_="col-md-4 country") # number of countries = 250

        country_names = []
        country_capitals = []
        country_populations = []
        country_areas = []

        for country in countries:
            country_name = country.h3.text.strip()
            country_capital = country.find("span", class_="country-capital").text.strip()
            country_population = int(country.find("span", class_="country-population").text.strip())
            country_area = float(country.find("span", class_="country-area").text.strip())

            country_names.append(country_name)
            country_capitals.append(country_capital)
            country_populations.append(country_population)
            country_areas.append(country_area)

        countries = {
            "names": country_names,
            "capitals": country_capitals,
            "populations": country_populations,
            "areas": country_areas
        }

        return countries

