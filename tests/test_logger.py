import unittest
import os
import json
from datetime import datetime
from unittest.mock import patch
from modules.logger import SessionLogger

class TestSessionLogger(unittest.TestCase):

    def setUp(self):
        self.logger = SessionLogger(method='file')
        self.session_id = 'test_session'
        self.logger.start_session(self.session_id)

    def tearDown(self):
        self.logger.close_session(self.session_id)
        log_file = f"log_{datetime.now().strftime('%Y-%m-%d')}.json"
        if os.path.exists(log_file):
            os.remove(log_file)

    def test_start_session(self):
        self.assertIn(self.session_id, self.logger.sessions)
        self.assertEqual(self.logger.sessions[self.session_id]['metadata'], {})
        self.assertEqual(len(self.logger.sessions[self.session_id]['logs']), 1)
        self.assertEqual(self.logger.sessions[self.session_id]['logs'][0]['message'], 'Session started')

    def test_log_entry(self):
        self.logger.log_entry(self.session_id, 'Test log entry', custom_fields={'key': 'value'})
        self.assertEqual(len(self.logger.sessions[self.session_id]['logs']), 2)
        self.assertEqual(self.logger.sessions[self.session_id]['logs'][1]['message'], 'Test log entry')
        self.assertEqual(self.logger.sessions[self.session_id]['logs'][1]['custom_fields']['key'], 'value')

    def test_save_logs_to_file(self):
        self.logger.save_logs()
        log_file = f"log_{datetime.now().strftime('%Y-%m-%d')}.json"
        self.assertTrue(os.path.exists(log_file))
        with open(log_file, 'r') as f:
            log_data = json.load(f)
        self.assertIn('Sessions', log_data)
        self.assertEqual(len(log_data['Sessions']), 1)
        self.assertEqual(log_data['Sessions'][0]['session_id'], self.session_id)

    @patch('builtins.print')
    def test_save_logs_to_stdout(self, mock_print):
        self.logger.method = 'stdout'
        self.logger.save_logs()
        mock_print.assert_called_once()
        printed_output = mock_print.call_args[0][0]
        log_data = json.loads(printed_output)
        self.assertIn('Sessions', log_data)
        self.assertEqual(len(log_data['Sessions']), 1)
        self.assertEqual(log_data['Sessions'][0]['session_id'], self.session_id)

    def test_save_logs_to_custom_handler(self):
        custom_handler_called = []

        def custom_handler(message):
            custom_handler_called.append(message)

        self.logger.method = 'custom'
        self.logger.kwargs['custom_handler'] = custom_handler
        self.logger.save_logs()
        self.assertEqual(len(custom_handler_called), 1)
        log_data = json.loads(custom_handler_called[0])
        self.assertIn('Sessions', log_data)
        self.assertEqual(len(log_data['Sessions']), 1)
        self.assertEqual(log_data['Sessions'][0]['session_id'], self.session_id)

if __name__ == '__main__':
    unittest.main()