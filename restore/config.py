# -*- Mode: python; coding: utf-8 -*-
from gi.repository import Gtk, GObject, PeasGtk
from gi.repository.Gio import Settings
from gi.repository import RB
import os, locale
SETTINGS_KEY="org.gnome.rhythmbox.plugins.restore"
ISPLAY_KEY="isplay"
ISPOS_KEY="isplaypos"

class RestoreConfigureDialog (GObject.Object, PeasGtk.Configurable):
    """This class is responsible for the appearance of the Preferences dialog"""
    __gtype_name__ = 'RestoreConfigureDialog'
    object = GObject.property(type=GObject.Object)
      
    def do_create_configure_widget(self):
        self.gladexml = Gtk.Builder()
        glade_file = self.find_plugin_file(self, "restore.glade")
        self.gladexml.add_from_file(glade_file)
        self.gladexml.get_objects()
        self.locale = locale
        self.dialog = self.gladexml.get_object("preferences_dialog")
        self.isplay_toggle = self.gladexml.get_object("isplay")
        self.isplaypos_toggle = self.gladexml.get_object("isplaypos")
        self.apply_btn= self.gladexml.get_object("ok_button")
        self.label = self.gladexml.get_object("frameCaption")
        self.SetLocale()
        self.dialog.connect("response", self.dialog_response)
        self.apply_btn.connect("released",  self.onApply)
        self.isplay_toggle.connect('toggled', self.isplay_toggled)
        self.isplaypos_toggle.connect('toggled', self.isplaypos_toggled)
        self.settings = Settings(SETTINGS_KEY)
        isplay = self.settings.get_boolean(ISPLAY_KEY)
        ispos = self.settings.get_boolean(ISPOS_KEY)
        self.isplay_toggle.set_active(isplay)
        self.isplaypos_toggle.set_active(ispos)
        return self.dialog

    def dialog_response (self, dialog, response):
        dialog.hide()
        
   
    def onApply(self,  widget):
        self.dialog.hide()

    def SetLocale(self):
        #check russian locale
        if 'ru' in self.locale.getlocale()[0]:
            self.isplay_toggle.set_label("Не воспроизводить при восстановлении")
            self.isplaypos_toggle.set_label("Восстанавливать позицию последнего трека")
            self.dialog.set_title("Настройки восстановления")
            self.label.set_text("Опции")
        #check ukrainian locale
        elif 'ua' in self.locale.getlocale()[0]:
            self.isplay_toggle.set_label("Не програвати при відновленні")
            self.isplaypos_toggle.set_label("Відновлювати позицію останньої композиції")
            self.dialog.set_title("Налаштування відновлення")
            self.label.set_text("Опції")

    def isplay_toggled (self, togglebutton):
        self.settings.set_boolean(ISPLAY_KEY,  togglebutton.get_active())

    def isplaypos_toggled(self,  togglebutton):
        self.settings.set_boolean(ISPOS_KEY,  togglebutton.get_active())
    
    def find_plugin_file(self,  plugin, filename):
        info = plugin.plugin_info
        data_dir = info.get_data_dir()
        path = os.path.join(data_dir, filename)
        if os.path.exists(path):
            return path
        return RB.file(filename)

    
GObject.type_register(RestoreConfigureDialog)
