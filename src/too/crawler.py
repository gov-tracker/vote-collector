from __future__ import annotations
from typing import AnyStr

from fake_useragent import UserAgent
import requests
import lxml.html as html

from too import Too

class GovTooCrawler:
    def __init__(self, config: Config) -> None:
        self.__config = config
        self.__gov_url = f"{config.gov_url}/agent.xsp?{config.gov_url_vote_endpoint}"
        self.__ua = UserAgent()

    def __iter__(self):
        """
        Iter over Govermetent Terms Of Office
        """
        self.too_number = 6
        return self

    def __next__(self):
        self.too_number += 1
        too = self.__get_too()
        if not too:
            raise StopIteration

        return too

    def __get_too(self) -> None:
        """
        Get meetings that took place durint given TOO
        """
        too = self.__get_too_page()

        meeting_table = too.xpath(
            "//*/div[@id='contentBody']"
            "/div[@id='view:_id1:_id2:facetMain']"
            "/div[@id='view:_id1:_id2:facetMain:agentHTML']"
        )[0]
        if (
            not len(meeting_table)
            or meeting_table[0].text == "Brak danych"
        ):
            return None

        return Too(meeting_table, self.too_number, self.too_url, self.__config)

    @property
    def too_url(self) -> AnyStr:
        return f"{self.__gov_url}&{self.__config.gov_too_endpoint}={self.too_number}"

    def __get_too_page(self) -> html.HtmlElement:
        print(f"Scanning url: {self.too_url}")
        headers={"User-Agent": self.__ua.random}
        r = requests.get(self.too_url, headers=headers)
        root = html.fromstring(r.text)
        return root