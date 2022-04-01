import scrapy


class UfcFightSpider(scrapy.Spider):
    name = "ufc_fight"
    # response.css("table.b-fight-details__table tbody tr::attr(data-link)").getall()
    #response.css("table.b-statistics__table-events tbody tr.b-statistics__table-row i.b-statistics__table-content a::attr(href)").getall()
    start_urls = [
        'http://ufcstats.com/statistics/events/completed?page=all'
    ]

    def parse(self, response):
        fight_event_links = response.css(
            "table.b-statistics__table-events tbody tr.b-statistics__table-row i.b-statistics__table-content a::attr(href)").getall()
        yield from response.follow_all(fight_event_links, self.parse_fight_events)

    def parse_fight_events(self, response):
        fight_links = response.css(
            "table.b-fight-details__table tbody tr::attr(data-link)").getall()
        yield from response.follow_all(fight_links, self.parse_fight_events)

    def parse_fight_event(self, response):
        page = response.url.split("/")[-2]
        filename = f'fights-{page}.html'
        with open(filename, 'wb') as f:
            f.write(response.body)
        self.log(f'Saved file {filename}')


# -> returns fighter names response.css("section.b-fight-details__section table tbody td.b-fight-details__table-col p.b-fight-details__table-text a::text").getall()
# returns fighter stats -> response.css("section.b-fight-details__section table tbody td.b-fight-details__table-col p.b-fight-details__table-text::text").getall()
# will need to do the following things ->
# 1. strip the strings -> stripped_list = list(map(str.strip,test_list))
# 2. remove empty string and --- from list ->
##while '---' in stripped_list:stripped_list.remove('---')
# >>> while "" in stripped_list: stripped_list.remove("")