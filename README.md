Rhtyhmbox Restore Plugin

Restores last playing track on Rhythmbox (>=2.95) start
To install plugin manually do the next steps:
# download sources archive
# downloaded archive in example placed at $HOME 
cd $HOME
tar -xzf rb-restore-plugin_{version}.tar.gz
cp -r $HOME/restore $HOME/.local/share/rhythmbox/plugins/
cd $HOME/.local/share/rhythmbox/plugins/restore
# copy as superuser schema-file to /usr/share/glib-2.0/schemas/
cp *.gschema.xml /usr/share/glib-2.0/schemas/
# compile dconf settings
glib-compile-schemas /usr/share/glib-2.0/schemas/
Or just run as superuser setup.py script

sudo python setup.py install 
