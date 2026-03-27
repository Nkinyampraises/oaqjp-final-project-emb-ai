"""Emotion detection using Watson NLP Emotion Predict API."""

import requests


def emotion_detector(text_to_analyze):
    """Run emotion detection and return formatted emotion scores."""
    url = (
        "https://sn-watson-emotion.labs.skills.network/v1/"
        "watson.runtime.nlp.v1/NlpService/EmotionPredict"
    )
    headers = {
        "grpc-metadata-mm-model-id": "emotion_aggregated-workflow_lang_en_stock"
    }
    input_json = {"raw_document": {"text": text_to_analyze}}
    response = requests.post(url, headers=headers, json=input_json)
    formatted_response = response.json()
    emotions = formatted_response["emotionPredictions"][0]["emotion"]

    return {
        "anger": emotions["anger"],
        "disgust": emotions["disgust"],
        "fear": emotions["fear"],
        "joy": emotions["joy"],
        "sadness": emotions["sadness"],
    }
