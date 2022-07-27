import json
import pathlib
import sys
import time
import os

from PyQt5.QtCore import QUrl, Qt
from PyQt5.QtWidgets import QApplication, QMainWindow, QShortcut, QAction, QErrorMessage, QMenuBar
from PyQt5.QtWebEngineWidgets import QWebEngineView, QWebEngineProfile, QWebEnginePage
from PyQt5.QtGui import QKeySequence, QIcon

from tkinter import Tk, ttk, Frame, Label, Entry, Button, X, W, LEFT, RIGHT, END
from tkinter import messagebox

import random

import threading

import win32gui
import win32con
import win32api

url = "https://universe.flyff.com/play"
icon = "icons/PyFlyff.ico"

default_user_agent = "None"

mini_ftool_activation_key = ""

alt_control_key_list_1 = []
alt_control_key_list_2 = []
profile_list = []

mini_ftool_window_name = ""
hwndMain = ""
hwndAlt = ""
alt_window_name = ""
user_agent = ""

mini_ftool_repeat_times = 0

start_mini_ftool_loop = False
alt_control_boolean = False
menubar_window = False
can_reload_client = False
is_on_top = False

data_folder = "C:/PyFlyff"
profile_file_location = "C:/PyFlyff/profiles.txt"

mini_ftool_json_file = "MiniFToolConfig.json"
mini_ftool_json_file_location = pathlib.Path(mini_ftool_json_file)

alt_control_json_file = "AltControl.json"
alt_control_json_file_location = pathlib.Path(alt_control_json_file)

user_agent_json_file = "UserAgent.json"
user_agent_json_file_location = pathlib.Path(user_agent_json_file)

vk_code = {'backspace': 0x08,
           'tab': 0x09,
           'clear': 0x0C,
           'enter': 0x0D,
           'shift': 0x10,
           'ctrl': 0x11,
           'alt': 0x12,
           'pause': 0x13,
           'caps_lock': 0x14,
           'esc': 0x1B,
           'spacebar': 0x20,
           'page_up': 0x21,
           'page_down': 0x22,
           'end': 0x23,
           'home': 0x24,
           'left_arrow': 0x25,
           'up_arrow': 0x26,
           'right_arrow': 0x27,
           'down_arrow': 0x28,
           'select': 0x29,
           'print': 0x2A,
           'execute': 0x2B,
           'print_screen': 0x2C,
           'ins': 0x2D,
           'del': 0x2E,
           'help': 0x2F,
           '0': 0x30,
           '1': 0x31,
           '2': 0x32,
           '3': 0x33,
           '4': 0x34,
           '5': 0x35,
           '6': 0x36,
           '7': 0x37,
           '8': 0x38,
           '9': 0x39,
           'a': 0x41,
           'b': 0x42,
           'c': 0x43,
           'd': 0x44,
           'e': 0x45,
           'f': 0x46,
           'g': 0x47,
           'h': 0x48,
           'i': 0x49,
           'j': 0x4A,
           'k': 0x4B,
           'l': 0x4C,
           'm': 0x4D,
           'n': 0x4E,
           'o': 0x4F,
           'p': 0x50,
           'q': 0x51,
           'r': 0x52,
           's': 0x53,
           't': 0x54,
           'u': 0x55,
           'v': 0x56,
           'w': 0x57,
           'x': 0x58,
           'y': 0x59,
           'z': 0x5A,
           'numpad_0': 0x60,
           'numpad_1': 0x61,
           'numpad_2': 0x62,
           'numpad_3': 0x63,
           'numpad_4': 0x64,
           'numpad_5': 0x65,
           'numpad_6': 0x66,
           'numpad_7': 0x67,
           'numpad_8': 0x68,
           'numpad_9': 0x69,
           'multiply_key': 0x6A,
           'add_key': 0x6B,
           'separator_key': 0x6C,
           'subtract_key': 0x6D,
           'decimal_key': 0x6E,
           'divide_key': 0x6F,
           'f1': 0x70,
           'f2': 0x71,
           'f3': 0x72,
           'f4': 0x73,
           'f5': 0x74,
           'f6': 0x75,
           'f7': 0x76,
           'f8': 0x77,
           'f9': 0x78,
           'f10': 0x79,
           'f11': 0x7A,
           'f12': 0x7B,
           'f13': 0x7C,
           'f14': 0x7D,
           'f15': 0x7E,
           'f16': 0x7F,
           'f17': 0x80,
           'f18': 0x81,
           'f19': 0x82,
           'f20': 0x83,
           'f21': 0x84,
           'f22': 0x85,
           'f23': 0x86,
           'f24': 0x87,
           'num_lock': 0x90,
           'scroll_lock': 0x91,
           'left_shift': 0xA0,
           'right_shift ': 0xA1,
           'left_control': 0xA2,
           'right_control': 0xA3,
           'left_menu': 0xA4,
           'right_menu': 0xA5,
           'browser_back': 0xA6,
           'browser_forward': 0xA7,
           'browser_refresh': 0xA8,
           'browser_stop': 0xA9,
           'browser_search': 0xAA,
           'browser_favorites': 0xAB,
           'browser_start_and_home': 0xAC,
           'volume_mute': 0xAD,
           'volume_Down': 0xAE,
           'volume_up': 0xAF,
           'next_track': 0xB0,
           'previous_track': 0xB1,
           'stop_media': 0xB2,
           'play/pause_media': 0xB3,
           'start_mail': 0xB4,
           'select_media': 0xB5,
           'start_application_1': 0xB6,
           'start_application_2': 0xB7,
           'attn_key': 0xF6,
           'crsel_key': 0xF7,
           'exsel_key': 0xF8,
           'play_key': 0xFA,
           'zoom_key': 0xFB,
           'clear_key': 0xFE,
           '+': 0xBB,
           ',': 0xBC,
           '-': 0xBD,
           '.': 0xBE,
           '/': 0xBF,
           '`': 0xC0,
           ';': 0xBA,
           '[': 0xDB,
           '\\': 0xDC,
           ']': 0xDD,
           "'": 0xDE}


class MainWindow(QMainWindow):
    def __init__(self):

        global user_agent
        global can_reload_client

        super(MainWindow, self).__init__()

        self.browser = None
        self.setWindowIcon(QIcon(icon))
        self.setMinimumSize(640, 480)
        self.showMaximized()

        self.menu_bar = QMenuBar()
        self.menu_bar.setNativeMenuBar(False)
        self.setMenuBar(self.menu_bar)

        ftool = QAction("Mini FTool", self)
        ftool.triggered.connect(lambda: self.multithreading(self.ftool_config))

        alt_control = QAction("Alt Control", self)
        alt_control.triggered.connect(lambda: self.multithreading(self.alt_control_config))

        clear_keys = QAction("Reset Hotkeys", self)
        clear_keys.triggered.connect(self.reset_hotkeys)

        menu_tools = self.menu_bar.addMenu("Tools")
        menu_tools.addAction(ftool)
        menu_tools.addAction(alt_control)
        menu_tools.addAction(clear_keys)

        q_action_user_agent = QAction("Set User Agent", self)
        q_action_user_agent.setToolTip("Change your User Agent to something else if you are having trouble "
                                       "connecting your Google Account/Facebook Account/Apple ID, "
                                       "or connecting to the game as a whole.")

        q_action_user_agent.triggered.connect(lambda: self.multithreading(self.set_user_agent))

        q_action_fullscreen = QAction("Fullscreen | Ctrl+Shift+F11", self)
        q_action_fullscreen.triggered.connect(self.fullscreen)

        q_action_open_alt_client = QAction("Open Alt Client | Ctrl+Shift+PageUp", self)
        q_action_open_alt_client.triggered.connect(lambda: self.create_open_client_profile("Alt"))

        q_action_change_main_client_profile = QAction("Change Main Client Profile", self)
        q_action_change_main_client_profile.triggered.connect(lambda: self.create_open_client_profile("Main"))

        self.q_action_always_on_top = QAction("Always on Top: Off", self)
        self.q_action_always_on_top.triggered.connect(self.always_on_top)

        menu_client = self.menu_bar.addMenu("Client")
        menu_client.addAction(q_action_user_agent)
        menu_client.addAction(q_action_fullscreen)
        menu_client.addAction(q_action_open_alt_client)
        menu_client.addAction(q_action_change_main_client_profile)
        menu_client.addAction(self.q_action_always_on_top)
        menu_client.setToolTipsVisible(True)

        q_action_flyffipedia = QAction("Flyffipedia", self)
        q_action_flyffipedia.triggered.connect(
            lambda: self.create_new_window("https://flyffipedia.com/", "Flyffipedia"))

        q_action_madrigalinside = QAction("Madrigal Inside", self)
        q_action_madrigalinside.triggered.connect(
            lambda: self.create_new_window("https://madrigalinside.com/", "Madrigal Inside"))

        q_action_flyffulator = QAction("Flyffulator", self)
        q_action_flyffulator.triggered.connect(
            lambda: self.create_new_window("https://flyffulator.com/", "Flyffulator"))

        q_action_madrigalmaps = QAction("Madrigal Maps", self)
        q_action_madrigalmaps.triggered.connect(
            lambda: self.create_new_window("https://www.madrigalmaps.com/", "Madrigal Maps"))

        q_action_flyffmodelviewer = QAction("Flyff Model Viewer", self)
        q_action_flyffmodelviewer.triggered.connect(
            lambda: self.create_new_window("https://flyffmodelviewer.com/", "Flyff Model Viewer"))

        q_action_skillulator = QAction("Skillulator", self)
        q_action_skillulator.triggered.connect(
            lambda: self.create_new_window("https://skillulator.com/", "Skillulator"))

        menu_community = self.menu_bar.addMenu("Community")
        menu_community.addAction(q_action_flyffipedia)
        menu_community.addAction(q_action_madrigalmaps)
        menu_community.addAction(q_action_flyffulator)
        menu_community.addAction(q_action_madrigalmaps)
        menu_community.addAction(q_action_flyffmodelviewer)
        menu_community.addAction(q_action_skillulator)

        self.reload_client = QShortcut(QKeySequence("Ctrl+Shift+F5"), self)
        self.reload_client.activated.connect(self.reload_main_client)

        self.change_fullscreen = QShortcut(QKeySequence("Ctrl+Shift+F11"), self)
        self.change_fullscreen.activated.connect(self.fullscreen)

        self.new_client = QShortcut(QKeySequence("Ctrl+Shift+PgUp"), self)
        self.new_client.activated.connect(lambda: self.create_open_client_profile("Alt"))

        self.create_shortcuts()

        self.windows = []

        self.create_open_client_profile("Main")

    def create_new_window(self, link, wn):
        new_window = QWebEngineView()
        new_window.setAttribute(Qt.WA_DeleteOnClose)
        new_window.destroyed.connect(lambda: self.windows.remove(new_window))

        client_folder = "C:/PyFlyff/" + wn.replace(" ", "")

        alt_profile = QWebEngineProfile(wn.replace(" ", ""), new_window)
        alt_profile.setCachePath(client_folder)
        alt_profile.setPersistentStoragePath(client_folder)
        alt_page = QWebEnginePage(alt_profile, new_window)

        new_window.setPage(alt_page)
        new_window.load(QUrl(link))
        new_window.setWindowTitle("PyFlyff - " + wn)
        new_window.setWindowIcon(QIcon(icon))
        new_window.setMinimumSize(640, 480)
        new_window.showMaximized()

        new_window.page().profile().setHttpUserAgent(self.load_user_agent())

        self.windows.append(new_window)

    def fullscreen(self):
        if self.isFullScreen():
            self.showMaximized()
            self.menu_bar.setVisible(True)
        else:
            self.showFullScreen()
            self.menu_bar.setVisible(False)

    def ftool_loop(self):
        global start_mini_ftool_loop
        global hwndMain

        counter = 0
        extra_key_time_1 = 0
        extra_key_time_2 = 0

        try:
            while True:

                if counter < mini_ftool_repeat_times and start_mini_ftool_loop is True:

                    self.winapi(hwndMain, globals()["mini_ftool_in_game_key_1"])

                    random_wait = random.uniform(0, globals()["mini_ftool_interval_1"])

                    extra_key_time_1 = extra_key_time_1 + random_wait
                    extra_key_time_2 = extra_key_time_2 + random_wait

                    if globals()["mini_ftool_in_game_key_2"] and globals()["mini_ftool_interval_2"]:
                        if extra_key_time_1 >= globals()["mini_ftool_interval_2"]:
                            self.winapi(hwndMain, globals()["mini_ftool_in_game_key_2"])
                            extra_key_time_1 = 0

                    if globals()["mini_ftool_in_game_key_3"] and globals()["mini_ftool_interval_3"]:
                        if extra_key_time_2 >= globals()["mini_ftool_interval_3"]:
                            self.winapi(hwndMain, globals()["mini_ftool_in_game_key_3"])
                            extra_key_time_2 = 0

                    time.sleep(random_wait)

                    counter += 1
                else:
                    start_mini_ftool_loop = False
                    break

        except Exception as e:
            messagebox.showerror("Error", str(e))

    def start_ftool(self):
        global start_mini_ftool_loop
        global hwndMain
        global mini_ftool_window_name

        hwndMain = win32gui.FindWindow(None, "PyFlyff - " + mini_ftool_window_name)

        if not start_mini_ftool_loop:
            if mini_ftool_activation_key != "" and globals()["mini_ftool_in_game_key_1"] != "":
                start_mini_ftool_loop = True
                self.multithreading(self.ftool_loop)
        else:
            start_mini_ftool_loop = False

    def ftool_config(self):
        global menubar_window
        global profile_list

        if not menubar_window:

            menubar_window = True

            ftool_config_window = Tk()

            window_width = 300
            window_height = 250

            screen_width = ftool_config_window.winfo_screenwidth()
            screen_height = ftool_config_window.winfo_screenheight()

            x = (screen_width / 2) - (window_width / 2)
            y = (screen_height / 2) - (window_height / 2)

            ftool_config_window.geometry("300x250+" + str(int(x)) + "+" + str(int(y)))
            ftool_config_window.minsize(300, 250)
            ftool_config_window.attributes("-topmost", True)
            ftool_config_window.title("Mini Ftool")
            ftool_config_window.iconbitmap(icon)

            def save():
                global mini_ftool_activation_key
                global alt_control_key_list_1
                global mini_ftool_repeat_times
                global mini_ftool_window_name
                global vk_code
                global menubar_window
                global mini_ftool_json_file

                globals()["mini_ftool_in_game_key_1"] = ""
                globals()["mini_ftool_in_game_key_2"] = ""
                globals()["mini_ftool_in_game_key_3"] = ""

                aux = activation_key_entry.get()

                activation_key_entry.delete(0, END)
                activation_key_entry.insert(0, aux.replace(" ", "").lower())

                aux = in_game_hotkey_entry.get()

                in_game_hotkey_entry.delete(0, END)
                in_game_hotkey_entry.insert(0, aux.replace(" ", "").lower())

                try:

                    list_keys = in_game_hotkey_entry.get().split(",")
                    list_interval = interval_entry.get().split(",")

                    if "" in list_keys:
                        list_keys.remove("")
                    if "" in list_interval:
                        list_interval.remove("")

                    if (activation_key_entry.get()
                        and in_game_hotkey_entry.get()
                        and repeat_times_entry.get()
                        and interval_entry.get()
                        and window_combobox.get()) == "":

                        messagebox.showerror("Error", "Fields cannot be empty.")

                    elif any(i for i in list_interval if float(i) < 0):

                        messagebox.showerror("Error", "Intervals cannot be lower than zero.")

                    elif activation_key_entry.get() in list_keys:

                        messagebox.showerror("Error", "Activation Key and In-game Hotkey must be different.")

                    elif activation_key_entry.get() in alt_control_key_list_1:

                        messagebox.showerror("Error", "Main Client HotKey from Alt Control "
                                                      "cannot be the same as the Mini Ftool Activation Key.")
                    elif len(list_keys) != len(list_interval):

                        messagebox.showerror("Error",
                                             "In-Game Hotkey(s) and Interval(s) must have the same "
                                             "amount of values (3 keys for 3 intervals)")
                    else:
                        key_counter = 1
                        interval_counter = 1

                        for key in list_keys:
                            globals()["mini_ftool_in_game_key_" + str(key_counter)] = vk_code.get(key)
                            key_counter += 1
                            if key_counter > len(list_keys):
                                break

                        for interval in list_interval:
                            globals()["mini_ftool_interval_" + str(interval_counter)] = float(interval)
                            interval_counter += 1
                            if interval_counter > len(list_interval):
                                break

                        mini_ftool_activation_key = activation_key_entry.get()
                        mini_ftool_repeat_times = int(repeat_times_entry.get())
                        mini_ftool_window_name = window_combobox.get()

                        self.ftool_key.setKey(mini_ftool_activation_key)

                        self.save_config_json(file=mini_ftool_json_file, values=(
                            activation_key_entry.get(), in_game_hotkey_entry.get(), repeat_times_entry.get(),
                            interval_entry.get(), window_combobox.get()))

                        window_combobox["values"] = self.save_alt_profiles(window_combobox.get())

                        menubar_window = False
                        ftool_config_window.destroy()

                except Exception as e:
                    messagebox.showerror("Error", str(e))

            self.load_alt_profiles()

            explanation_label = Label(ftool_config_window, text="To stop the Mini Ftool, press the activation"
                                                                "\nkey again.", anchor=W, justify="left")
            explanation_label.pack(fill=X, padx=5, pady=5)

            frame = Frame(ftool_config_window)

            frame.pack(fill=X, padx=5, pady=5)

            activation_key_label = Label(frame, text="Activation Key:", width=22, anchor=W)
            activation_key_entry = Entry(frame, width=20)

            in_game_hotkey_label = Label(frame, text="In-Game Hotkey(s):", width=22, anchor=W)
            in_game_hotkey_entry = Entry(frame, width=20)

            repeat_times_label = Label(frame, text="Repeat:", width=22, anchor=W)
            repeat_times_entry = Entry(frame, width=20)

            interval_label = Label(frame, text="Interval(s):", width=22, anchor=W)
            interval_entry = Entry(frame, width=20)

            window_label = Label(frame, text="Profile Name:", width=22, anchor=W)
            window_combobox = ttk.Combobox(frame, values=profile_list, width=17)

            activation_key_label.grid(row=0, column=0, pady=5)
            activation_key_entry.grid(row=0, column=1, pady=5)

            in_game_hotkey_label.grid(row=1, column=0, pady=5)
            in_game_hotkey_entry.grid(row=1, column=1, pady=5)

            repeat_times_label.grid(row=2, column=0, pady=5)
            repeat_times_entry.grid(row=2, column=1, pady=5)

            interval_label.grid(row=3, column=0, pady=5)
            interval_entry.grid(row=3, column=1, pady=5)

            window_label.grid(row=4, column=0, pady=5)
            window_combobox.grid(row=4, column=1, pady=5)

            button_save = Button(text="Save", width=10, height=1, command=save)
            button_save.pack()

            try:
                if mini_ftool_json_file_location.exists():
                    with open(mini_ftool_json_file_location) as js:
                        data = json.load(js)

                        activation_key_entry.insert(0, data["activation_key"])
                        in_game_hotkey_entry.insert(0, data["in_game_key"])
                        repeat_times_entry.insert(0, data["repeat_times"])
                        interval_entry.insert(0, data["interval"])
                        window_combobox.insert(0, data["window"])
            except Exception as e:
                messagebox.showerror("Error", str(e))

            ftool_config_window.wm_protocol("WM_DELETE_WINDOW",
                                            lambda: self.destroy_toolbar_windows(ftool_config_window))
            ftool_config_window.mainloop()

    def alt_control_config(self):
        global menubar_window
        global profile_list

        if not menubar_window:

            menubar_window = True

            alt_control_config_window = Tk()

            window_width = 300
            window_height = 280

            screen_width = alt_control_config_window.winfo_screenwidth()
            screen_height = alt_control_config_window.winfo_screenheight()

            x = (screen_width / 2) - (window_width / 2)
            y = (screen_height / 2) - (window_height / 2)

            alt_control_config_window.geometry("300x280+" + str(int(x)) + "+" + str(int(y)))
            alt_control_config_window.minsize(300, 280)
            alt_control_config_window.attributes("-topmost", True)
            alt_control_config_window.title("Alt Control")
            alt_control_config_window.iconbitmap(icon)

            def start():
                global mini_ftool_activation_key
                global vk_code
                global alt_control_boolean
                global menubar_window
                global alt_window_name
                global alt_control_json_file
                global alt_control_key_list_1
                global alt_control_key_list_2

                self.clear_alt_control_shortcut_keys()

                aux = main_client_hotkey_entry.get()

                main_client_hotkey_entry.delete(0, END)
                main_client_hotkey_entry.insert(0, aux.replace(" ", "").lower())

                aux = alt_client_hotkey_entry.get()

                alt_client_hotkey_entry.delete(0, END)
                alt_client_hotkey_entry.insert(0, aux.replace(" ", "").lower())

                alt_control_key_list_1 = main_client_hotkey_entry.get().split(",")
                alt_control_key_list_2 = alt_client_hotkey_entry.get().split(",")

                try:
                    if (main_client_hotkey_entry.get()
                        and alt_client_hotkey_entry.get()
                        and alt_window_combobox.get()) == "":

                        messagebox.showerror("Error", "Fields cannot be empty.")

                    elif any(e in alt_control_key_list_1 for e in alt_control_key_list_2):

                        messagebox.showerror("Error",
                                             "Main Client Hotkey(s) and Alt Client Hotkey(s) must be different.")

                    elif len(alt_control_key_list_1) != len(alt_control_key_list_2):
                        messagebox.showerror("Error",
                                             "Number of keys must be equal to both Main Client and Alt Client.")

                    elif mini_ftool_activation_key in alt_control_key_list_1:

                        messagebox.showerror("Error", "Main Client HotKey from Alt Control cannot "
                                                      "be the same as the Mini Ftool Activation Key.")

                    else:

                        key1_counter = 1

                        for key1 in alt_control_key_list_1:
                            globals()["acak" + str(key1_counter)] = key1
                            exec('self.alt_control_key_' + str(key1_counter) + '.setKey("' + key1 + '")', None,
                                 locals())
                            key1_counter += 1

                        key2_counter = 1

                        for key2 in alt_control_key_list_2:
                            globals()["acig" + str(key2_counter)] = vk_code.get(key2)
                            key2_counter += 1

                        alt_window_name = alt_window_combobox.get()

                        self.save_config_json(file=alt_control_json_file,
                                              values=(main_client_hotkey_entry.get(), alt_client_hotkey_entry.get(),
                                                      alt_window_combobox.get()))

                        alt_window_combobox["values"] = self.save_alt_profiles(alt_window_combobox.get())

                        alt_control_boolean = True
                        menubar_window = False

                        alt_control_config_window.destroy()

                except Exception as e:
                    messagebox.showerror("Error", str(e))

            def stop():
                global alt_control_boolean

                self.clear_alt_control_shortcut_keys()

                alt_control_boolean = False

            self.load_alt_profiles()

            explanation_label = Label(alt_control_config_window, text="You can assign multiple keys (up to 20 keys)."
                                                                      "\n\nSeparate each key with a comma '','' "
                                                                      "if more than one."
                                                                      "\n\nExample:"
                                                                      "\n\nMain Client Hotkey(s): q,e,f1,f2,v,x..."
                                                                      "\nAlt Client Hotkey(s): 1,2,3,spacebar,z,c...",
                                      anchor=W,
                                      justify="left")
            explanation_label.pack(fill=X, padx=5, pady=5)

            frame = Frame(alt_control_config_window)

            frame.pack(fill=X, padx=5, pady=5)

            main_client_hotkey_label = Label(frame, text="Main Client Hotkey(s):", width=20, anchor=W)
            main_client_hotkey_entry = Entry(frame, width=22)

            alt_client_hotkey_label = Label(frame, text="Alt Client Hotkey(s):", width=20, anchor=W)
            alt_client_hotkey_entry = Entry(frame, width=22)

            alt_window_label = Label(frame, text="Profile Name:", width=20, anchor=W)
            alt_window_combobox = ttk.Combobox(frame, values=profile_list, width=19)

            main_client_hotkey_label.grid(row=0, column=0, pady=5)
            main_client_hotkey_entry.grid(row=0, column=1, pady=5)

            alt_client_hotkey_label.grid(row=1, column=0, pady=5)
            alt_client_hotkey_entry.grid(row=1, column=1, pady=5)

            alt_window_label.grid(row=2, column=0, pady=5)
            alt_window_combobox.grid(row=2, column=1, pady=5)

            button_start = Button(text="Start", width=10, height=1, command=start)
            button_start.pack(side=LEFT, padx=25)

            button_stop = Button(text="Stop", width=10, height=1, command=stop)
            button_stop.pack(side=RIGHT, padx=25)

            try:
                if alt_control_json_file_location.exists():
                    with open(alt_control_json_file_location) as js:
                        data = json.load(js)

                        main_client_hotkey_entry.insert(0, data["activation_key"])
                        alt_client_hotkey_entry.insert(0, data["in_game_key"])
                        alt_window_combobox.insert(0, data["alt_window"])
            except Exception as e:
                messagebox.showerror("Error", str(e))

            alt_control_config_window.wm_protocol("WM_DELETE_WINDOW",
                                                  lambda: self.destroy_toolbar_windows(alt_control_config_window))
            alt_control_config_window.mainloop()

    def send_alt_control_command(self, igk):
        global alt_control_boolean
        global alt_window_name
        global hwndAlt

        if alt_control_boolean and igk != "":
            hwndAlt = win32gui.FindWindow(None, "PyFlyff - " + alt_window_name)

            self.winapi(hwndAlt, igk)

    def set_user_agent(self):
        global user_agent
        global menubar_window

        if not menubar_window:

            menubar_window = True

            user_agent_config_window = Tk()

            window_width = 300
            window_height = 130

            screen_width = user_agent_config_window.winfo_screenwidth()
            screen_height = user_agent_config_window.winfo_screenheight()

            x = (screen_width / 2) - (window_width / 2)
            y = (screen_height / 2) - (window_height / 2)

            user_agent_config_window.geometry("300x130+" + str(int(x)) + "+" + str(int(y)))
            user_agent_config_window.minsize(300, 130)
            user_agent_config_window.attributes("-topmost", True)
            user_agent_config_window.title("User Agent")
            user_agent_config_window.iconbitmap(icon)

            def save():
                global menubar_window
                global user_agent_json_file

                try:
                    if user_agent_entry.get() == "":

                        messagebox.showerror("Error", "Field cannot be empty.")

                    else:

                        self.save_config_json(file=user_agent_json_file, values=(user_agent_entry.get(),))

                        menubar_window = False
                        user_agent_config_window.destroy()

                except Exception as e:
                    messagebox.showerror("Error", str(e))

            user_agent_label = Label(user_agent_config_window, text="Set your User Agent below:")
            user_agent_entry = Entry(user_agent_config_window)
            restart_label = Label(user_agent_config_window, text="After setting your User Agent, restart the Client.")

            user_agent_label.pack(fill=X, pady=5, padx=5)
            user_agent_entry.pack(fill=X, pady=5, padx=5)
            restart_label.pack(fill=X, pady=5, padx=5)

            button_save = Button(text="Save", width=10, height=1, command=save)
            button_save.pack(pady=5)

            if user_agent == "":
                user_agent_entry.insert(0, default_user_agent)
            else:
                user_agent_entry.insert(0, user_agent)

            user_agent_config_window.wm_protocol("WM_DELETE_WINDOW",
                                                 lambda: self.destroy_toolbar_windows(user_agent_config_window))

            user_agent_config_window.mainloop()

    def reset_hotkeys(self):
        global mini_ftool_window_name
        global hwndMain
        global hwndAlt
        global mini_ftool_activation_key
        global start_mini_ftool_loop

        if not start_mini_ftool_loop:
            mini_ftool_window_name = ""
            hwndMain = ""
            hwndAlt = ""

            mini_ftool_activation_key = ""

            globals()["mini_ftool_in_game_key_1"] = ""
            globals()["mini_ftool_in_game_key_2"] = ""
            globals()["mini_ftool_in_game_key_3"] = ""

            self.ftool_key.setKey("")

            self.clear_alt_control_shortcut_keys()

    def load_user_agent(self):
        global user_agent
        global user_agent_json_file_location

        try:
            if user_agent_json_file_location.exists():
                with open(user_agent_json_file_location) as js:
                    data = json.load(js)
                    user_agent = data["user_agent"]

            if user_agent == "":
                return default_user_agent
            else:
                return user_agent
        except KeyError as e:
            error_dialog = QErrorMessage()
            error_dialog.showMessage("Key not found in UserAgent.json: " + str(e) + "\nMake sure the key is valid "
                                                                                    "inside the file, or delete "
                                                                                    "the file "
                                                                                    "''C:/PyFlyff/UserAgent.json'' "
                                                                                    "to create a new one by setting "
                                                                                    "a new User Agent.")
            error_dialog.setWindowIcon(QIcon(icon))
            self.windows.append(error_dialog)

    def clear_alt_control_shortcut_keys(self):
        global alt_control_key_list_1
        global alt_control_key_list_2
        global alt_window_name

        alt_window_name = ""

        alt_control_key_list_1.clear()
        alt_control_key_list_2.clear()

        self.alt_control_key_1.setKey("")
        self.alt_control_key_2.setKey("")
        self.alt_control_key_3.setKey("")
        self.alt_control_key_4.setKey("")
        self.alt_control_key_5.setKey("")
        self.alt_control_key_6.setKey("")
        self.alt_control_key_7.setKey("")
        self.alt_control_key_8.setKey("")
        self.alt_control_key_9.setKey("")
        self.alt_control_key_10.setKey("")
        self.alt_control_key_11.setKey("")
        self.alt_control_key_12.setKey("")
        self.alt_control_key_13.setKey("")
        self.alt_control_key_14.setKey("")
        self.alt_control_key_15.setKey("")
        self.alt_control_key_16.setKey("")
        self.alt_control_key_17.setKey("")
        self.alt_control_key_18.setKey("")
        self.alt_control_key_19.setKey("")
        self.alt_control_key_20.setKey("")

    def create_shortcuts(self):
        self.ftool_key = QShortcut(self)
        self.ftool_key.activated.connect(self.start_ftool)

        self.alt_control_key_1 = QShortcut(self)
        self.alt_control_key_1.activated.connect(
            lambda: self.multithreading(lambda: self.send_alt_control_command(globals()["acig1"])))

        self.alt_control_key_2 = QShortcut(self)
        self.alt_control_key_2.activated.connect(
            lambda: self.multithreading(lambda: self.send_alt_control_command(globals()["acig2"])))

        self.alt_control_key_3 = QShortcut(self)
        self.alt_control_key_3.activated.connect(
            lambda: self.multithreading(lambda: self.send_alt_control_command(globals()["acig3"])))

        self.alt_control_key_4 = QShortcut(self)
        self.alt_control_key_4.activated.connect(
            lambda: self.multithreading(lambda: self.send_alt_control_command(globals()["acig4"])))

        self.alt_control_key_5 = QShortcut(self)
        self.alt_control_key_5.activated.connect(
            lambda: self.multithreading(lambda: self.send_alt_control_command(globals()["acig5"])))

        self.alt_control_key_6 = QShortcut(self)
        self.alt_control_key_6.activated.connect(
            lambda: self.multithreading(lambda: self.send_alt_control_command(globals()["acig6"])))

        self.alt_control_key_7 = QShortcut(self)
        self.alt_control_key_7.activated.connect(
            lambda: self.multithreading(lambda: self.send_alt_control_command(globals()["acig7"])))

        self.alt_control_key_8 = QShortcut(self)
        self.alt_control_key_8.activated.connect(
            lambda: self.multithreading(lambda: self.send_alt_control_command(globals()["acig8"])))

        self.alt_control_key_9 = QShortcut(self)
        self.alt_control_key_9.activated.connect(
            lambda: self.multithreading(lambda: self.send_alt_control_command(globals()["acig9"])))

        self.alt_control_key_10 = QShortcut(self)
        self.alt_control_key_10.activated.connect(
            lambda: self.multithreading(lambda: self.send_alt_control_command(globals()["acig10"])))

        self.alt_control_key_11 = QShortcut(self)
        self.alt_control_key_11.activated.connect(
            lambda: self.multithreading(lambda: self.send_alt_control_command(globals()["acig11"])))

        self.alt_control_key_12 = QShortcut(self)
        self.alt_control_key_12.activated.connect(
            lambda: self.multithreading(lambda: self.send_alt_control_command(globals()["acig12"])))

        self.alt_control_key_13 = QShortcut(self)
        self.alt_control_key_13.activated.connect(
            lambda: self.multithreading(lambda: self.send_alt_control_command(globals()["acig13"])))

        self.alt_control_key_14 = QShortcut(self)
        self.alt_control_key_14.activated.connect(
            lambda: self.multithreading(lambda: self.send_alt_control_command(globals()["acig14"])))

        self.alt_control_key_15 = QShortcut(self)
        self.alt_control_key_15.activated.connect(
            lambda: self.multithreading(lambda: self.send_alt_control_command(globals()["acig15"])))

        self.alt_control_key_16 = QShortcut(self)
        self.alt_control_key_16.activated.connect(
            lambda: self.multithreading(lambda: self.send_alt_control_command(globals()["acig16"])))

        self.alt_control_key_17 = QShortcut(self)
        self.alt_control_key_17.activated.connect(
            lambda: self.multithreading(lambda: self.send_alt_control_command(globals()["acig17"])))

        self.alt_control_key_18 = QShortcut(self)
        self.alt_control_key_18.activated.connect(
            lambda: self.multithreading(lambda: self.send_alt_control_command(globals()["acig18"])))

        self.alt_control_key_19 = QShortcut(self)
        self.alt_control_key_19.activated.connect(
            lambda: self.multithreading(lambda: self.send_alt_control_command(globals()["acig19"])))

        self.alt_control_key_20 = QShortcut(self)
        self.alt_control_key_20.activated.connect(
            lambda: self.multithreading(lambda: self.send_alt_control_command(globals()["acig20"])))

    def create_open_client_profile(self, client_type):
        global profile_file_location
        global menubar_window
        global profile_list

        if not menubar_window:

            menubar_window = True

            profile_window = Tk()

            window_width = 300
            window_height = 100

            screen_width = profile_window.winfo_screenwidth()
            screen_height = profile_window.winfo_screenheight()

            x = (screen_width / 2) - (window_width / 2)
            y = (screen_height / 2) - (window_height / 2)

            profile_window.geometry("300x100+" + str(int(x)) + "+" + str(int(y)))
            profile_window.minsize(300, 100)
            profile_window.attributes("-topmost", True)
            profile_window.title("Profile")
            profile_window.iconbitmap(icon)

            def open_profile_new_window():
                global menubar_window
                global profile_file_location
                global profile_list
                global url
                global can_reload_client

                try:
                    if profile_window_combobox.get() == "":

                        messagebox.showerror("Error", "Field cannot be empty.")

                    else:

                        profile_window_combobox["values"] = self.save_alt_profiles(profile_window_combobox.get())

                        if client_type == "Alt":

                            self.create_new_window(url, profile_window_combobox.get())
                        else:

                            self.browser = None

                            self.browser = QWebEngineView()

                            self.setCentralWidget(self.browser)

                            client_folder = "C:/PyFlyff/" + profile_window_combobox.get().replace(" ", "")

                            main_profile = QWebEngineProfile(profile_window_combobox.get().replace(" ", ""),
                                                             self.browser)
                            main_profile.setCachePath(client_folder)
                            main_profile.setPersistentStoragePath(client_folder)
                            main_page = QWebEnginePage(main_profile, self.browser)

                            self.browser.setPage(main_page)
                            self.browser.setUrl(QUrl(url))
                            self.setWindowTitle("PyFlyff - " + profile_window_combobox.get())

                            self.browser.page().profile().setHttpUserAgent(self.load_user_agent())

                            can_reload_client = True

                        menubar_window = False
                        profile_window.destroy()

                except Exception as e:
                    messagebox.showerror("Error", str(e))

            self.load_alt_profiles()

            profile_window_label = Label(profile_window, text="Create a new profile or choose an existing one.")
            profile_window_combobox = ttk.Combobox(profile_window, values=profile_list)

            profile_window_label.pack(fill=X, pady=5, padx=5)
            profile_window_combobox.pack(fill=X, pady=5, padx=5)

            button_save = Button(text="Open", width=10, height=1, command=open_profile_new_window)
            button_save.pack(pady=5)

            profile_window.wm_protocol("WM_DELETE_WINDOW",
                                       lambda: self.destroy_toolbar_windows(profile_window))
            profile_window.mainloop()

    def always_on_top(self):
        global is_on_top

        if not is_on_top:
            self.setWindowFlag(Qt.WindowStaysOnTopHint)
            self.show()
            self.q_action_always_on_top.setText("Always on Top: On")
            is_on_top = True
        else:
            self.setWindowFlags(
                Qt.Window |
                Qt.WindowTitleHint |
                Qt.WindowCloseButtonHint |
                Qt.WindowMinimizeButtonHint |
                Qt.WindowMaximizeButtonHint)
            self.show()
            self.q_action_always_on_top.setText("Always on Top: Off")
            is_on_top = False

    def reload_main_client(self):
        global can_reload_client

        if can_reload_client:
            self.browser.setUrl(QUrl(url))

    @staticmethod
    def save_config_json(**kwargs):
        global mini_ftool_json_file
        global alt_control_json_file
        global user_agent_json_file

        file = kwargs.get("file")
        values = kwargs.get("values")

        data = ""

        try:
            if file == mini_ftool_json_file:
                data = {"activation_key": values[0], "in_game_key": values[1], "repeat_times": values[2],
                        "interval": values[3], "window": values[4]}

            if file == alt_control_json_file:
                data = {"activation_key": values[0], "in_game_key": values[1], "alt_window": values[2]}

            if file == user_agent_json_file:
                data = {"user_agent": values[0]}

            json_data = json.dumps(data)
            save_json = open(file, "w")
            save_json.write(str(json_data))
            save_json.close()

        except Exception as e:
            messagebox.showerror("Error", str(e))

    @staticmethod
    def destroy_toolbar_windows(w):
        global menubar_window

        menubar_window = False
        w.destroy()

    @staticmethod
    def save_alt_profiles(combobox):
        exist = any(combobox in string for string in profile_list)

        if not exist:
            profile_list.append(combobox)

            f = open(profile_file_location, "a")
            f.write(combobox + "\n")
            f.close()

            return profile_list

    @staticmethod
    def load_alt_profiles():
        global profile_list
        global data_folder

        if os.path.isfile(profile_file_location):
            f = open(profile_file_location, "r")
            content = f.read()
            profile_list = content.split("\n")
            if "" in profile_list:
                profile_list.remove("")
            f.close()
        else:
            if not os.path.isdir(data_folder):
                os.makedirs(data_folder)
                f = open(profile_file_location, "w")
                f.close()

    @staticmethod
    def multithreading(function):
        threading.Thread(target=function).start()

    @staticmethod
    def winapi(w, key):
        win32api.SendMessage(w, win32con.WM_KEYDOWN, key, 0)
        time.sleep(random.uniform(0.369420, 0.769420))
        win32api.SendMessage(w, win32con.WM_KEYUP, key, 0)


app = QApplication(sys.argv)

QApplication.setApplicationName("PyFlyff")

window = MainWindow()

app.exec_()
