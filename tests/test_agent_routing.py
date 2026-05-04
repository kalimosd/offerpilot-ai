import unittest
from unittest.mock import patch

from offerpilot.intent import classify_user_intent
from offerpilot.llm import get_llm


class AgentIntentTests(unittest.TestCase):
    def test_pipeline_intent_parses_chinese_scan_request(self) -> None:
        intent = classify_user_intent("扫描最近14天，推荐前20个国内岗位")

        self.assertEqual(intent["task_type"], "pipeline")
        self.assertEqual(intent["pipeline_days"], 14)
        self.assertEqual(intent["pipeline_top_n"], 20)
        self.assertTrue(intent["pipeline_cn_focus"])

    def test_batch_evaluate_intent_uses_default_profile(self) -> None:
        intent = classify_user_intent("帮我批量评估这些 JD")

        self.assertEqual(intent, {
            "task_type": "batch_evaluate",
            "batch_profile_path": "profile_store.yaml",
        })


class LlmCacheTests(unittest.TestCase):
    def tearDown(self) -> None:
        get_llm.cache_clear()

    def test_llm_cache_keeps_default_and_precise_clients(self) -> None:
        get_llm.cache_clear()

        with patch("langchain.chat_models.init_chat_model", side_effect=lambda *args, **kwargs: object()) as init_model:
            default_llm = get_llm()
            precise_llm = get_llm(temperature=0.1)
            default_llm_again = get_llm()

        self.assertIs(default_llm, default_llm_again)
        self.assertIsNot(default_llm, precise_llm)
        self.assertEqual(init_model.call_count, 2)


if __name__ == "__main__":
    unittest.main()
