# -*- Mode: python; coding: utf-8 -*-
import os
from gi.repository.Gio import Settings

IS_PLAY=True
IS_STOP=False
IS_POSITION=True
NO_POSITION=False
MIN_ELAPSED=2
SETTINGS_KEY="org.gnome.rhythmbox.plugins.restore"
ENTRY_KEY="entry"
POS_KEY="position"
IS_PLAY_KEY=  "isplay"
IS_POSITION_KEY = "isplaypos"

class RestoreSettings:
    """Special class to work with plugin settings"""
    def __init__(self):
        self.entry = None
        self.position = NO_POSITION
        self.isPlay = IS_STOP
        self.isPosition = NO_POSITION
        self.dbloaded = False
        self.elapsed = False
        self.settings = Settings(SETTINGS_KEY)
        self.read_settings()

    def writeSettings(self, entry,  type):
        """Writes plugin settings to gconf"""
        try:
            if entry:
                self.entry = entry.get_string(type)
            if self.entry and (self.entry[0:4] in ('http','file','ftp:')):
                #
                self.settings.set_string(ENTRY_KEY, self.entry)
                if self.isPosition == 1:
                    self.settings.set_int(POS_KEY, self.position)
                else:
                    self.settings.set_int(POS_KEY, NO_POSITION)
                self.settings.set_boolean(IS_PLAY_KEY, self.isPlay)
                self.settings.set_boolean(IS_POSITION_KEY, self.isPosition)
        except Exception as e:
            os.sys.stderr.write("Error in writeSettings function\n")
            os.sys.stderr.write(str(e)+"\n")

    def read_settings(self):
        """Reads gconf keys into variables"""
        self.entry = self.settings.get_string(ENTRY_KEY)
        self.position = self.settings.get_int(POS_KEY)
        self.isPlay = self.settings.get_boolean(IS_PLAY_KEY)
        if self.isPlay == None:
            self.isPlay = IS_PLAY
        self.isPosition = self.settings.get_boolean(IS_POSITION_KEY)
        if self.isPosition == None:
            self.isPosition = NO_POSITION

    def set_gconf_key (self, **kwargs):
        """Sets settings changed in Configure Dialog"""
        kw = kwargs
        if "isplay" in kw:
            self.isPlay = kw["isplay"]
            self.settings.set_int(IS_PLAY_KEY, self.isPlay)
        if "isplaypos" in kw:
            self.isPosition = kw["isplaypos"]
            self.settings.set_int(IS_POSITION_KEY['isplaypos'], self.isPosition)
