from mycroft import MycroftSkill, intent_handler
from mycroft.util.log import getLogger
from mycroft.util import extract_number
from mycroft.api import DeviceApi
import sys
import os
import time
import samsungctl
LOGGER = getLogger(__name__)


class MySamsungTvRc(MycroftSkill):
    def __init__(self):
        super(MySamsungTvRc, self).__init__(name="MySamsungTV")

    def initialize(self):
        self.settings_change_callback = self.on_settings_changed
        self.on_settings_changed()
        self.same_device = DeviceApi()
        info = self.same_device.get(); self.same_device = info['description'].lower()
        self.trans = {"nach links": "LEFT", "nach rechts": "RIGHT", "nach oben": "UP", "nach unten": "DOWN", "nehmen": "ENTER", "verlassen": "EXIT"}

    def on_settings_changed(self):
        self.host = self.settings.get('tv')
        self.port = self.settings.get('port')
        self.placement = self.settings.get('placement')
        self.name = self.settings.get('tvname')
        self.method = self.settings.get('method')
        self.description = self.settings.get('description')
        self.translations = self.settings.get('translations')
        self.trans = self.translations.split(',')
        self.trans = {self.trans[0]: 'LEFT', self.trans[1]: 'RIGHT', \
            self.trans[2]: 'UP', self.trans[3]: 'DOWN', \
            self.trans[4]: 'ENTER', self.trans[5]: 'EXIT'}
        LOGGER.info(self.host)

        self.config = {"name": self.name, "description": self.description,\
            "id": "", "host": self.host, "port": self.port, "method": self.method,\
            "timeout": 0}

#Main functions
    def send_keycode(self, keycode):
        '''Standard function for sending keycodes'''
        keycode = "KEY_" + keycode.upper()
        try:
            with samsungctl.Remote(self.config) as remote:
                remote.control(keycode)
        except Exception as e:
            LOGGER.info(str(e))
        finally:
            pass

#Helper functions
    def send_channel_pos(self, pos):
        '''Function for sending channel number; with multi-digit numbers \
        the values are transmitted number by number. Therefore there is a \
        small pause to consider the latency time of the LAN/WLAN or web server.'''
        if len(pos) > 1:
            i = 0
            while i < len(pos):
                self.send_keycode(pos[i])
                time.sleep(.5)
                i += 1
        else:
            self.send_keycode(pos)

    def explain_cursor_moves(self):
        '''Usage of cursor based selections'''
        self.speak_dialog('cursor_moves')
        move = ""
        return move

    def cursor_recursion(self, move):
        '''Recursive function to handle cursor movements'''
        move = self.get_response('cursor_dummy', 0)
        if move == None:
            keycode = "EXIT"
            self.send_keycode(keycode)
            return
        if move == "nehmen":
            keycode = "ENTER"
            self.send_keycode(keycode)
            return
        if move == "verlassen":
            keycode = "EXIT"
            self.send_keycode(keycode)
            return
        keycode = self.trans[move]
        self.send_keycode(keycode)
        move = ""
        self.cursor_recursion(move)

##Handlers
#basic handlers
    @intent_handler('next_channel.intent')
    def handle_next_channel(self):
        keycode = "CHUP"
        self.send_keycode(keycode)

    @intent_handler('prev_channel.intent')
    def handle_prev_channel(self):
        keycode = "CHDOWN"
        self.send_keycode(keycode)

    @intent_handler('pos.intent')
    def handle_switch_to_pos(self, message):
        pos = message.data.get('pos_nr')
        pos = extract_number(pos); pos=str(int(pos))
        self.send_channel_pos(pos)

    @intent_handler('vol_up.intent')
    def handle_vol_up(self):
        keycode = "VOLUP"
        self.send_keycode(keycode)

    @intent_handler('vol_down.intent')
    def handle_vol_down(self):
        keycode = "VOLDOWN"
        self.send_keycode(keycode)

    @intent_handler('exit.intent')
    def handle_exit(self):
        keycode = "EXIT"
        self.send_keycode(keycode)

#dialog handlers
    @intent_handler('channel_by_dialog.intent')
    def handle_channel_by_dialog(self, message):
        keycode = "CH_LIST"
        self.send_keycode(keycode)
        move = self.explain_cursor_moves()
        self.cursor_recursion(move)

    @intent_handler('program_guide_dialog.intent')
    def handle_program_guide(self):
        keycode = "GUIDE"
        self.send_keycode(keycode)
        move = self.explain_cursor_moves()
        self.cursor_recursion(move)

    @intent_handler('source_dialog.intent')
    def handle_source(self):
        keycode = "SOURCE"
        self.send_keycode(keycode)
        move = self.explain_cursor_moves()
        self.cursor_recursion(move)

    @intent_handler('smarthub_dialog.intent')
    def handle_smarthub(self):
        keycode = "CONTENTS"
        self.send_keycode(keycode)
        move = self.explain_cursor_moves()
        self.cursor_recursion(move)

#recording and playback handlers
    @intent_handler('pause.intent')
    def handle_timeshift_or_pause(self):
        keycode = "PAUSE"
        self.send_keycode(keycode)

    @intent_handler('play.intent')
    def handle_playing(self):
        keycode = "PLAY"
        self.send_keycode(keycode)

    @intent_handler('stop.intent')
    def handle_stop(self):
        keycode = "STOP"
        self.send_keycode(keycode)

    @intent_handler('record.intent')
    def handle_recording(self):
        keycode = "REC"
        self.send_keycode(keycode)

    @intent_handler('rewind.intent')
    def handle_recording(self):
        keycode = "REWIND"
        self.send_keycode(keycode)

    @intent_handler('fastforward.intent')
    def handle_recording(self):
        keycode = "FF"
        self.send_keycode(keycode)

#source handlers
    @intent_handler('hdmi.intent')
    def handle_recording(self):
        keycode = "HDMI"
        self.send_keycode(keycode)

    @intent_handler('dtv.intent')
    def handle_recording(self):
        keycode = "DTV"
        self.send_keycode(keycode)

    def stop(self):
        pass

def create_skill():
    return MySamsungTvRc()

