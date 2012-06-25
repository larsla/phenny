# -*- coding: utf-8 -*-
#!/usr/bin/env python
"""
megahal.py - Megahal module for phenny
"""

from bs4 import BeautifulSoup
import urllib2

def _strip(phenny, input):
    #print "_strip: " + input
    r = input.lstrip(phenny.nick)
    r = r.lstrip(": ")
    print "Stripped: " + r
    return r

def learn(phenny, input):
    if input.startswith("."): return
    #print "learn: " + input
    i = _strip(phenny, input)
    #print "l: " + i
    input.brain.learn(i)

learn.rule = r'.*'
learn.priority = 'high'
learn.thread = False


def reply(phenny, input):
    #print "reply: " + input
    r = _strip(phenny, input)
    if r.startswith("reload"): return
    #print "r: " + r
    response = input.brain.reply(r)
    phenny.say(input.nick + ": " + response)

reply.rule = r'$nickname: .*'
reply.priority = 'high'
reply.thread = False


def urllearn(phenny, input):
    print "urllearn: " + input
    if input.admin:
        url = input.lstrip(".urllearn ")
        print "Url: " + url
        if not url.startswith("http://"):
            phenny.say(input.nick + ": Usage: .urllearn http://www.examle.com")
            return

        from useragents import UserAgent
        useragent = UserAgent()
        headers = {}
        headers['Origin'] = url
        headers['Referer'] = 'http://www.google.com'
        headers['Cache-Control'] = 'max-age=0'
        headers['Accept'] = 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8'
        headers['Accept-Language'] = 'sv-SE,en-US,en;q=0.8'
        headers['Accept-Charset'] = 'utf-8,ISO-8859-1;q=0.7,*;q=0.3'
        headers['User-Agent'] = useragent.random()

        redirect_handler = urllib2.HTTPRedirectHandler()
        opener = urllib2.build_opener(redirect_handler,urllib2.HTTPCookieProcessor)
        f = opener.open(urllib2.Request(url=url, headers=headers))
        bs = BeautifulSoup(f.read())
        for s in bs.body.strings:
            print "Learning: " + s
            input.brain.learn(s)

urllearn.rule = r'\.urllearn (\S+)'
urllearn.priority = 'high'
urllearn.thread = False