# -*- coding: utf-8 -*-
import json

__author__ = 'anna'


def fallback(header, items):
    return "*{0}*\n {1}".format(header, bulletize(items))


def bulletize(items, bullet=u'•'):
    newline = "\n {0} ".format(bullet)
    return "{0} {1}".format(bullet, newline.join([str(item) for item in items]))


def format_menu(name, distance, items):
    if len(items) > 3:
        fallback_items = items[0:3]
    else:
        fallback_items = items
    attachments = [{
        'pretext': "*{} ({} min)*".format(name, distance),
        'fallback': fallback(name, fallback_items),
        'text': bulletize(items),
        'color': 'good',
        'mrkdwn_in': ['pretext', 'text']
    }]
    return json.dumps(attachments)
