# inotify-spamlearn

## Description
Designed to be a companion to the Kopano Core kopano-spamd, which is included from Kopano Core 8.6.
The kopano-spamd, detects spam state changes, and writes these to /var/lib/kopano/spamd/spam or the /var/lib/kopano/spamd/ham or folder as eml files for further processing by external tooling.

## Installation
Copy the included config file to /etc/kopano/ and put the inotify-spamlearn.py script somewhere in your path.
Run the script as a user which can both run the required spam command and delete files from the /var/lib/kopano/spamd/spam and /var/lib/kopano/spamd/spam directory.
Also make sure you also have write permission for the log file.

## Python modules required
- inotify
- configparser
- logging
- os
- subprocess

## Possible Todo's
- Add a proper service file to start the inotify-spamlearn with systemd. 
- Start initial scan on startup as a seperate thread.
- Daemonize (or let systemd care about that).
- Make use of python-kopano for server initialization.
