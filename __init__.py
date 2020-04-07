from mycroft import MycroftSkill, intent_file_handler
from mycroft.messagebus.message import Message
from mycroft.skills.msm_wrapper import build_msm_config, create_msm
import time
import os


class Password(MycroftSkill):
    _msm = None
    def __init__(self):
        MycroftSkill.__init__(self)

    def initialize(self):
        self.settings["password"] = self.settings.get('password', None)
        self.settings["uespassword"] = self.settings.get('usepassword', False)
        self.settings["allowskill"] = self.settings.get('allowskill', "password")
        self.settings["timeout"] = self.settings.get('timeout', 0)
        if self.settings["password"] is None:
            self.log.info("no Password found")
            self.shutdown()
        if self.settings["uespassword"] is True:
            self.enable = False
            self.log.info("go sleep")
            self.handler_sleep()
        else:
            self.enable = True
    
    @property
    def msm(self):
        if self._msm is None:
            msm_config = build_msm_config(self.config_core)
            self._msm = create_msm(msm_config)

        return self._msm

    def handler_sleep(self):
        skills = [skill for skill in self.msm.all_skills if skill.is_local]
        for skill in skills:
            if not self.settings["allowskill"] in str(skill):
                folder = os.path.basename(skill.path)
                try:
                    if self.enable is False:
                        self.bus.emit(Message('skillmanager.deactivate',
                                    {'skill': str(folder)}))
                    else:
                        self.bus.emit(Message('skillmanager.activate',
                                    {'skill': str(folder)}))
                except TypeError:
                    self.log.info(skill+ " already done")

        self.log.info("end list")
    
    @intent_file_handler('password.intent')
    def handle_password(self, message):
        password = message.data.get("password")
        if password is None and self.enable is False:
            self.speak_dialog("say.password")
            #self.bus.emit(Message('recognizer_loop:sleep'))
            return
        elif password is None:
            self.log.info("no password found")
            return
        if self.settings["password"] in password:
            self.enable = True
            self.speak_dialog('password')
        else:
            self.enable = False
            self.speak_dialog("wrong.password")
        self.handler_sleep()


    @intent_file_handler('logout.intent')
    def handle_logout(self, message):
        self.enable = False
        self.speak_dialog("logout")
        self.handler_sleep()

    def shutdown(self):
        super(Password, self).shutdown()


def create_skill():
    return Password()

