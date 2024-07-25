# encoding:utf-8

import json
import os
import requests
import plugins
from bridge.context import ContextType
from bridge.reply import Reply, ReplyType
from common.log import logger
from plugins import *
import random
from config import conf


@plugins.register(
    name="QiquWework",
    desire_priority=997,
    hidden=True,
    desc="奇趣企业微信需求",
    version="0.1",
    author="xing.syner",
)
class QiquWework(Plugin):
    api_base_url: None
    api_token: None

    def __init__(self):
        super().__init__()
        try:
            self.conf = conf()
            self.handlers[Event.ON_RECEIVE_MESSAGE] = self.on_receive_message
            self.handlers[Event.ON_HANDLE_CONTEXT] = self.on_handle_context
            self.handlers[Event.ON_DECORATE_REPLY] = self.on_decorate_reply
            self.api_base_url = conf().get("qiqu_api_base", "")
            self.api_token = conf().get("qiqu_api_token", "")
            logger.info("[qiqu wework] inited.")
        except Exception as e:
            logger.warn(
                "[keyword] init failed, ignore or see https://github.com/zhayujie/chatgpt-on-wechat/tree/master/plugins/keyword .")
            raise e

    def on_receive_message(self, e_context: EventContext):
        if e_context["context"].kwargs["msg"].is_group_admin or (
                not e_context["context"].kwargs["msg"].is_company_user):
            print("record")
            # requests.post("", json={
            #     "is_group_admin": e_context["context"].kwargs["msg"].is_group_admin,
            #     "company_user_id": e_context["context"].kwargs["msg"].company_user_id,
            #     "actual_user_nickname": e_context["context"].kwargs["msg"].actual_user_nickname,
            #     "from_user_nickname": e_context["context"].kwargs["msg"].from_user_nickname
            #     # from_user_id
            #
            #    })
            # """
            #     ChatMessage: id=R:10698764940847169, create_time=1721821589, ctype=TEXT, content=5553, from_user_id=R:10698764940847169, from_user_nickname=测试1, to_user_id=1688857370558766, to_user_nickname=高鑫, other_user_id=R:10698764940847169, other_user_nickname=测试1, is_group=True, is_at=False, actual_user_id=7881300270909054, actual_user_nickname=高鑫, at_list=[]"""

        e_context.action = EventAction.CONTINUE  # 事件结束，并跳过处理context的默认逻辑

    def on_handle_context(self, e_context: EventContext):

        if not e_context["context"].kwargs["isgroup"]:
            e_context.action = EventAction.BREAK_PASS
            return

        if e_context["context"].kwargs["msg"].is_group_admin or (
                not e_context["context"].kwargs["msg"].is_company_user):
            print("record")
            # requests.post("", json={
            #     "is_group_admin": e_context["context"].kwargs["msg"].is_group_admin,
            #     "company_user_id": e_context["context"].kwargs["msg"].company_user_id,
            #     "actual_user_nickname": e_context["context"].kwargs["msg"].actual_user_nickname,
            #     "from_user_nickname": e_context["context"].kwargs["msg"].from_user_nickname
            #     # from_user_id
            #
            #    })
            # """
            #     ChatMessage: id=R:10698764940847169, create_time=1721821589, ctype=TEXT, content=5553, from_user_id=R:10698764940847169, from_user_nickname=测试1, to_user_id=1688857370558766, to_user_nickname=高鑫, other_user_id=R:10698764940847169, other_user_nickname=测试1, is_group=True, is_at=False, actual_user_id=7881300270909054, actual_user_nickname=高鑫, at_list=[]"""


        if self.conf.get("close_reply_company_user", False) and e_context["context"].kwargs["msg"].is_company_user:
            e_context.action = EventAction.BREAK_PASS
            return
        if e_context["context"].type != ContextType.TEXT:
            return
        e_context.action = EventAction.CONTINUE  # 事件结束，并跳过处理context的默认逻辑

    def on_decorate_reply(self, e_context: EventContext):
        if e_context["context"].type != ContextType.TEXT:
            return
        if e_context["reply"].content == "机器人不给予回复":
            # e_context.action = EventAction.BREAK_PASS
            e_context["reply"].type = 0
            return
        e_context.action = EventAction.CONTINUE  # 事件结束，并跳过处理context的默认逻辑

    def get_help_text(self, **kwargs):
        help_text = "奇趣企业微信"
        return help_text
