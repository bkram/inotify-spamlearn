# inotify-spamlearn

## Description

Designed to be a companion to the Kopano Core kopano-spamd, which is included from Kopano Core 8.6.
The kopano-spamd, detects spam state changes, and writes these to /var/lib/kopano/spamd/spam or the /var/lib/kopano/spamd/ham or folder as eml files for further processing by external tooling.

## Python modules required

- logging
- os
- subprocess
- configparser
- inotify.adapters
- threading

## Things to take care of before installation

Edit the configuration file if required.

Change the inotify-speamlearn.service to reflect the username and group required for your spamlearn command.

## Basic installation

```bash
sudo cp inotify-spamlearn.cfg /etc/kopano
sudo cp inotify-spamlearn.py /usr/local/sbin/
sudo cp inotify-spamlearn.service /etc/systemd/system
sudo systemctl enable inotify-spamlearn
sudo systemctl start inotify-spamlearn
```

## Verify if it is running

```bash
sudo systemctl status inotify-spamlearn
sudo journalctl -u inotify-spamlearn -f
```

## TODO

- only scan directories and exit (crontab mode)
