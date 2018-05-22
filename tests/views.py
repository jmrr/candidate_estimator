from webtest import TestApp
import unittest
from iso8601 import parse_date

from candidate_estimator import main


class TestCandidatesAPI(unittest.TestCase):
    def setUp(self):
        settings = {
            'sqlalchemy.url': 'sqlite:///:memory:',
            'model': '../scripts/model.pkl',
        }
        self.app = TestApp(main({}, **settings))

    def test_post_get_candidate_profile(self):
        candidate = {
            "applicationId": "367125q77318",
            "candidateId": 367125,
            "invitationDate": "2016-04-07 06:07:47+00:00",
            "applicationTime": "2016-04-08 23:29:48+00:00",
            "isRetake": False,
            "speechToText": [
                {
                    "name": "Hi",
                    "time": "1.89",
                    "duration": "0.18",
                    "confidence": "1.000"
                },
                {
                    "name": "there",
                    "time": "2.22",
                    "duration": "0.15",
                    "confidence": "1.000"
                },
                {
                    "name": ".",
                    "time": "2.37",
                    "duration": "0.18",
                    "confidence": "1.000"
                }
            ],
            "videoLength": 115.09,
            "score": 4
        }
        self.app.post_json('/candidates', candidate, status=200)
        res = self.app.get('/candidates/1', status=200)

        dict_keys = (
            'applicationId', 'candidateId',
            'isRetake', 'videoLength', 'score',
        )
        self.assertTrue(
            {k: candidate[k] for k in dict_keys}.items()
            <=  # subset
            {k: res.json_body[k] for k in dict_keys}.items()
        )
        self.assertEqual(
            parse_date(candidate['invitationDate']),
            parse_date(res.json_body['invitationDate'])
        )
        self.assertEqual(
            parse_date(candidate['applicationTime']),
            parse_date(res.json_body['applicationTime'])
        )
