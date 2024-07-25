# encoding:utf-8
import json
import threading

import requests

from bot.bot import Bot
from bot.dify.dify_session import DifySession, DifySessionManager
from bridge.context import ContextType, Context
from bridge.reply import Reply, ReplyType
from common.log import logger
from common import const
from config import conf


class QiquBot(Bot):
    api_base_url: None
    api_token: None

    def __init__(self):
        super().__init__()
        self.api_base_url = conf().get("qiqu_api_base", "https://qiqu.dify.ai/v1")
        self.api_token = conf().get("qiqu_api_token", "https://qiqu.dify.ai/v1")

    def reply(self, query, context: Context = None):
        # acquire reply content
        if context.type == ContextType.TEXT:
            reply, err = self._reply(query, context)
            if err != None:
                reply = Reply(ReplyType.TEXT, "我暂时遇到了一些问题，请您稍后重试~")
            return reply
        else:
            reply = Reply(ReplyType.ERROR, "Bot不支持处理{}类型的消息".format(context.type))
            return reply

    def _reply(self, query: str, context: Context):
        try:
            result = requests.post(f"{self.api_base_url}/api/v1/wework/chat", json={
                "message": query
            },headers={
                "Authorization": f"Bearer {self.api_token}"
            })
            return Reply(ReplyType.TEXT, result.text), None

        except Exception as e:
            error_info = f"[QIQU] Exception: {e}"
            logger.exception(error_info)
            return None, error_info
