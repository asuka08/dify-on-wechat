import re

from bot.bot import Bot
from bridge.context import Context
from bridge.reply import Reply, ReplyType


class EChoiceBot(Bot):

    def reply(self, query, context: Context = None):
        is_valid = self.validate_input_format(query)
        reply_content = "已收到，我备注一下。"
        if not is_valid:
            reply_content = "格式错误，请您按照:品类-品牌名字-身份-名字-角色 的格式，把您的信息提供给我。(例如:女装-伊美丽-品牌方-谭某某-运营)(例如:电器-添可-经销商-谭某某-老板)"
        reply = Reply(ReplyType.TEXT, reply_content)
        return reply

    def validate_input_format(self, input_text):
        pattern = re.compile(r'^[^-\s]+-[^-\s]+-[^-\s]+-[^-\s]+-[^-\s]+$')
        return bool(pattern.match(input_text))
