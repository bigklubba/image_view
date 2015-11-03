#!/usr/bin/env python
#-*- coding:utf-8 -*-


__author__ = 'piem7783'
import gtk
import glob
import sys
import os

MAX_SIZE = 200.0
MAX_HEIGHT = 600
MAX_WIDTH = 600
PADDING = 50
TITLE = "RIR (Rensa i röran)"
types = ('*.png', '*.gif', '*.jpg', '*.jpeg')


class MainWindow():

    def on_key_press(self, widget, event):
        if event.keyval == gtk.keysyms.Right:
            self.next(0)
        elif event.keyval == gtk.keysyms.Left:
            self.prev(0)
        elif event.keyval == gtk.keysyms.Delete:
            self.delete(0)
        elif event.keyval == gtk.keysyms.Up:
            a = self.get_max_height_and_max_width_on_current_monitor()
            global MAX_HEIGHT
            global MAX_WIDTH
            MAX_HEIGHT = a[0]-PADDING
            MAX_WIDTH = a[1]
            self.main_window.resize(MAX_WIDTH, MAX_HEIGHT)

    def next(self, id):
        if len(self.directory_images_paths) == 0:
                return
        
        if self.current_image_index+1 == len(self.directory_images_paths):
                return
        self.current_image_index += 1
        self.set_image()

    def prev(self, id):
        if self.current_image_index == 0:
                return
        self.current_image_index -= 1
        self.set_image()

    def delete(self, id):

        if self.directory_images_paths != 0:
            os.remove(self.directory_images_paths[self.current_image_index])

        if len(self.directory_images_paths) == 0:
                self.current_image_index = 0
                self.current_image.hide()               
                return

        self.directory_images_paths.pop(self.current_image_index)
        if len(self.directory_images_paths) == 0:
                self.current_image_index = 0
                self.current_image.hide()               
                return

        if (self.current_image_index+1) > len(self.directory_images_paths):
            self.current_image_index -= 1
        
        if self.current_image_index >= 0:
                self.set_image()
        else:
                self.current_image.hide()        

    def set_image(self):
        pixbuf = gtk.gdk.pixbuf_new_from_file(self.directory_images_paths[self.current_image_index])
        scaled_size = self.get_scaled_size(pixbuf)

        scaled_buf = pixbuf.scale_simple(scaled_size[1], scaled_size[0], gtk.gdk.INTERP_BILINEAR)
        self.current_image.set_from_pixbuf(scaled_buf)
        self.current_image.show()

    def get_scaled_size(self, pixbuf):
        orig_height = pixbuf.get_height()
        orig_width = pixbuf.get_width()

        if orig_height > orig_width:
            height = MAX_HEIGHT
            width = int(MAX_WIDTH * (orig_width/float(orig_height)))
        else:
            height = int(MAX_HEIGHT * (orig_height/float(orig_width)))
            width = MAX_WIDTH

        return [height, width]

    def get_files(self):
        for files in types:
            self.directory_images_paths.extend(glob.glob(self.path+'/'+files))

    def __init__(self, title="MainWindow", path="."):
        self.path = path
        self.main_window = gtk.Window()
        self.main_window.connect('destroy', self.close_window)
        self.main_window.connect('key_press_event', self.on_key_press)
        self.main_window.set_events(gtk.gdk.KEY_PRESS_MASK)
        self.main_window.set_title(title)
        self.main_window.set_default_size(MAX_HEIGHT + PADDING, MAX_WIDTH + PADDING)
        self.main_window.set_position(gtk.WIN_POS_CENTER)
        self.directory_images_paths=[]
        self.current_image_index=0
        
        self.get_files()
        hbox = gtk.HBox()
        
        vbox = gtk.VBox()
        next_button = gtk.Button()
        next_button.connect('clicked', self.next)
        next_button.set_label("next")
        
        prev_button = gtk.Button()
        prev_button.connect('clicked', self.prev)
        prev_button.set_label("prev")

        del_button = gtk.Button()
        del_button.connect('clicked', self.delete)
        del_button.set_label("delete")

        self.current_image = gtk.Image()
        self.set_image()

        hbox = gtk.HBox()
        hbox.pack_start(prev_button, True, True, 0)
        hbox.pack_start(del_button, True, True, 0)
        hbox.pack_start(next_button, True, True, 0)
        
        vbox.pack_start(self.current_image, True, 0)        
        vbox.pack_start(hbox)
        self.main_window.add(vbox)

    def show(self):
        self.main_window.show_all()

    def get_max_height_and_max_width_on_current_monitor(self):
        screen = self.main_window.get_screen()
        curmonitor = screen.get_monitor_at_window(screen.get_active_window())
        mg = screen.get_monitor_geometry(curmonitor)
        return mg.height, mg.width

    @staticmethod
    def close_window(self):
        gtk.main_quit()


def main():
    if len(sys.argv) > 1:
        main_window = MainWindow(TITLE, sys.argv[1])
    else:
        main_window = MainWindow(TITLE)
    main_window.show()
    gtk.main()

main()
