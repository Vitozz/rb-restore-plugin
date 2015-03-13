# -*- Mode: python; coding: utf-8 -*-
# This is a Rhythmbox Restore plugin.
#
# Main features:
## - can restore last playing item when Rhythmbox player starts
## - can restore last playing item position
## - if appropriate option is selected the plugin can stop playing after recovery
## - if appropriate option is selected, the plugin will not restore the position of the last track
#
#
from gi.repository import Peas, RB
import  os
from gi.repository import GObject,  Gdk,  GLib
from _settings import RestoreSettings
from config import RestoreConfigureDialog
import threading, time

SLEEP_TIME=0.5
ITERATIONS=10

IS_PLAY=True
IS_STOP=False
IS_POSITION=True
NO_POSITION=False
MIN_ELAPSED=2

class restorePlugin (GObject.Object, Peas.Activatable):
    __gtype_name__ = 'restore'
    object = GObject.property (type=GObject.Object)
    
    def __init__(self):
        GLib.threads_init()
        Gdk.threads_init()
        super(restorePlugin, self).__init__()
        self.current_entry = None
        self.events = []
        self.work = None
        self.source = None
        self.settings = None
        self.shell = None
        self.sp = None
        self.db = None
        self.init_entry = None
        self.dbloaded = False

    def do_activate(self):
        """Function runs when plugin activated"""
        self.shell = self.object
        self.sp = self.shell.props.shell_player
        self.db = self.shell.props.db
        self.settings = RestoreSettings()
        self.init_entry = self.settings.entry
        psc_evt =  self.sp.connect("playing-song-changed", self.playing_song_changed)
        self.events.append(psc_evt)
        self.dbloaded_evt = self.db.connect_after('load-complete', self.onDBLoaded)

    def do_deactivate(self):
        """Function runs when plugin deactivated"""
        if self.work.isAlive:
            self.work._Thread__stop()
            self.work.join(0)
            del self.work
        for event in self.events:
            if event:
                self.sp.disconnect(event)
                event = None
                del event
        self.settings.writeSettings(self.current_entry, RB.RhythmDBPropType.LOCATION)
        del self.events
        del self.current_entry
        del self.settings
        del self.source
        del self.shell
    
    def onDBLoaded(self, db):
        """Runs on RhythmDB load-complete signal"""
        db.disconnect(self.dbloaded_evt)
        del self.dbloaded_evt
        self.runThreads()

    def runThreads(self):
        """Initialize working thread and run it"""
        self.work= RertoreThread(self)
        self.work.start()

    def getEntry(self):
        """Sets the current entry"""
        try:
            if self.settings.entry:
                can_load = RB.uri_exists(self.settings.entry)
                if(can_load):
                    self.current_entry = self.db.entry_lookup_by_location(self.settings.entry)
                    if self.current_entry != None:
                        self.source = self.shell.get_source_by_entry_type(self.current_entry.get_entry_type())
            return self.current_entry != None
        except Exception as e:
            os.sys.stderr.write("Error in GetEntry function\n")
            os.sys.stderr.write("TRACK %s\n" % self.settings.entry)
            os.sys.stderr.write("POS: %s\n" % self.settings.position)
            os.sys.stderr.write(str(e)+"\n")
            return False

    def setEntry(self):
        """Set Current Entry function"""
        sp = self.object.props.shell_player
        current_entry = self.current_entry
        source = self.source
        if current_entry != None:
            if (self.settings.isPlay==True):
                Gdk.threads_enter()
                if self.selectEntry(current_entry,  source):
                    self.dbloaded = True
                else:
                    self.dbloaded = False
                Gdk.threads_leave()
            else:
                Gdk.threads_enter()
                sp.play_entry(current_entry)
                Gdk.threads_leave()
                self.dbloaded = True
        else:
            self.dbloaded = False
        return self.dbloaded

    def selectEntry(self, entry, source, entry_view = None):
        """Selects the current entry in player playlist"""
        if entry:
            sp = self.object.props.shell_player
            if source != None:
                sp.set_selected_source(source)
                try:                    
                    if not self.object.get_property("visibility"):
                        self.object.toggle_visibility()
                    entry_view = source.get_entry_view()
                except Exception as e:
                    os.sys.stderr.write("Error in SetEntry function\n")
                    os.sys.stderr.write(str(e)+"\n")
            if entry_view != None:
                try:
                    if entry_view.get_entry_contained(entry):
                        entry_view.select_entry(entry)
                        entry_view.scroll_to_entry(entry)
                        return True
                except Exception as e:
                    os.sys.stderr.write("Error in SetEntry function\n")
                    os.sys.stderr.write(str(e)+"\n")
                return False
            else:
                return False

    def playing_song_changed(self, sp, entry):
        """Function runs on playing-song-changed signal"""
        if entry != None:
            self.current_entry = entry

    def initEntry(self, entry):
        """Checks if saved track is a current playing track"""
        return (entry == self.getPlayingEntry())

    def getPlayingEntry(self):
        """Returns the current playing track uri"""
        try:
            entry = self.object.props.shell_player.get_playing_entry()
            if (entry):
                return entry.get_string(RB.RhythmDBPropType.LOCATION)
            else:
                return None
        except Exception as e:
            os.sys.stderr.write("Error %s" %str(e))
            return None

    def setPosition(self, sp):
        """Sets current track position at player startup"""
        if self.initEntry(self.init_entry):
            try:
                sp.set_playing_time(self.settings.position)
                self.settings.elapsed = True
                del self.init_entry
            except Exception as e:
                self.settings.elapsed = False
                os.sys.stderr.write("Error in  setPosition function\n")
                os.sys.stderr.write(str(e)+"\n")

    def elapsed_changed(self, sp, elapsed):
        """Checks if first run and sets track position, else writes position to settings,
            Function runs on elapsed_changed signal"""
        if self.dbloaded and (self.settings.isPosition) :
            if not self.settings.elapsed:
                Gdk.threads_enter()
                self.setPosition(sp)
                Gdk.threads_leave()
            if elapsed > MIN_ELAPSED:
                self.settings.position = elapsed

class RertoreThread(threading.Thread):
    """Working thread class"""
    def __init__(self, parent):
        super(RertoreThread,  self).__init__()
        self.parent = parent

    def run(self):
        idented = False
        if self.parent.settings.entry:
            for i in range(ITERATIONS):
                if self.parent.getEntry():
                    idented = True
                    time.sleep(SLEEP_TIME)
                    break
                else:
                    time.sleep(SLEEP_TIME)
            if idented and self.parent.current_entry:
                while not self.parent.setEntry():
                    time.sleep(SLEEP_TIME)
                self.parent.settings.elapsed = False
                player=self.parent.object.props.shell_player
                ec_evt = player.connect('elapsed_changed',self.parent.elapsed_changed)
                self.parent.events.append(ec_evt)
                print("Tread Finished")
