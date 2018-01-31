# inotify-spamlearn

## Description

A companion to the Kopano Core kopano-spamd, which is included from Kopano Core 8.6 on.

The kopano-spamd detects spam/ham state changes and writes these to either /var/lib/kopano/spamd/spam or /var/lib/kopano/spamd/ham respectively.

These folders are used by inotify-spamlearn to expose these eml files to external tooling.

The [kopano-spamd](https://github.com/Kopano-dev/kopano-core/tree/master/ECtools/spamd) from Kopano Core git master can be found here.

## Python modules required

- logging
- os
- subprocess
- configparser
- inotify.adapters
- threading

## Basic installation

### Configuration

- Edit the inotify-spamlearn.cfg file if required.
- Edit the inotify-speamlearn.service to reflect the username and group required for your spamlearn command.
- Verify the provided /etc/kopano/spamd.cfg is correct for your setup e.g. check the sa_group.

### Copying the files

```bash
sudo cp inotify-spamlearn.cfg /etc/kopano
sudo cp inotify-spamlearn.py /usr/local/sbin/
sudo cp inotify-spamlearn.service /etc/systemd/system
```

### Enabling and starting

```bash
sudo systemctl enable inotify-spamlearn
sudo systemctl start inotify-spamlearn
```

## Verify if it is running

In the default config all logging is to the console, so systemd takes care of it, use journalctl to read the logging.

```bash
sudo systemctl status inotify-spamlearn
sudo journalctl -u inotify-spamlearn -f
```
