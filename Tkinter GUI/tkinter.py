# -*- coding: utf-8 -*-
__author__ = 'imressed'

import ConfigParser
import tkMessageBox
from Tkinter import *
from ttk import LabelFrame, Notebook, Checkbutton, Scrollbar, Separator
from event_proxy.utils import read_main_config # this method simply read config using ConfigParser


class Model(object):
    def __init__(self, config_route):
        self.config = read_main_config(config_route)
        self.config_route = config_route
    def get_config(self):
        return self.config

    def get_channels(self):
        return self.config['channels']

    def get_updated_config(self):
        return read_main_config(self.config_route)

    def get_config_route(self):
        return self.config_route


class View(Toplevel):
    def __init__(self, model):
        self.model = model
        self.model_config = self.model.get_config()
        self.channels_num = 0
        self.channels_amount = 0

        self.root = Tk()
        self.root.resizable(width=FALSE, height=FALSE)
        self.root.title("RaaS. event_proxy configurator")
        #: self.root.iconbitmap('resourse/vit.ico')
        self.config_route = self.model.get_config_route()

        self.panelFrame = Frame(self.root, height=60)
        self.canvas = Canvas(self.root, borderwidth=0)
        self.textFrame = Frame(self.canvas, height=340, width=600)
        self.mainFrame = LabelFrame(self.root, width=200, text="Main:",
                                    height=340, relief=RAISED, borderwidth=1)
        self.chanelFrame = LabelFrame(self.root, width=370, text="Channels:",
                                      height=340, relief=RAISED, borderwidth=1)

        #: self.vsb = Scrollbar(self.root, orient="horizontal",
        #:                     command=self.canvas.xview)
        #:self.canvas.configure(xscrollcommand=self.vsb.set)
        #:self.vsb.pack(side="bottom", fill="x")
        self.canvas.pack(side="bottom", fill="both", expand=True)
        self.canvas.configure(scrollregion=self.canvas.bbox("all"))
        self.root.protocol("WM_DELETE_WINDOW", self.quit_handler)

        self.tabs = Notebook(self.root)
        self.in_channel_text = []
        self.out_port_text = []
        self.out_channel_text = []

        self.c = self.model.get_channels().keys()
        self.channels_len = len(self.model.get_channels())
        #:print self.model.get_channels()
        self.panelFrame.pack(side='top', fill='x')
        self.textFrame.pack(side='bottom', fill='both', expand=1)
        self.mainFrame.place(x=10, y=60)
        self.chanelFrame.place(x=220, y=60)
        self.tabs.place(x=230, y=80)

        x = (self.root.winfo_screenwidth() - self.root.winfo_reqwidth()) / 2
        y = (self.root.winfo_screenheight() - self.root.winfo_reqheight()) / 2
        self.root.geometry("+%d+%d" % (x-150, y-150))

        for i in range(self.channels_len):
            self.channels_num += 1
            self.channels_amount += 1

            self.f1 = Frame(self.tabs, height=290, width=350)
            self.tabs.add(self.f1, text='Channel {0}'.format(i + 1))

            self.in_channel = Label(self.f1, text="In channel")
            self.out_port = Label(self.f1, text="Out port")
            self.out_channel = Label(self.f1, text="Out channel")

            self.in_channel_text.append(Entry(self.f1, width=20, bd=3))
            self.in_channel_text[i].insert(0, self.c[i])

            self.out_port_text.append(Entry(self.f1, width=20, bd=3))
            self.out_port_text[i].insert(0, self.model.get_channels()[
                self.c[i]].out_port)

            self.out_channel_text.append(Entry(self.f1, width=20, bd=3))
            self.out_channel_text[i].insert(0, self.model.get_channels()[
                self.c[i]].out_channel)

            self.in_channel.place(x=5, y=10)
            self.in_channel_text[i].place(x=5, y=30)

            self.out_port.place(x=5, y=50)
            self.out_port_text[i].place(x=5, y=70)

            self.out_channel.place(x=5, y=90)
            self.out_channel_text[i].place(x=5, y=110)

            self.del_ch_btn = Button(self.f1, text='Delete channel {0}'.format(
                self.channels_amount),
                                     command=
                                     lambda: self.del_channel(i))
            self.del_ch_btn.bind("<Button-1>")
            self.del_ch_btn.place(x=5, y=140, width=100, height=30)

        self.server_host_label = Label(self.root, text="Server host")
        self.server_port_label = Label(self.root, text="Server port")
        self.raas_port_label = Label(self.root, text="Raas port")
        self.encoding_label = Label(self.root, text='Encoding')
        self.levenshtein_distance_label = Label(self.root,
                                                text='Levenshtein distance')
        self.window_time_label = Label(self.root, text='Window time')

        self.server_host_entity = Entry(self.root, width=20, bd=3)
        self.server_host_entity.insert(0, self.model_config['server_host'])

        self.server_port_entity = Entry(self.root, width=20, bd=3)
        self.server_port_entity.insert(0, self.model_config['server_port'])

        self.raas_port_entity = Entry(self.root, width=20, bd=3)
        self.raas_port_entity.insert(0, self.model_config['raas_port'])

        self.encoding_entry = Entry(self.root, width=20, bd=3)
        self.encoding_entry.insert(0, self.model_config['encoding'])

        self.levenshtein_distance_entry = Entry(self.root, width=20, bd=3)
        self.levenshtein_distance_entry.insert(0, self.model_config[
            'levenshtein_distance'])

        self.window_time_entry = Entry(self.root, width=20, bd=3)
        self.window_time_entry.insert(0, self.model_config['window_time'])

        self.var = IntVar()
        self.cfg_debug = self.model_config['debug']
        if self.cfg_debug == 'True':
            self.var.set(1)
        else:
            self.var.set(0)
        self.check_debug = Checkbutton(self.root, text='Debug',
                                       variable=self.var)

        self.filter_var = IntVar()
        self.cfg_use_filter = self.model_config['use_filter']
        if self.cfg_use_filter == 'True':
            self.filter_var.set(1)
        else:
            self.filter_var.set(0)
        self.check_use_filter = Checkbutton(self.root, text='Use filter',
                                            variable=self.filter_var)

        self.addBtn = Button(self.panelFrame, text='Add channel')
        self.saveBtn = Button(self.panelFrame, text='Save')
        self.quitBtn = Button(self.panelFrame, text='Quit')

        self.saveBtn.bind("<Button-1>", self.SaveFile)
        self.quitBtn.bind("<Button-1>", self.Quit)
        self.addBtn.bind("<Button-1>", self.add_channel)

        self.saveBtn.place(x=10, y=10, width=40, height=40)
        self.quitBtn.place(x=60, y=10, width=40, height=40)
        self.addBtn.place(x=220, y=10, width=80, height=40)

        self.server_host_label.place(x=20, y=80)
        self.server_host_entity.place(x=20, y=100)

        self.server_port_label.place(x=20, y=120)
        self.server_port_entity.place(x=20, y=140)

        self.raas_port_label.place(x=20, y=160)
        self.raas_port_entity.place(x=20, y=180)

        self.encoding_label.place(x=20, y=200)
        self.encoding_entry.place(x=20, y=220)

        self.check_debug.place(x=20, y=250)
        self.f = Frame(self.root, height=1, width=190, bg='grey')
        self.f.place(x=15, y=275)

        self.levenshtein_distance_label.place(x=20, y=280)
        self.levenshtein_distance_entry.place(x=20, y=300)

        self.window_time_label.place(x=20, y=320)
        self.window_time_entry.place(x=20, y=340)

        self.check_use_filter.place(x=20, y=370)

    def del_channel(self, numb):
        rwidth = self.root.winfo_width()
        rheight = self.root.winfo_height()
        if self.channels_num > 6:
            self.chanelFrame.config(width=self.chanelFrame.winfo_width() - 65)
            self.root.geometry("%dx%d" % (rwidth - 65, rheight))

        if self.channels_num == 6:
            self.chanelFrame.config(width=self.chanelFrame.winfo_width() - 20)
            self.root.geometry("%dx%d" % (rwidth - 20, rheight))

        dvar = self.tabs.tabs().index(self.tabs.select())

        self.in_channel_text.pop(dvar)
        self.out_channel_text.pop(dvar)
        self.out_port_text.pop(dvar)
        self.channels_num -= 1
        self.tabs.forget(self.tabs.select())

        tabs_list = self.tabs.tabs()
        self.root.update()

    def add_channel(self, env):
        if self.channels_num > 15:
            tkMessageBox.showerror('Error',
                                   'You can not add more than 16 channels')
            return False

        rwidth = self.root.winfo_width()
        rheight = self.root.winfo_height()

        if self.channels_num == 5:
            self.chanelFrame.config(width=self.chanelFrame.winfo_width() + 20)
            self.root.geometry("%dx%d" % (rwidth + 20, rheight))

        if self.channels_num > 5:
            self.chanelFrame.config(width=self.chanelFrame.winfo_width() + 65)
            self.root.geometry("%dx%d" % (rwidth + 65, rheight))

        self.f1 = Frame(self.tabs, height=290, width=350)
        self.tabs.add(self.f1,
                      text='Channel {0}'.format(self.channels_amount + 1))

        self.in_channel = Label(self.f1, text="In channel")
        self.out_port = Label(self.f1, text="Out port")
        self.out_channel = Label(self.f1, text="Out channel")

        self.in_channel_text.append(Entry(self.f1, width=20, bd=3))

        self.out_port_text.append(Entry(self.f1, width=20, bd=3))

        self.out_channel_text.append(Entry(self.f1, width=20, bd=3))

        self.in_channel.place(x=5, y=10)
        self.in_channel_text[self.channels_num].place(x=5, y=30)

        self.out_port.place(x=5, y=50)
        self.out_port_text[self.channels_num].place(x=5, y=70)

        self.out_channel.place(x=5, y=90)
        self.out_channel_text[self.channels_num].place(x=5, y=110)

        self.del_ch_btn = Button(self.f1, text='Delete channel {0}'.format(
            self.channels_num + 1),
                                 command=
                                 lambda: self.del_channel(self.channels_num))
        self.del_ch_btn.bind("<Button-1>")
        self.del_ch_btn.place(x=5, y=140, width=100, height=30)

        self.channels_num += 1
        self.channels_amount += 1

    def Quit(self, env):
        if tkMessageBox.askyesno('Quit', 'Whant to save config before quit?'):
            self.SaveFile(env)
        self.root.destroy()

    def quit_handler(self):
        if tkMessageBox.askyesno('Quit', 'Whant to save config before quit?'):
            self.save_handler()
        self.root.destroy()

    def validate_int(self, var, text, channel):
        if not var.isdigit():
            tkMessageBox.showerror("Error",
                                   "Error in {1}. Value of field '{0}' must be int.".format(text, channel))
            return False
        return True

    def validate_empty(self, var, text):
        if not var:
            tkMessageBox.showerror("Error",
                                   "Field {0} must be not empty.".format(text))
            return False
        return True

    def validate_channels(self):
        if not self.channels_num:
            tkMessageBox.showerror("Error",
                                   "You must add at least one channel")
            return False
        return True

    def validate_change_field(self):
        self.validating_config = self.model.get_updated_config()
        self.flag = False
        if self.server_host_entity.get() != str(self.validating_config['server_host']):
            self.flag = True
        if self.server_port_entity.get() != str(self.validating_config['server_port']):
            self.flag = True
        if self.raas_port_entity.get() != str(self.validating_config['raas_port']):
            self.flag = True
        if self.encoding_entry.get() != str(self.validating_config['encoding']):
            self.flag = True
        if str(self.levenshtein_distance_entry.get()) != str(self.validating_config['levenshtein_distance']):
            self.flag = True
        if str(self.window_time_entry.get()) != str(self.validating_config['window_time']):
            self.flag = True
        self.tmp = IntVar()
        if self.validating_config['debug'] == 'True':
            self.tmp.set(1)
        else:
            self.tmp.set(0)
        if self.tmp.get() != self.var.get():
            self.flag = True
        self.tmp_filter = IntVar()
        if self.validating_config['use_filter'] == 'True':
            self.tmp_filter.set(1)
        else:
            self.tmp_filter.set(0)
        if self.tmp_filter.get() != self.filter_var.get():
            self.flag = True
        #TODO: add validating of channels
        if self.channels_num != self.channels_amount or self.channels_len != self.channels_num:
            return True
        for i in range(self.channels_num):
            if self.in_channel_text[i].get() != str(self.c[i]):
                self.flag = True
            if self.out_port_text[i].get() != str(self.model.get_channels()[
                self.c[i]].out_port):
                self.flag = True
            if self.out_channel_text[i].get() != str(self.model.get_channels()[
                self.c[i]].out_channel):
                self.flag = True
        return self.flag

    def validate_all(self):
        #if not self.validate_change_field():
        #    return False
        if not self.validate_channels():
            return False
        if not self.validate_empty(self.server_host_entity.get(),
                                   'Server host'):
            return False
        if not self.validate_empty(self.encoding_entry.get(), 'Encoding'):
            return False
        if not self.validate_empty(self.levenshtein_distance_entry.get(),
                                   'Levenshtein distance'):
            return False
        if not self.validate_int(self.server_port_entity.get(), 'Server port',
                                 ''):
            return False
        if not self.validate_int(self.raas_port_entity.get(), 'Raas port', ''):
            return False
        if not self.validate_int(self.levenshtein_distance_entry.get(),
                                 'Levenshtein distance', ''):
            return False
        if not self.validate_int(self.window_time_entry.get(), 'Window time',
                                 ''):
            return False
        for i in range(self.channels_num):
            if not self.validate_int(self.in_channel_text[i].get(),
                                     'In channel',
                                     ' Channel {0}'.format(i + 1)):
                return False
            if not self.validate_int(self.out_port_text[i].get(), 'Out port',
                                     ' Channel {0}'.format(i + 1)):
                return False
            if not self.validate_int(self.out_channel_text[i].get(),
                                     'Out channel',
                                     ' Channel {0}'.format(i + 1)):
                return False
        return True

    def SaveFile(self, env):
        self.save_handler()

    def save_handler(self):
        if not self.validate_all():
            return False

        config = ConfigParser.RawConfigParser()
        config.add_section('Main')
        config.set('Main', 'server_host', self.server_host_entity.get())
        config.set('Main', 'server_port', self.server_port_entity.get())
        config.set('Main', 'raas_port', self.raas_port_entity.get())
        result = 'False'
        if self.var.get():
            result = 'True'
        config.set('Main', 'debug', result)
        config.set('Main', 'encoding', self.encoding_entry.get())
        config.set('Main', 'levenshtein_distance',
                   self.levenshtein_distance_entry.get())
        config.set('Main', 'window_time', self.window_time_entry.get())
        result_filter = 'False'
        if self.filter_var.get():
            result_filter = 'True'
        config.set('Main', 'use_filter', result_filter)

        for i in range(self.channels_num):
            config.add_section('Channel{0}'.format(i + 1))
            config.set('Channel{0}'.format(i + 1), 'in_channel',
                       self.in_channel_text[i].get())
            config.set('Channel{0}'.format(i + 1), 'out_port',
                       self.out_port_text[i].get())
            config.set('Channel{0}'.format(i + 1), 'out_channel',
                       self.out_channel_text[i].get())

        with open(self.config_route, 'wb') as configfile:
            config.write(configfile)
        tkMessageBox.showinfo("Info", "Successfully saved.")

    def run(self):
        self.root.mainloop()


class Controller(object):
    def __init__(self, config_route):
        self.model = Model(config_route)
        self.view = View(self.model)
        self.view.run()