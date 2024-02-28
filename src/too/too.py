from meeting import Meeting


class Too:
    """
    Class containing information about votes
    """

    def __init__(self, too_table, too_number, too_url, config) -> None:
        self.too_number = too_number
        self.too_url = too_url
        self.__config = config
        self.__decouple_table(too_table)


    def __decouple_table(self, too_table):
        self.headers = self.__get_headers(too_table)

        self.meetings = self.__get_meetings(too_table)

    @staticmethod
    def __get_headers(too_table) -> None:
        headers = too_table.xpath("./table/thead/*/th")

        return [h.text for h in headers]

    def __get_meetings(self, too_table):
        meetings = too_table.xpath("./table/tbody/tr")
        meeting_processed = []
        for meeting in meetings:
            if meeting[0].text.strip() != "":
                meeting_number = meeting[0].text.strip()
            
            meeting_processed.append(
                Meeting(meeting, self.too_number, self.too_url, meeting_number, self.__config)
            )