import scrapy
import requests
import re
import urllib


class ActivePrincipalItem(scrapy.item.Item):
    url = scrapy.item.Field()
    country_name = scrapy.item.Field()
    state = scrapy.item.Field()
    registration_date = scrapy.item.Field()
    registration_number = scrapy.item.Field()
    registration = scrapy.item.Field()
    address = scrapy.item.Field()
    foreign_principal = scrapy.item.Field()
    date = scrapy.item.Field()
    exhibit_url = scrapy.item.Field()


class FaraSpider(scrapy.Spider):
    name = "fara"
    allowed_domains = ['efile.fara.gov']
    start_urls = ['https://efile.fara.gov/pls/apex/f?p=171:130:0::NO:RP,130:P130_DATERANGE:N']
    post_url = 'https://efile.fara.gov/pls/apex/wwv_flow.show'

    def __init__(self, *args, **kwargs):
        super(FaraSpider, self).__init__(*args, **kwargs)
        self.p_flow_id = None
        self.p_flow_step_id = None
        self.p_instance = None

    def get_next_url(self, response):
        try:
            p_widget_action_mod = response.css('td.pagination > span > a::attr("href")').extract()[-1]
            return re.compile("'(.*?)'").findall(p_widget_action_mod)[0]
        except (IndexError, TypeError):
            return None

    def get_post_data(self, response):
        p_widget_action_mod = self.get_next_url(response)
        if p_widget_action_mod:
            if self.p_instance is None:
                self.p_instance = response.css('input#pInstance ::attr("value")').extract_first()
            
            if self.p_flow_id is None:
                self.p_flow_id = response.css('input#pFlowId ::attr("value")').extract_first()
            
            if self.p_flow_step_id is None:
                self.p_flow_step_id = response.css('input#pFlowStepId ::attr("value")').extract_first()
            
            apexir_WORKSHEET_ID = response.css('input#apexir_WORKSHEET_ID ::attr("value")').extract_first()
            apexir_REPORT_ID = response.css('input#apexir_REPORT_ID ::attr("value")').extract_first()
            return {
                'p_request': 'APXWGT',
                'p_instance': self.p_instance,
                'p_flow_id': self.p_flow_id,
                'p_flow_step_id': self.p_flow_step_id,
                'p_widget_num_return': '15',
                'p_widget_name': 'worksheet',
                'p_widget_mod': 'ACTION',
                'p_widget_action': 'PAGE',
                'p_widget_action_mod': p_widget_action_mod,
                'x01': apexir_WORKSHEET_ID, 
                'x02': apexir_REPORT_ID,
            }
        return None

    def get_body_data(self, response):
        data = self.get_post_data(response)
        return urllib.parse.urlencode(data) if data else None

    def create_item(self, data):
        if data:
            item = ActivePrincipalItem()
            for key, value in data.items():
                item[key] = value
            if item['url']:
                request = scrapy.Request(item['url'] ,callback=self.parse_exhibit_url)
                request.meta['item'] = item
                return request
            return item

    def parse_exhibit_url(self, response):
        item = response.meta['item']

        for td_data in response.css('table.t7GCCReportsStyle2 td'):
            headers = td_data.xpath('@headers').extract_first()
            if headers and headers == 'DOCLINK':
                item['exhibit_url'] = td_data.css('a::attr("href")').extract_first()
        
        return item

    def parse(self, response):

        country_name = ''
        country_index = 0
        for tr in response.css('div#apexir_DATA_PANEL')[0].css('tr'):
            th_data = tr.css('th')
            if th_data.extract_first():
                aux_country_name = th_data.css('span.apex_break_headers::text').extract_first()
                if aux_country_name:
                    country_name = aux_country_name
                    country_index += 1

            data = {}
            for td_data in tr.css('td'):
                headers = td_data.xpath('@headers').extract_first() or ''

                if 'LINK' in headers:
                    link = 'https://efile.fara.gov/pls/apex/{0}'.format(td_data.css('a::attr("href")').extract_first() or '')
                    data.update({'url': link})

                elif 'FP_NAME' in headers:
                    data.update({'foreign_principal': td_data.css('td::text').extract_first() or ''})

                elif 'FP_REG_DATE' in headers:
                    data.update({'date' :td_data.css('td::text').extract_first() or ''})

                elif 'ADDRESS_1' in headers:
                    data.update({'address': td_data.css('td::text').extract_first() or ''})

                elif 'STATE' in headers:
                    data.update({'state': td_data.css('td::text').extract_first() or ''})

                elif 'REGISTRANT_NAME' in headers:
                    data.update({'registration': td_data.css('td::text').extract_first() or ''})

                elif 'REG_NUMBER' in headers:
                    data.update({'registration_number': td_data.css('td::text').extract_first() or ''})

                elif 'REG_DATE' in headers:
                    data.update({'registration_date': td_data.css('td::text').extract_first() or ''})
            if data:
                data.update({'country_name': country_name})
                yield self.create_item(data)

        body = self.get_body_data(response)
        if body:
            yield scrapy.Request(
                self.post_url,
                method="POST",
                body=body)
