import pytest
from pytest_mock import MockerFixture
from tests import APITestcase, AssertRequest, AssertResponse

ROUTE = "/callback"

UNHANDLED_EVENT = {
    "replyToken": "0f3779fba3b349968c5d07db31eab56f",
    "type": "message",
    "mode": "active",
    "timestamp": 1462629479859,
    "source": {"type": "user", "userId": "U4af4980629"},
    "message": {"id": "325708", "type": "text", "text": "Hello, world"},
}

QUICKREPLY_EVENT = {
    **UNHANDLED_EVENT,
    **{"message": {"id": "325708", "type": "text", "text": "/quickreply"}},
}

QUICKREPLY_INCORRECT_EVENT = {
    **UNHANDLED_EVENT,
    **{"message": {"id": "325708", "type": "text", "text": "1"}},
}

QUICKREPLY_CORRECT_EVENT = {
    **UNHANDLED_EVENT,
    **{"message": {"id": "325708", "type": "text", "text": "2"}},
}

CASES = [
    APITestcase(
        "unhandled events",
        AssertRequest(
            "POST",
            ROUTE,
            None,
            json={"destination": "xxxxxxxxxx", "events": [UNHANDLED_EVENT]},
        ),
        AssertResponse("OK", 200),
    ),
    APITestcase(
        "quickreply",
        AssertRequest(
            "POST",
            ROUTE,
            None,
            json={"destination": "xxxxxxxxxx", "events": [QUICKREPLY_EVENT]},
        ),
        AssertResponse("OK", 200),
    ),
    APITestcase(
        "quickreply_correct",
        AssertRequest(
            "POST",
            ROUTE,
            None,
            json={"destination": "xxxxxxxxxx", "events": [QUICKREPLY_CORRECT_EVENT]},
        ),
        AssertResponse("OK", 200),
    ),
    APITestcase(
        "quickreply_incorrect",
        AssertRequest(
            "POST",
            ROUTE,
            None,
            json={"destination": "xxxxxxxxxx", "events": [QUICKREPLY_INCORRECT_EVENT]},
        ),
        AssertResponse("OK", 200),
    ),
    APITestcase(
        "quickreply_invalid",
        AssertRequest(
            "POST",
            ROUTE,
            None,
            json={"destination": "xxxxxxxxxx", "events": [QUICKREPLY_EVENT]},
        ),
        AssertResponse("OK", 200),
    ),
]
