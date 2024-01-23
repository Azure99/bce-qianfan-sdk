import logging
from typing import Any, AsyncIterator, Dict, List, Optional, Tuple, Union

from qianfan.extensions.semantic_kernel.connectors.qianfan_settings import (
    QianfanChatRequestSettings,
    QianfanRequestSettings,
    QianfanTextRequestSettings,
)
from qianfan.resources import ChatCompletion
from semantic_kernel.connectors.ai.ai_exception import AIException
from semantic_kernel.connectors.ai.ai_request_settings import AIRequestSettings
from semantic_kernel.connectors.ai.ai_service_client_base import AIServiceClientBase
from semantic_kernel.connectors.ai.chat_completion_client_base import (
    ChatCompletionClientBase,
)
from semantic_kernel.connectors.ai.text_completion_client_base import (
    TextCompletionClientBase,
)

logger: logging.Logger = logging.getLogger(__name__)


class QianfanChatCompletion(
    ChatCompletionClientBase, TextCompletionClientBase, AIServiceClientBase
):
    client: Any
    """
    qianfan sdk client
    """

    def __init__(
        self,
        model: str = "ERNIE-Bot-turbo",
        endpoint: Optional[str] = None,
        **kwargs: Any,
    ):
        """
        Initializes a new instance of the QianfanChatCompletion class.

        Arguments:
            model Optional[str]
                model name for qianfan.
            endpoint Optional[str]
                model endpoint for qianfan.
            app_ak_sk: Optional[Tuple[str, str]], see
                https://cloud.baidu.com/doc/WENXINWORKSHOP/s/Dlkm79mnx#access_token%E9%80%82%E7%94%A8%E7%9A%84api
            iam_ak_sk: Optional[Tuple[str, str]], see
                https://cloud.baidu.com/doc/WENXINWORKSHOP/s/Dlkm79mnx#%E5%AE%89%E5%85%A8%E8%AE%A4%E8%AF%81aksk%E7%AD%BE%E5%90%8D%E8%AE%A1%E7%AE%97%E9%80%82%E7%94%A8%E7%9A%84api
        """
        super().__init__(
            ai_model_id=model,
            client=ChatCompletion(
                model=model,
                endpoint=endpoint,
                **kwargs,
            ),
        )

    async def complete_chat_async(
        self,
        messages: List[Dict[str, str]],
        settings: QianfanRequestSettings,
        **kwargs: Any,
    ) -> Optional[str]:
        assert isinstance(settings, QianfanChatRequestSettings)
        settings.messages = messages
        response = await self._send_chat_request(settings)
        return response["result"]["messages"][-1]["content"]

    async def complete_chat_stream_async(
        self,
        messages: List[Tuple[str, str]],
        settings: QianfanRequestSettings,
    ):
        assert isinstance(settings, QianfanChatRequestSettings)
        settings.messages = messages
        settings.stream = True
        response = await self._send_chat_request(settings)
        async for r in response:
            yield r["result"]

    async def complete_async(
        self,
        prompt: str,
        settings: QianfanRequestSettings,
        **kwargs,
    ) -> Union[str, None]:
        if isinstance(settings, QianfanChatRequestSettings):
            settings.messages.extend({"role": "user", "content": prompt})
        elif isinstance(settings, QianfanTextRequestSettings):
            settings.messages = [{"role": "user", "content": prompt}]

        response = await self._send_chat_request(settings)

        return response["result"]["messages"][-1]["content"]

    async def complete_stream_async(
        self,
        prompt: str,
        settings: QianfanRequestSettings,
        **kwargs,
    ) -> AsyncIterator[Union[str, None]]:
        res = await self._send_chat_request(settings)
        for r in res:
            yield r

    async def _send_chat_request(
        self, settings: QianfanRequestSettings, **kwargs: Any
    ) -> Union[Union[str, None], AsyncIterator[Union[Dict, None]]]:
        if settings is None:
            raise ValueError("The request settings cannot be `None`")
        try:
            data = {**settings.prepare_settings_dict(), **kwargs}
            response = await self.client.ado(**data)
        except Exception as ex:
            raise AIException(
                AIException.ErrorCodes.ServiceError,
                "qianfan chat service failed to response the messages",
                ex,
            )
        return response

    def get_request_settings_class(self) -> "AIRequestSettings":
        """Create a request settings object."""
        return QianfanChatRequestSettings