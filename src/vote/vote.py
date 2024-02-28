import lxml.html as html
import datetime
import re
import requests

from fake_useragent import UserAgent

class Vote:
    def __init__(
        self,
        vote,
        meeting_number,
        too_number,
        meeting_date,
        config
    ):
        self.__vote = vote
        self.__meeting_number = meeting_number
        self.__too_number = too_number
        self.__meeting_date = meeting_date
        self.__config = config
        self.__ua = UserAgent()
        try:
            print(self.result)
        except:
            print(self.date)
            raise
        # raise


    @property
    def title(self):
        if "_Meeting__title" in dir(self):
            return self.__title

        self.__title = html.tostring(self.__vote[2], encoding='utf-8', method='text').decode('utf-8')
        return self.__title

    @property
    def date(self):
        if "_Meeting__date" in dir(self):
            return self.__date

        d = self.__vote[1].text
        d = f"{self.__meeting_date.strftime('%Y-%m-%d')} {d}"
        self.__date = datetime.datetime.strptime(d, "%Y-%m-%d %H:%M:%S")

        return self.__date

    @property
    def __voters_page(self):
        if "_Meeting__vote_page" in dir(self):
            return self.__vote_page

        endpoint = self.__vote[0].xpath('./a')[0].attrib['href']
        headers={"User-Agent": self.__ua.random}
        r = requests.get(f"{self.__config.gov_url}/{endpoint}", headers=headers)
        self.__vote_page = html.fromstring(r.text)
        return self.__vote_page

    @property
    def result(self):
        if "_Meeting__result" in dir(self):
            return self.__result
        if votes := self.__voters_page.xpath("//*/div[@class='sub-title']/center/p"):
            votes=votes[0]
            regexp = (
                r"Głosowało-(?P<voters>\d+)posłów"
                r"(?:Za-(?P<for>\d+))"
                r"(?:Przeciw-(?P<against>\d+))"
                r"(?:Wstrzymałosię-(?P<abstained>[0-9]+))"
                r"(?:Niegłosowało-(?P<no_vote>\d+))"
                r"(?:(?:Większośćbezwzględna|Większość3/5ustawowa)-(?P<majority>\d+))?"
            )
        elif votes := self.__voters_page.xpath("//*/div[@class='sub-title']")[0]:
            candidates=votes.xpath('./div[@style="padding-left:40px;"]')[0]
            candidates_str = html.tostring(
                candidates, encoding='utf-8', method='text'
            ).decode('utf-8')
            print(candidates_str)
            votes.remove(candidates)
            candidates_regex = (
                r"(?:([AaĄąBbCcĆćDdEeĘęFfGgHhIiJjKkLlŁłMmNnŃńOoÓóPpRrSsŚśTtUuWwYyZzŹźŻż ]+)"
                r" - (\d+))"
            )
            print(self.date)
            print(re.findall(candidates_regex, candidates_str))

            regexp = (
                r".*Głosowało-(?P<voters>\d+)posłów,"
                r"(?:Większośćbezwzględna|Większość3/5ustawowa)-(?P<majority>\d+)"
                r".*(?:(?P<against>\d+)(?:-|)(?:poseł|posłów)(?:zagłosował|zagłosowało)przeciwkowszystkimkandydatom)"
            )
        v =  html.tostring(votes, encoding='utf-8', method='text').decode('utf-8')

        v = "".join(v.split())
        print(v)
        r = re.match(regexp, v)
        return r.groups()



