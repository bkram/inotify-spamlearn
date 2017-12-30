#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# vim: ai ts=4 sts=4 et sw=4

import configparser
import logging
import os
import subprocess

import inotify.adapters


def getconfig():
    config = configparser.ConfigParser()
    try:
        config.read('inotify-spamlearn.cfg')
        path = config.get('path', 'watch')
        learncmd = config.get('spam', 'learncmd')
        return (path, learncmd)
    except:
        exit('Configuration error, please check \'config.cfg\'')


def learn(filename, spamcmd):
    cmd = ' '.join([spamcmd, filename])

    try:
        p = subprocess.Popen(cmd.split(' '), stdout=subprocess.PIPE)
        learning, output_err = p.communicate()
        logging.info('Learn [%s]: %s' % (filename, str(learning.decode('utf-8')).strip('\n')))

    except Exception as e:
        logging.warning('Learn failed [%s]: ' % e)

    else:
        logging.info('Removing file: %s' % filename)
        os.remove(filename)


def main():
    (path, learncmd) = getconfig()
    logging.basicConfig(filename='example.log', format='%(asctime)s %(message)s', level=logging.INFO)
    logging.info('Starting Inotify Learning')
    i = inotify.adapters.Inotify()
    i.add_watch(path)

    try:
        for event in i.event_gen():
            if event is not None:
                (header, type_names, watch_path, filename) = event
                if type_names[0] == 'IN_CLOSE_WRITE' and filename.split('.')[1] == 'eml':
                    print('file written %s' % filename)
                    learn('/'.join([path, filename]), learncmd)

    finally:
        i.remove_watch(path)


if __name__ == '__main__':
    main()
