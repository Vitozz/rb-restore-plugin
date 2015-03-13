#!/usr/bin/env python

from distutils.core import setup
from distutils.command.install_data import install_data
import os

class InstallData(install_data):
    def run (self):
        os.system('glib-compile-schemas /usr/share/glib-2.0/schemas/')
        install_data.run (self)
        return

setup(name='rb-restore-plugin',
      version='0.9.4',
      description='Rhythmbox restore plugin',
      long_description = "Restores the played item when Rhythmbox is starting",
      author='Vitaly Tonkacheyev',
      author_email='thetvg@gmail.com',
      url='http://sites.google.com/site/thesomeprojects/',
      maintainer='Vitaly Tonkacheyev',
      maintainer_email='thetvg@gmail.com',
      data_files=[  ('/usr/lib/rhythmbox/plugins/restore', ['restore.py']),
                    ('/usr/lib/rhythmbox/plugins/restore', ['_settings.py']),
                    ('/usr/lib/rhythmbox/plugins/restore', ['config.py']),
                    ('/usr/lib/rhythmbox/plugins/restore', ['restore.glade']),
                    ('/usr/lib/rhythmbox/plugins/restore', ['restore.plugin']),
                    ('/usr/share/glib-2.0/schemas', ['org.gnome.rhythmbox.plugins.restore.gschema.xml']),
                 ],
      )

