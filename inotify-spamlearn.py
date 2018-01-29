#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# vim: ai ts=4 sts=4 et sw=4

import logging
import os
import subprocess

import configparser
import inotify.adapters


def getconfig():
    config = configparser.ConfigParser()
    try:
        config.read('/etc/kopano/inotify-spamlearn.cfg')
        spam_dir = config.get('paths', 'spam_dir')
        ham_dir = config.get('paths', 'ham_dir')
        spamcmd = config.get('spam', 'spamcmd')
        hamcmd = config.get('spam', 'spamcmd')
        delete = config.getboolean('spam', 'delete')
        startup = config.getboolean('spam', 'startup')
        logfile = config.get('logs', 'logfile')
        return spam_dir, ham_dir, spamcmd, hamcmd, logfile, delete, startup
    except Exception as e:
        exit('Configuration {}\n please check inotify-spamlearn.cfg'.format(e))


def process(filename, spamcmd, delete):
    cmd = ' '.join([spamcmd, filename])
    if os.path.exists(filename):
        try:
            p = subprocess.Popen(cmd.split(' '), stdout=subprocess.PIPE)
            learning, output_err = p.communicate()
            logging.info('Processing [%s]: %s' % (filename, str(learning.decode('utf-8')).strip('\n')))

        except Exception as e:
            logging.warning('Processing failed [{}]: '.format(e))

        else:
            if delete:
                logging.info('Removing file: {}'.format(filename))
                os.remove(filename)
    else:
        logging.warning('File %s does not exist (anymore)' % filename)


def start():
    (spam_dir, ham_dir, spamcmd, hamcmd, logfile, delete, startup) = getconfig()

    logging.basicConfig(filename=logfile, format='%(asctime)s %(message)s', level=logging.INFO)
    logging.info('Starting Process')

    if startup:

        for checkdir in [spam_dir, ham_dir]:

            logging.info('Looking for existing files in {}'.format(checkdir))
            for spam in os.listdir(checkdir):
                try:
                    if checkdir == spam_dir:
                        process('/'.join([checkdir, spam]), spamcmd, delete)
                    elif checkdir == ham_dir:
                        process('/'.join([checkdir, spam]), hamcmd, delete)
                except Exception as e:
                    logging.error('Cannot open path {} {}'.format(checkdir, e))

    i = inotify.adapters.Inotify()
    try:
        i.add_watch(spam_dir)
        i.add_watch(ham_dir)
    except Exception as e:
        logging.error('Cannot start inotify watch: {}'.format(e))
    else:
        logging.info('Inotify Learning Started')

    try:
        for event in i.event_gen():
            if event is not None:
                (header, type_names, watch_path, filename) = event
                if type_names[0] == 'IN_CLOSE_WRITE':
                    if watch_path == spam_dir:
                        process('/'.join([watch_path, filename]), spamcmd, delete)
                    elif watch_path == ham_dir:
                        process('/'.join([watch_path, filename]), hamcmd, delete)

    finally:
        i.remove_watch([spam_dir, ham_dir])


def main():
    start()


if __name__ == '__main__':
    main()
