from bot.bot import Bot
from bridge.context import Context
from bridge.reply import Reply, ReplyType


class EChoiceBot(Bot):

    def reply(self, query, context: Context = None):
        print("[EChoice] query={}".format(query))
        print("[EChoice] Context={}".format(context))

        from_user_id = context.kwargs["msg"].from_user_id
        to_user_id = context.kwargs["msg"].to_user_id
        print(from_user_id)
        print(to_user_id)

        reply = Reply(ReplyType.TEXT, "Hello, I am EChoice Bot.")
        return reply
