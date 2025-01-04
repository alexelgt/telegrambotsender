# telegrambotsender
# Copyright (C) 2025 Alexelgt

# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU Affero General Public License as published
# by the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.

# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU Affero General Public License for more details.

# You should have received a copy of the GNU Affero General Public License
# along with this program.  If not, see <https://www.gnu.org/licenses/>.

from typing import Optional

import json
import requests


class TelegramBotSender:
    """Class to send messages to Telegram as a bot"""

    def __init__(
        self,
        bot_token: str
    ) -> None:
        """Initialize and instance of the class

        Args:
            bot_token (str): token of the bot to use to send the messages
        """
        self.bot_token = bot_token

    def send_text_message(
        self,
        chat_id: int,
        msg_text: Optional[str],
        msg_entities: Optional[list[dict]] = None,
        timeout: int = 10
    ) -> Optional[dict]:
        """""Send a text message to a Telegram chat

        Args:
            chat_id (int): unique identifier for the target chat
            msg_text (Optional[str]): text of the message to be sent
            msg_entities (Optional[list[dict]], optional): list of entities of the message. Each element of the list is a MessageEntity dict (https://core.telegram.org/bots/api#messageentity). Defaults to None
            timeout (int, optional): time in seconds to wait. Defaults to 10

        Returns:
            Optional[dict]: result of the message sent
        """""
        if msg_entities is not None:
            msg_entities = json.dumps(msg_entities)

        try:
            if msg_text is not None:
                message_sent = requests.post(
                    url=f"https://api.telegram.org/bot{self.bot_token}/sendMessage",
                    data={
                        "chat_id": chat_id,
                        "text": msg_text,
                        "disable_web_page_preview": True,
                        "entities": msg_entities
                    },
                    timeout=timeout
                ).json()

                return message_sent["result"]
            return
        except:
            return

    def send_media_group_message(
        self,
        chat_id: int,
        msg_text: Optional[str],
        media_info: list[dict],
        msg_entities: Optional[list[dict]] = None,
        timeout: int = 10
    ) -> Optional[dict]:
        """Send a media group message to a Telegram chat

        Args:
            chat_id (int): unique identifier for the target chat
            msg_text (Optional[str]): text of the message to be sent
            media_info (list[dict]): list of media elements to sent. Each element of the list is a InputMedia dict (https://core.telegram.org/bots/api#inputmedia).
            msg_entities (Optional[list[dict]], optional): list of entities of the message. Each element of the list is a MessageEntity dict (https://core.telegram.org/bots/api#messageentity). Defaults to None
            timeout (int, optional): time in seconds to wait. Defaults to 10

        Returns:
            Optional[dict]: result of the message sent
        """
        try:
            if msg_text is not None and len(media_info) > 0:
                media_info[0]["caption"] = msg_text
                media_info[0]["caption_entities"] = msg_entities

                message_sent = requests.post(
                    url=f"https://api.telegram.org/bot{self.bot_token}/sendMediaGroup",
                    data={
                        "chat_id": chat_id,
                        "media": json.dumps(media_info)
                    },
                    timeout=timeout
                ).json()

                print(message_sent)

                return message_sent["result"]
            return
        except:
            return
