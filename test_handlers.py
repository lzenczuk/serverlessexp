import unittest
import mock

import handler


def s3_store_text_mock(text):
    print("Store text mock")


class TestStartPageHandler(unittest.TestCase):
    @mock.patch('jobbrose.s3.store_text', side_effect=s3_store_text_mock)
    def test_start_page(self, s3_store_text_mock_function):
        handler.start_page_handler(None, None)

        assert s3_store_text_mock_function.called


if __name__ == '__main__':
    unittest.main()
