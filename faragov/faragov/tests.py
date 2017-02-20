import os
import unittest
import urllib

from scrapy.http import HtmlResponse, Response, Request
from spiders.fara import FaraSpider


class OsdirSpiderTestCase(unittest.TestCase):

    def setUp(self):
        self.spider = FaraSpider()
        self.url = 'https://efile.fara.gov/pls/apex/f?p=171:130:0::NO:RP,130:P130_DATERANGE:N'

    def fake_response_from_file(self):
        request = Request(url=self.url)
        r = requests.get(self.url)
        response = HtmlResponse(
            url=self.url,
            request=request,
            body=bytes(r.text, 'utf-8'))
        # response.encoding = 'utf-8'
        return response

    def _test_item_results(self, results, expected_length):
        count = 0
        permalinks = set()
        for item in results:
            self.assertIsNotNone(item['content'])
            self.assertIsNotNone(item['title'])
        self.assertEqual(count, expected_length)

    def test_01_parse(self):
        results = self.spider.parse(self.fake_response_from_file())
        print(results)
        for item in results:
            print(item)
        # self._test_item_results(results, 10)

if __name__ == "__main__":
    unittest.main()
