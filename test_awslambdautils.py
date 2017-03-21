import unittest
import test_events_examples
from awslambdautils import lambda_events


class TestEventTypeRecognition(unittest.TestCase):
    def test_recognition(self):
        self.assertEquals(lambda_events.EventType.UNKNOWN,
                          lambda_events.get_event_type(test_events_examples.get_unknown_event()))
        self.assertEquals(lambda_events.EventType.SNS,
                          lambda_events.get_event_type(test_events_examples.get_sns_event()))
        self.assertEquals(lambda_events.EventType.KINESIS,
                          lambda_events.get_event_type(test_events_examples.get_kinesis_event()))
        self.assertEquals(lambda_events.EventType.DYNAMODB,
                          lambda_events.get_event_type(test_events_examples.get_dynamodb_event()))

    def test_get_kinesis_data(self):
        data = lambda_events.get_kinesis_event_json_data_list(test_events_examples.get_kinesis_event())

        self.assertEquals(1, len(data))
        self.assertIn('jsession', data[0])
        self.assertEquals('qwerty123', data[0]['jsession'])
        self.assertIn('id', data[0])
        self.assertEquals(245, data[0]['id'])

    def test_get_sns_data(self):
        data = lambda_events.get_sns_event_json_data_list(test_events_examples.get_sns_event())

        self.assertEquals(1, len(data))
        self.assertIn('jsession', data[0])
        self.assertEquals('qwerty123', data[0]['jsession'])
        self.assertIn('id', data[0])
        self.assertEquals(245, data[0]['id'])


if __name__ == '__main__':
    unittest.main()
