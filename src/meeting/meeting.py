import lxml.html as html
import datetime
import babel.dates
import requests
from fake_useragent import UserAgent
from vote import Vote

months = {
    "styczeń": "1",
    "luty": "2",
    "marzec": "3",
    "kwiecień": "4",
    "maj": "5",
    "czerwiec": "6",
    "lipiec": "7",
    "sierpień": "8",
    "wrzesień": "9",
    "październik": "10",
    "listopad": "11",
    "grudzień": "12",
    "stycznia": "1",
    "lutego": "2",
    "marca": "3",
    "kwietnia": "4",
    "maja": "5",
    "czerwca": "6",
    "lipca": "7",
    "sierpnia": "8",
    "września": "9",
    "października": "10",
    "listopada": "11",
    "grudnia": "12"
}

class Meeting:
    def __init__(self, meeting, too_number, too_url, meeting_number, config):
        self.__too_url = too_url
        self.__too_number = too_number
        self.__config = config
        self.meeting_number = meeting_number
        self.__meeting = meeting
        self.__gov_url = f"{config.gov_url}?{config.gov_url_vote_endpoint}"
        self.__ua = UserAgent()
        self.votings

    @property
    def votings(self):
        if "_Meeting__votings" in dir(self):
            return self.__votings

        self.__votings = []

        vote_url = self.__meeting.xpath("./*/a")[0].attrib['href']
        headers={"User-Agent": self.__ua.random}
        r = requests.get(f"{self.__config.gov_url}/{vote_url}", headers=headers)
        vote_table = html.fromstring(r.text)
        table = vote_table.xpath(
            "//*/div[@id='contentBody']"
            "/div[@id='view:_id1:_id2:facetMain']"
            "/div[@id='view:_id1:_id2:facetMain:agentHTML']/*/tbody"
        )[0]
        for vote in table:
            self.__votings.append(
                Vote(
                    vote,
                    self.meeting_number,
                    self.__too_number,
                    self.date,
                    self.__config
                )
            )


    @property
    def date(self):
        if "_Meeting__date" in dir(self):
            return self.__date
        date = self.__meeting.xpath("./*/a")[0]
        d = date.text.split(" ")
        d[1] = months[d[1]]
        self.__date = babel.dates.parse_date(" ".join(d), locale='pl_PL')
        return self.__date