from disco.handler import BaseHandler

class MorphexHandler(BaseHandler):
    def __init__(self):
        super().__init__()
        self.allowed_servers = ["Morphex", "Bot Dev", "w3n"]
        self.global_rate_limit = True
        self.delete_own = True

#     # # faq menu
#     # elif re.search(r'^!faq$', message_lower):
#     #     await self.do_faq_menu(message)

#     # # faq responses
#     # elif message_lower in self.faq.keys():
#     #     await self.do_faq_response(message)
