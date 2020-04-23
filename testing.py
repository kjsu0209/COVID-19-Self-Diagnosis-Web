import unittest
import test, app
import nltk
from nltk.tokenize import word_tokenize
import json


class TestGetRAD(unittest.TestCase):

    def test_word_classifier(self):
        keyword = 'vomited'
        words = word_tokenize(keyword)
        # returns tag name of part of speech
        tag_block = nltk.pos_tag(words)
        print(tag_block)
        # returns stemmed word
        t = test.word_classify(tag_block[0][1], tag_block[0][0])
        self.assertEqual(t, 'vomit')

    def test_return_value(self):
        # returns 0 if argument is not symptom word
        r = test.get_rad_value('happy')
        self.assertEqual(r, 0)
        # returns RAD value if argument is symptom word existed in dataset
        r = test.get_rad_value('fever')
        self.assertTrue(0 < r < 1)


class TestSteps(unittest.TestCase):
    symptom_list = []

    @classmethod
    def setUpClass(cls):
        pass

    @classmethod
    def tearDownClass(cls):
        pass

    def tearDown(self):
        pass

    def setUp(self):
        # creates a test client
        self.app = app.app.test_client()
        # propagate the exceptions to the test client
        self.app.testing = True

    def test_step1(self):
        symptom_string = 'I have a headache and cough.'
        req = '/step1?symptom='
        req += symptom_string
        res = self.app.get(req)
        self.symptom_list = json.loads(res.data)

        # assert the response data
        self.assertEqual(res.data, b'{"symptoms":["headache","cough"]}\n')

    def test_step3(self):
        self.symptom_list = ["headache", "cough"]
        str = ''
        for s in self.symptom_list:
            str += s + ','
        req = '/step3?symptom='
        req += str

        res = self.app.get(req)
        rad_value = json.loads(res.data)
        rad_value = rad_value['rad'][0]
        rad_value = json.loads(rad_value)

        for s in rad_value.keys():
            # assert the RAD value of each symptom exists
            print(s, ': ', rad_value[s])
            self.assertTrue(rad_value[s] > 0)


if __name__ == '__main__':
    unittest.main()