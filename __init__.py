from mycroft import MycroftSkill, intent_file_handler


class MySamsungTvRc(MycroftSkill):
    def __init__(self):
        MycroftSkill.__init__(self)

    @intent_file_handler('rc.tv.samsung.my.intent')
    def handle_rc_tv_samsung_my(self, message):
        self.speak_dialog('rc.tv.samsung.my')


def create_skill():
    return MySamsungTvRc()

