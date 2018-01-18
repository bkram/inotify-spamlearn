#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# vim: ai ts=4 sts=4 et sw=4

import inotify.adapters
import configparser
import logging
import os
import subprocess


def getconfig():
    config = configparser.ConfigParser()
    try:
        config.read('/etc/kopano/inotify-spamlearn.cfg')
        path = config.get('path', 'watch')
        learncmd = config.get('spam', 'learncmd')
        delete = config.getboolean('spam', 'delete')
        startup = config.getboolean('spam', 'startup')
        logfile = config.get('logs', 'logfile')
        return path, learncmd, logfile, delete, startup
    except:
        exit('Configuration error, please check \'inotify-spamlearn.cfg\'')


def learn(filename, spamcmd, delete):
    cmd = ' '.join([spamcmd, filename])
    if os.path.exists(filename):
        try:
            p = subprocess.Popen(cmd.split(' '), stdout=subprocess.PIPE)
            learning, output_err = p.communicate()
            logging.info('Learn [%s]: %s' % (filename, str(learning.decode('utf-8')).strip('\n')))

        except Exception as e:
            logging.warning('Learn failed [{}]: '.format(e))

        else:
            if delete:
                logging.info('Removing file: {}'.format(filename))
                os.remove(filename)
    else:
        logging.warning('File %s does not exist (anymore)' % filename)


def start():
    (path, learncmd, logfile, delete, startup) = getconfig()
    logging.basicConfig(filename=logfile, format='%(asctime)s %(message)s', level=logging.INFO)
    logging.info('Starting Process')

    if startup:
        try:
            logging.info('Looking for existing spam')
            for spam in os.listdir(path):
                learn('/'.join([path, spam]), learncmd, delete)
        except:
            logging.error('Cannot open path {}'.format(path))

    i = inotify.adapters.Inotify()
    try:
        i.add_watch(path)
    except Exception:
        logging.error('Cannot start inotify watch for {}'.format(path))
    else:
        logging.info('Inotify Learning Started')

    try:
        for event in i.event_gen():
            if event is not None:
                (header, type_names, watch_path, filename) = event
                if type_names[0] == 'IN_CLOSE_WRITE':
                    learn('/'.join([path, filename]), learncmd, delete)

    finally:
        i.remove_watch(path)


def main():
    start()


if __name__ == '__main__':
    main()
