#!/usr/bin/env python

from time import sleep
from urllib2 import urlopen

from circuits.web import Controller
from circuits import future, Event, Component

class Hello(Event):
    """Hello Event"""

class Test(Component):

    def hello(self):
        return "Hello World!"

class Root(Controller):

    @future()
    def index(self):
        sleep(1)
        return self.push(Hello())

def test(webapp):
    Test().register(webapp)

    f = urlopen(webapp.server.base)
    s = f.read()
    assert s == "Hello World!"