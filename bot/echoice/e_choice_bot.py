import json
import re
from typing import Any, Dict

import requests

from bot.bot import Bot
from bridge.context import Context
from bridge.reply import Reply, ReplyType
from lib import itchat


class EChoiceBot(Bot):

    def reply(self, query, context: Context = None):
        # is_valid = self.validate_input_format(query)
        # reply_content = "已收到，我备注一下。"
        # if not is_valid:
        #     reply_content = "格式错误，请您按照:品类-品牌名字-身份-名字-角色 的格式，把您的信息提供给我。(例如:女装-伊美丽-品牌方-谭某某-运营)(例如:电器-添可-经销商-谭某某-老板)"
        check_res = self.check_content(query)
        category = check_res["category"]
        brand = check_res["brand"]
        identity = check_res["identity"]
        name = check_res["name"]
        role = check_res["role"]
        if all([category, brand, identity, name, role]):
            reply = Reply(ReplyType.TEXT, "好的，备注信息已收到")
            return reply
        else:
            if (category == "" and brand == "" and identity == "" and name == "" and role == ""):
                reply = Reply(ReplyType.TEXT,
                              "格式错误，请您按照:品类-品牌名字-身份-名字-角色 的格式，把您的信息提供给我。(例如:女装-伊美丽-品牌方-谭某某-运营)(例如:电器-添可-经销商-谭某某-老板)")
                return reply

            itchat.send("我确认一下哈，你看对不对", toUserName=context.kwargs["msg"].from_user_id)
            message2 = "品类: " + category + "\n" + "品牌: " + brand + "\n" + "身份: " + identity + "\n" + "名字: " + name + "\n" + "角色: " + role
            itchat.send(message2, toUserName=context.kwargs["msg"].from_user_id)
            reply_content = ""
            if category == "" or category is None:
                reply_content = reply_content + "品类名称是？\n"
            if brand == "" or brand is None:
                reply_content = reply_content + "品牌名称是？\n"
            if identity == "" or identity is None:
                reply_content = reply_content + "身份是？\n"
            if name == "" or name is None:
                reply_content = reply_content + "名字是？\n"
            if role == "" or role is None:
                reply_content = reply_content + "角色是？\n"
            reply = Reply(ReplyType.TEXT, reply_content)
            return reply

    def validate_input_format(self, input_text):
        pattern = re.compile(r'^[^-\s]+-[^-\s]+-[^-\s]+-[^-\s]+-[^-\s]+$')
        return bool(pattern.match(input_text))

    def check_content(self, input_text: str = "") -> Dict[str, Any]:
        data = {
            "inputs": {
                "content": input_text
            },
            "response_mode": "blocking",
            "user": "2283047992@qq.com",
        }
        url = "http://42.193.112.247:82/v1/workflows/run"
        headers = {
            'Authorization': "Bearer app-vRNBVXOsqhVY6h6KEKku3iBY",
            'Content-Type': 'application/json',
        }
        response = requests.post(url, headers=headers, data=json.dumps(data))
        res = {}
        if response.status_code == 200:
            response_data = response.json()
            print(response_data)
            # 检查 API 调用是否成功
            if response_data.get("data", {}).get("status") == "succeeded":
                outputs = response_data["data"]["outputs"]
                category = outputs["category"]
                brand = outputs["brand"]
                identity = outputs["identity"]
                name = outputs["name"]
                role = outputs["role"]
                print(f"category: {category}, brand: {brand}, identity: {identity}, name: {name}, role: {role}")
                res = {
                    "category": category if category and category != "无" else '',
                    "brand": brand if brand and brand != "无" else '',
                    "identity": identity if identity and identity != "无" else '',
                    "name": name if name and name != "无" else '',
                    "role": role if role and role != "无" else ''
                }
            else:
                print(f"API call failed, response: {response_data}")
        return res
