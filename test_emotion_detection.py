import unittest
from unittest.mock import patch

from EmotionDetection import emotion_detector


class _MockResponse:
    def __init__(self, payload, status_code=200):
        self._payload = payload
        self.status_code = status_code

    def json(self):
        return self._payload

def _mock_post(url, headers=None, json=None, **kwargs):
    text = json["raw_document"]["text"]
    if text is None or str(text).strip() == "":
        return _MockResponse({}, status_code=400)

    mocked_emotions = {
        "I am glad this happened": {
            "anger": 0.01,
            "disgust": 0.01,
            "fear": 0.01,
            "joy": 0.95,
            "sadness": 0.02,
        },
        "I am really mad about this": {
            "anger": 0.92,
            "disgust": 0.02,
            "fear": 0.01,
            "joy": 0.01,
            "sadness": 0.04,
        },
        "I feel disgusted just hearing about this": {
            "anger": 0.02,
            "disgust": 0.94,
            "fear": 0.01,
            "joy": 0.01,
            "sadness": 0.02,
        },
        "I am so sad about this": {
            "anger": 0.02,
            "disgust": 0.01,
            "fear": 0.01,
            "joy": 0.01,
            "sadness": 0.95,
        },
        "I am really afraid that this will happen": {
            "anger": 0.01,
            "disgust": 0.01,
            "fear": 0.95,
            "joy": 0.01,
            "sadness": 0.02,
        },
    }
    return _MockResponse({"emotionPredictions": [{"emotion": mocked_emotions[text]}]})


class TestEmotionDetector(unittest.TestCase):
    @patch("EmotionDetection.emotion_detection.requests.post", side_effect=_mock_post)
    def test_joy(self, _):
        self.assertEqual(emotion_detector("I am glad this happened")["dominant_emotion"], "joy")

    @patch("EmotionDetection.emotion_detection.requests.post", side_effect=_mock_post)
    def test_anger(self, _):
        self.assertEqual(
            emotion_detector("I am really mad about this")["dominant_emotion"], "anger"
        )

    @patch("EmotionDetection.emotion_detection.requests.post", side_effect=_mock_post)
    def test_disgust(self, _):
        self.assertEqual(
            emotion_detector("I feel disgusted just hearing about this")[
                "dominant_emotion"
            ],
            "disgust",
        )

    @patch("EmotionDetection.emotion_detection.requests.post", side_effect=_mock_post)
    def test_sadness(self, _):
        self.assertEqual(emotion_detector("I am so sad about this")["dominant_emotion"], "sadness")

    @patch("EmotionDetection.emotion_detection.requests.post", side_effect=_mock_post)
    def test_fear(self, _):
        self.assertEqual(
            emotion_detector("I am really afraid that this will happen")[
                "dominant_emotion"
            ],
            "fear",
        )

    @patch("EmotionDetection.emotion_detection.requests.post", side_effect=_mock_post)
    def test_blank_input(self, _):
        self.assertEqual(
            emotion_detector(""),
            {
                "anger": None,
                "disgust": None,
                "fear": None,
                "joy": None,
                "sadness": None,
                "dominant_emotion": None,
            },
        )


if __name__ == "__main__":
    unittest.main()
