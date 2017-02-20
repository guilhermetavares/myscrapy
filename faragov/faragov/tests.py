import os
import unittest
import requests
import urllib

from scrapy.http import HtmlResponse, Response, Request
from spiders.fara import FaraSpider


class OsdirSpiderTestCase(unittest.TestCase):
    body = '''

        <input type="hidden" name="p_flow_id" value="171" id="pFlowId" />
        <input type="hidden" name="p_flow_step_id" value="130" id="pFlowStepId" />
        <input type="hidden" name="p_instance" value="15842442319768" id="pInstance" />
        <input type="hidden" name="p_page_submission_id" value="6775972940794" id="pPageSubmissionId" />
        <input type="hidden" name="p_request" value="" id="pRequest" />

        <table class="t7GCCReportsStyle2">
            <td headers="ERRORLINK">
            </td>
            <td headers="DOCLINK">
                <a href="test_url">s</a>
            </td>
        </table>

        <td colspan="10" class="pagination" align="right">
            <span class="fielddata">
            <a href="javascript:gReport.navigate.paginate('pgR_min_row=1max_rows=15rows_fetched=15')">
                <img src="/i/jtfupree.gif" title="Previous" alt="Previous" align="absmiddle">
            </a> 16 - 30 of 510
            <a href="javascript:gReport.navigate.paginate('pgR_min_row=31max_rows=15rows_fetched=15')">
            <img src="/i/jtfunexe.gif" title="Next" alt="Next" align="absmiddle"></a></span></td>
    '''
    error_body = '''
        <td colspan="10" class="pagination" align="right">
        </td>
    '''

    example_data = {
        'address': '211 Corniche, PO Box 3600',
        'country_name': 'UNITED ARAB EMIRATES',
        'date': '07/31/2009',
        'exhibit_url': 'http://www.fara.gov/docs/5947-Exhibit-AB-20090731-1.pdf',
        'foreign_principal': 'Abu Dhabi Investment Authority',
        'registration': 'Brunswick Group, LLC',
        'registration_date': '07/31/2009',
        'registration_number': '5947',
        'state': '',
        'url': 'https://efile.fara.gov/pls/apex/f?p=171:200:16319220096257::NO:RP,200:P200_REG_NUMBER,P200_DOC_TYPE,P200_COUNTRY:5947,Exhibit%20AB,UNITED%20ARAB%20EMIRATES'
    }

    def setUp(self):
        self.spider = FaraSpider()
        self.url = 'https://efile.fara.gov/pls/apex/f?p=171:130:0::NO:RP,130:P130_DATERANGE:N'

    def fake_response_from_file(self, body=None):
        request = Request(url=self.url)

        if body is None:
            body = requests.get(self.url).text

        response = HtmlResponse(
            url=self.url,
            request=request,
            body=bytes(body, 'utf-8'))
        # response.encoding = 'utf-8'
        return response

    def test_01_get_next_url(self):
        response = self.fake_response_from_file(self.body)
        self.assertEqual(self.spider.get_next_url(response), 'pgR_min_row=31max_rows=15rows_fetched=15')

    def test_02_error_get_next_url(self):
        response = self.fake_response_from_file(self.error_body)
        self.assertEqual(self.spider.get_next_url(response), None)

    def test_03_get_post_data(self):
        response = self.fake_response_from_file(self.body)
        self.spider.p_flow_id = '9999999'
        self.spider.p_flow_step_id = '9999999'
        self.spider.p_instance = '9999999'
        data = self.spider.get_post_data(response)
        self.assertEqual(data.get('p_flow_id'), '9999999')
        self.assertEqual(data.get('p_flow_step_id'), '9999999')
        self.assertEqual(data.get('p_widget_name'), 'worksheet')

        self.spider.p_flow_id = None
        self.spider.p_flow_step_id = None
        self.spider.p_instance = None
        data = self.spider.get_post_data(response)
        self.assertEqual(data.get('p_flow_id'), '171')
        self.assertEqual(data.get('p_flow_step_id'), '130')
        self.assertEqual(data.get('p_widget_name'), 'worksheet')

    def test_04_get_post_data(self):
        response = self.fake_response_from_file(self.error_body)
        self.assertEqual(self.spider.get_post_data(response), None)

    def test_05_get_body_data(self):
        response = self.fake_response_from_file(self.body)
        self.assertTrue('pgR_min_row' in self.spider.get_body_data(response))

    def test_06_create_item(self):
        self.assertTrue(self.spider.create_item({}) is None)
        self.assertFalse(self.spider.create_item(self.example_data) is None)

    def test_07_parse_exhibit_url(self):
        rmv_url_example_data = self.example_data
        rmv_url_example_data['url'] = ''
        response = self.fake_response_from_file(self.body)
        response.meta['item'] = self.spider.create_item(rmv_url_example_data)
        item = self.spider.parse_exhibit_url(response)
        self.assertEqual(item['exhibit_url'], 'test_url')

    def test_08_parse(self):
        results = self.spider.parse(self.fake_response_from_file())
        for item in results:
           self.assertIsNotNone(item)

if __name__ == "__main__":
    unittest.main()
