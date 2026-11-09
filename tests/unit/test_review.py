from unittest import mock

from factory import main


def test_review_reads_confidence():
    with mock.patch.object(main, "ask_agent", return_value="LGTM\nCONFIDENCE: 8"):
        assert main.review({"a.py": "x = 1"}, "claude") == 8


def test_review_low_confidence():
    with mock.patch.object(main, "ask_agent", return_value="bad code\nCONFIDENCE: 3"):
        assert main.review({"a.py": "x = 1"}, "claude") == 3
