import unittest
from PhoneFetch import phone_fetch


class TestPF(unittest.TestCase):
    def test_hands_ru(self):
        self.assertEqual(phone_fetch(['https://hands.ru/company/about/']), {'84951370720'}, 'hands.ru test')

    def test_repetitors_info(self):
        self.assertEqual(phone_fetch(['https://repetitors.info/']), {'88005057284',
                                                                     '88005555676',
                                                                     '84952292491',
                                                                     '84955405676',
                                                                     '88005057283',
                                                                     '84955625880'},
                         'repetitors test')

    def test_invalid_url(self):
        self.assertEqual(phone_fetch(['http//invalid.url']), set(), 'invalid URL test')

    def test_few_urls(self):
        self.assertEqual(phone_fetch(['https://hands.ru/company/about/',
                                      'https://repetitors.info/',
                                      'http//invalid.url']),
                         {'88005057284',
                          '88005555676',
                          '84952292491',
                          '84955405676',
                          '88005057283',
                          '84955625880',
                          '84951370720'},
                         'few pages test')


if __name__ == '__main__':
    unittest.main()
