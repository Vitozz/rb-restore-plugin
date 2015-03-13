<b>Rhythmbox playback resotre plugin</b>

Restores last playing track on start of Rhythmbox (>=2.95).

To install plugin manually do the next steps:
- download sources archive
- downloaded archive in example placed at $HOME

```bash
cd $HOME
tar -xzf rb-restore-plugin_{version}.tar.gz
cp -r $HOME/restore $HOME/.local/share/rhythmbox/plugins/
cd $HOME/.local/share/rhythmbox/plugins/restore
```

- copy as superuser schema-file to /usr/share/glib-2.0/schemas/

```bash
cp *.gschema.xml /usr/share/glib-2.0/schemas/
```

- compile dconf settings

```bash
glib-compile-schemas /usr/share/glib-2.0/schemas/
```

- Or just run as superuser setup.py script

```bash
sudo python setup.py install
```
