import pygtk
pygtk.require('2.0')
import gtk
import threading

import sys
import urllib2
import json
from time import sleep

def get_all_current_event_ids():
    ret = [x for x in json.loads(urllib2.urlopen('https://api.guildwars2.com/v1/events.json?world_id=1021&map_id=15&lang=en').read())['events']]
    return ret

troll_event_id = 'D17D47E9-0A87-4189-B02A-54E23AA91A82'
boar_event_id = '69D031A8-7AD2-4419-B564-48457841A57C'
oak_event_id = '04084490-0117-4D56-8D67-C4FFFE933C0C'
bandit_event_id = 'BC997F15-4C05-4D95-A14F-9B7C4CF41B4E'
wasp_event_id = '3C3915FB-E2E4-4794-A700-E3B5FCFE0404'
zerg_event_ids = [troll_event_id, boar_event_id, oak_event_id, bandit_event_id, wasp_event_id]

class Champion:
    def __init__(self, event_id, event_name, event_status):
        self.event_id = event_id
        self.event_name = event_name
        self.event_status = event_status
    def get_status(self):
        return self.event_status
    def set_status(self, new):
        self.event_status = new
    def __repr__(self):
        return '<Champion-%s-%s-%s>' % (self.event_id, self.event_name, self.event_status)

troll = Champion(troll_event_id, 'Troll', 'Unknown')
boar = Champion(boar_event_id, 'Boar', 'Unknown')
oak = Champion(oak_event_id, 'Oak', 'Unknown')
bandit = Champion(bandit_event_id, 'Bandit', 'Unknown')
wasp = Champion(wasp_event_id, 'Wasp', 'Unknown')
champions = [troll, boar, oak, bandit, wasp]

def event_by_id(event_id):
    for c in champions:
        if c.event_id == event_id:
            return c

def check():
    current_event_ids = get_all_current_event_ids()
    ret = []
    for event in current_event_ids:
        champ = event_by_id(event['event_id'])
        if champ:
            champ.set_status(event['state'])

class Updater(threading.Thread):
	def __init__(self):
		self.running = False
		threading.Thread.__init__(self)
	def run(self):
		self.running = True
		while self.running:
			print 'working'
			sleep(2.5)
	def stop(self):
		self.running = False

class Zerg:
    def update_form(self):
        print 'Form update!'
        pass
    def delete_event_id(self, widget, event, data=None):
        return False
    def destroy(self, widget, data=None):
        self.updater.stop()
        gtk.main_quit()
    def __init__(self):
        self.window = gtk.Window(gtk.WINDOW_TOPLEVEL)
        self.window.connect("destroy", self.destroy)
        self.window.set_border_width(10)
        self.button = gtk.Button("Refresh")
        self.button.connect_object("clicked", gtk.Widget.destroy, self.window)
        self.window.add(self.button)
        
        self.b_troll = gtk.Button('Troll: ' + troll.get_status())
        self.window.add(self.b_troll)
        self.b_boar = gtk.Button('Boar: ' + boar.get_status())
        self.window.add(self.b_boar)
        self.b_oak = gtk.Button('Oak: ' + oak.get_status())
        self.window.add(self.b_oak)
        self.b_bandit = gtk.Button('Bandit: ' + bandit.get_status())
        self.window.add(self.b_bandit)
        self.b_wasp = gtk.Button('Wasp: ' + wasp.get_status())
        self.window.add(self.b_wasp)
        
        self.button.show()
        self.window.show()
        self.updater = Updater()
        self.updater.start()
    def main(self):
        gtk.main()

zerg = None
if __name__ == "__main__":
    zerg = Zerg()
    zerg.main()
