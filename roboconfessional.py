#!/usr/bin/python

"""
 "THE BEER-WARE LICENSE" (Revision 42):
 <luisfelipe@softwarelivre.org> wrote this file. As long as you retain this notice you
 can do whatever you want with this stuff. If we meet some day, and you think this stuff 
 is worth it, you can buy me a beer in return -- see AUTHORS 
"""

import os
import gst
import gtk
import datetime

# DARPA Affair's video
filename1 = os.getcwd() + '/example.ogv'
uri1 = 'file://' + filename1

# Noisebridge's video
filename2 = os.getcwd() + '/robot_test.ogv'
uri2 = 'file://' + filename2

class Main:
    def __init__(self):
        self.window = gtk.Window()
        self.window.set_position(gtk.WIN_POS_CENTER)
        self.window.fullscreen()
        self.window.set_decorated(False)
        self.vbox = gtk.VBox()
	self.da = gtk.DrawingArea()
	self.bb = gtk.HButtonBox()
	self.da.set_size_request(800,600)
	
	self.playButton = gtk.Button(stock='gtk-media-play')
	self.playButton.set_label("Hear DARPA Faire's position")
	self.playButton.id = self.playButton.connect("clicked", self.play1)       
	self.playButton.set_size_request(200,120)
	
	self.playButton2 = gtk.Button(stock='gtk-media-play')
	self.playButton2.set_label("Hear Noisebridge's position")
	self.playButton2.id = self.playButton2.connect("clicked", self.play2)
	
	self.recordButton = gtk.Button(stock='gtk-media-record')
	self.recordButton.set_label("Tell Us Your Confession")
	self.recordButton.id = self.recordButton.connect("clicked", self.record)

	self.stopButton = gtk.Button(stock='gtk-media-stop')
	self.stopButton.set_label("Stop Everything")
	self.stopButton.connect("clicked", self.stop)

	self.quitButton = gtk.Button(stock='gtk-quit')
	self.quitButton.set_label("Quit")
	self.quitButton.connect("clicked", self.quit)
	
	self.vbox.pack_start(self.da)
	self.bb.add(self.playButton)
	self.bb.add(self.playButton2)
	self.bb.add(self.recordButton)
	self.bb.add(self.stopButton)
	self.bb.add(self.quitButton)
	self.vbox.pack_start(self.bb)
	self.window.add(self.vbox)
        
        # GStreamer pipelines
        self.pipeline1 = gst.Pipeline()
        self.pipeline2 = gst.Pipeline()
	    
        # Bus to get events from GStreamer pipeline
        self.bus = self.pipeline1.get_bus()
        self.bus.add_signal_watch()

	self.bus2 = self.pipeline2.get_bus()
        self.bus2.add_signal_watch()
        
        # Output to drawing area
        self.bus.enable_sync_message_emission()
        self.bus.connect('sync-message::element', self.on_sync_message)

	self.bus2.enable_sync_message_emission()
        self.bus2.connect('sync-message::element', self.on_sync_message)
        
        # Create GStreamer elements
        self.playbin = gst.element_factory_make('playbin2')
        self.playbin2 = gst.element_factory_make('playbin2')

        # Add playbin to pipelines
        self.pipeline1.add(self.playbin)
	self.pipeline2.add(self.playbin2)
	
        # Set properties
        self.playbin.set_property('uri', uri1)
        self.playbin2.set_property('uri', uri2)
        
    def run(self):
        self.window.show_all() 
        self.xid = self.da.window.xid
        gtk.main()
    
    def play1(self, widget):
        self.window.show_all()
        self.pipeline1.set_state(gst.STATE_READY) 
        self.xid = self.da.window.xid
        self.pipeline1.set_state(gst.STATE_PLAYING)
        gtk.main()
        
    def play2(self, widget):
        self.window.show_all()
        self.pipeline2.set_state(gst.STATE_READY)
        self.xid = self.da.window.xid
        self.pipeline2.set_state(gst.STATE_PLAYING)
        gtk.main()
        
    def record(self, widget):
    	suffix = datetime.datetime.now().strftime("%Y%m%d_%H:%M:%S")
	self.recorder = gst.parse_launch("autoaudiosrc ! "
            "audio/x-raw-int,rate=22100,channels=1,depth=16 "
	    "! queue ! audioconvert ! vorbisenc quality=0.2 ! "
            "oggmux ! filesink location=" + os.getcwd() + "/confession_" + suffix + ".ogg")
	self.recorder.set_state(gst.STATE_READY)    
	self.recorder.set_state(gst.STATE_PLAYING)
        gtk.main()
        
    def stop(self, widget):
        self.pipeline1.set_state(gst.STATE_READY)
        self.pipeline2.set_state(gst.STATE_READY)
        self.recorder.set_state(gst.STATE_NULL)
        gtk.main()
        
    def quit(self, widget):
        gtk.main_quit()
    	     
    def on_sync_message(self, bus, msg):
        if msg.structure.get_name() == 'prepare-xwindow-id':
            print('prepare-xwindow-id')
            msg.src.set_property('force-aspect-ratio', True)
            msg.src.set_xwindow_id(self.xid)

p = Main()
p.run()
