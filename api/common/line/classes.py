from typing import List, Optional, Tuple

# pylint: disable=E0611
from pydantic import BaseModel

# pylint: enable=E0611


class Event(BaseModel):
    replyToken: Optional[str]
    type: str
    mode: str
    timestamp: int
    source: dict
    message: Optional[dict]


class TextMessage:
    """Line text message class"""

    text = ""

    def __init__(self, text: str):
        self.text = text

    def format(self) -> dict:
        """Return format for messaging API"""
        return {"type": "text", "text": self.text}


class QuickReplyMessage(TextMessage):
    """
    A QuickReply message
    Combination of TextMessage and reply options
    """

    quick_replies = []

    def __init__(self, text: str, quick_replies: List[Tuple[str, str]]):
        super().__init__(text)
        self.quick_replies = quick_replies

    def format(self):
        """Return format for messaging API"""
        payload = super().format()
        payload["quickReply"] = {"items": []}
        for item in self.quick_replies:
            payload["quickReply"]["items"].append(
                {
                    "type": "action",
                    "action": {"type": "message", "label": item[0], "text": item[1]},
                }
            )
        return payload


class FlexMessage:
    """LineBotDesigner format"""

    jsonformat = ""
    altText = ""

    def __init__(self, jsonformat: dict, altText: str):
        self.jsonformat = jsonformat
        self.altText = altText

    def format(self):
        return {"type": "flex", "altText": self.altText, "contents": self.jsonformat}


class ImageMessage:
    original = ""
    preview = ""

    def __init__(self, original: str, preview: str):
        self.original_content_url = original
        self.preview_image_url = preview

    def format(self) -> dict:
        return {
            "type": "image",
            "originalContentUrl": self.original_content_url,
            "previewImageUrl": self.preview_image_url,
        }


class ImageMapMessage:
    baseUrl = ""
    altText = ""
    baseSize = {"width": 0, "height": 0}
    video = {}
    action = []

    PARMS = {
        "baseUrl": "",
        "altText": "懶人包(點選查看專家文章)",
        "baseSize": {"width": 1040, "height": 1470},
        # NOTE: The width of the image must be 1040 px, and set the height that corresponds to a width of 1040 px. Reference: https://developers.line.biz/en/reference/messaging-api/#imagemap-message
        "action": [
            {
                "type": "uri",
                "area": {
                    "x": 0,
                    "y": 0,
                    "width": 1040,
                    "height": 1470,
                },
                "linkUri": "",
            }
        ],
    }

    def __init__(
        self,
        baseUrl: str,
        linkUri: str,
        altText: str = PARMS["altText"],
        baseSize: dict = PARMS["baseSize"],
        action: list = PARMS["action"],
        video: dict = {},
    ):
        self.baseUrl = baseUrl
        self.altText = altText
        self.baseSize = baseSize
        self.action = [{**action[0], "linkUri": linkUri}]
        self.video = video

    def format(self) -> dict:
        payload = {
            "type": "imagemap",
            "baseUrl": self.baseUrl,
            "altText": self.altText,
            "baseSize": self.baseSize,
            "actions": self.action,
        }
        if self.video:
            payload["video"] = self.video

        return payload


class QuickReplyCamera(FlexMessage):

    def __init__(self, jsonformat: str, altText: str):
        super().__init__(jsonformat, altText)

    def format(self):
        """Return format for messaging API"""
        payload = super().format()
        payload["quickReply"] = {"items": []}
        for type, label in [("camera", "開啟相機"), ("cameraRoll", "開啟相簿")]:
            payload["quickReply"]["items"].append(
                {
                    "type": "action",
                    "action": {"type": type, "label": label},
                }
            )
        return payload


def dataframe_to_flex_message(df):
    # Convert the DataFrame to a list of dictionaries
    data = df.to_dict(orient="records")
    # Get the column headers
    headers = df.columns.tolist()

    # Create the header content for the Flex Message
    header_contents = [
        {
            "type": "text",
            "text": header,
            "weight": "bold",  # Make the header bold
            "color": "#000000",  # Use a darker color for the header text
            "size": "xs",
            "flex": 1,
            "align": "start",  # Align headers to the start
        }
        for header in headers
    ]

    # Add a separator after the headers
    contents = [
        {
            "type": "box",
            "layout": "horizontal",
            "contents": header_contents,
            "margin": "xs",  # Add some margin to separate from the data rows
        },
        {"type": "separator"},
    ]

    # Add the data rows
    for row in data:
        row_contents = [
            {
                "type": "text",
                "text": str(row[header]),
                "size": "md",
                "color": "#555555",
                "flex": 1,
                "align": "start",  # Align data to the start
            }
            for header in headers
        ]
        contents.append(
            {"type": "box", "layout": "horizontal", "contents": row_contents}
        )

    # Create the Flex Message using your FlexMessage class
    flex_message = FlexMessage(
        jsonformat={
            "type": "bubble",
            "body": {"type": "box", "layout": "vertical", "contents": contents},
        },
        altText="Your data",
    )

    return flex_message
