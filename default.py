#!/usr/bin/env python
# -*- coding: utf-8 -*-
from __future__ import absolute_import, division, unicode_literals
import logging
import sys
import os
import urlparse

import xbmcgui
import xbmcplugin
import xbmcaddon

from resources.lib import loghandler

loghandler.config()
LOG = logging.getLogger()

PLUGIN_PATH = 'plugin://plugin.video.proof-of-concept'

__addon__ = xbmcaddon.Addon()
__addon_path__ = __addon__.getAddonInfo('path').decode('utf-8')
# Dummy video file with a lenght of 10min, 5s
VIDEO_FILE_PATH = os.path.join(__addon_path__, 'dummy-movie.mkv').encode('utf-8')
TOTAL_LENGTH = 10 * 60 + 5
RESUME = 5 * 60


def directory_item(label, path):
    """
    Adds a xbmcplugin.addDirectoryItem() directory itemlistitem
    """
    listitem = xbmcgui.ListItem(label, path=path)
    xbmcplugin.addDirectoryItem(handle=int(sys.argv[1]),
                                url=path,
                                listitem=listitem,
                                isFolder=True)


def main_menu():
    xbmcplugin.setContent(int(sys.argv[1]), 'files')
    directory_item('Proof of concept',
                   '%s/?mode=demo' % PLUGIN_PATH)
    xbmcplugin.endOfDirectory(int(sys.argv[1]))


def show_demo():
    xbmcplugin.setContent(int(sys.argv[1]), 'movies')
    listitem = xbmcgui.ListItem('Demo video file')

    listitem.setProperty("isPlayable", "true")
    xbmcplugin.addDirectoryItem(handle=int(sys.argv[1]),
                                url='%s/?mode=play' % PLUGIN_PATH,
                                listitem=listitem,
                                isFolder=False)
    xbmcplugin.endOfDirectory(int(sys.argv[1]))

def play():
    listitem = xbmcgui.ListItem('Demo video file')
    listitem.setPath(VIDEO_FILE_PATH)
    xbmcplugin.setResolvedUrl(int(sys.argv[1]), True, listitem)


if __name__ == '__main__':
    LOG.info('Full sys.argv received: %s', sys.argv)
    args = sys.argv[2][1:].decode('utf-8')
    args = dict(urlparse.parse_qsl(args))
    mode = args.get('mode')
    if mode == 'demo':
        show_demo()
    elif mode == 'play':
        play()
    else:
        main_menu()
