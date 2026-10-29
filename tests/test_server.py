import json
import os
import unittest
from unittest.mock import patch, MagicMock

import server


class OpenAIProxyTests(unittest.TestCase):
    def setUp(self):
        self.env_patch = patch.dict(os.environ, {}, clear=True)
        self.env_patch.start()
        self.file_patch = patch.object(server, "ENV_FILE", "/tmp/atlas-test-env-does-not-exist")
        self.file_patch.start()

    def tearDown(self):
        self.file_patch.stop()
        self.env_patch.stop()

    def test_missing_key_fails_with_setup_guidance(self):
        with self.assertRaisesRegex(RuntimeError, "OPENAI_API_KEY"):
            server.openai_chat({"messages": [{"role": "user", "content": "hello"}]})

    def test_rejects_empty_messages(self):
        os.environ["OPENAI_API_KEY"] = "test-key"
        with self.assertRaisesRegex(ValueError, "messages array"):
            server.openai_chat({"messages": []})

    def test_successful_openai_response_is_normalized(self):
        os.environ["OPENAI_API_KEY"] = "test-key"
        response = MagicMock()
        response.__enter__.return_value = response
        response.read.return_value = json.dumps({
            "choices": [{"message": {"content": "  Hello from mocked OpenAI  "}}]
        }).encode("utf-8")
        with patch.object(server.urllib.request, "urlopen", return_value=response) as urlopen:
            result = server.openai_chat({
                "system": "Be concise",
                "messages": [{"role": "user", "content": "hello"}]
            })
        self.assertEqual(result, {"text": "Hello from mocked OpenAI"})
        request = urlopen.call_args.args[0]
        self.assertEqual(request.full_url, "https://api.openai.com/v1/chat/completions")
        self.assertEqual(request.get_header("Authorization"), "Bearer test-key")
        body = json.loads(request.data.decode("utf-8"))
        self.assertEqual(body["model"], "gpt-4.1-mini")
        self.assertEqual(body["messages"][0]["role"], "system")
        self.assertEqual(body["messages"][1]["content"], "hello")


if __name__ == "__main__":
    unittest.main()
