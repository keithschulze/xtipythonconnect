#
#
#  Python IPythonConnect XTension
#
#  Copyright (c) 2014 Keith Schulze (keith.schulze@monash.edu)
#  BSD-style copyright and disclaimer apply
#
#    <CustomTools>
#      <Menu>
#       <Item name="IPython Connect" icon="Python" tooltip="Opens an notebook instance.">
#         <Command>PythonXT::XTIPythonConnect(%i)</Command>
#       </Item>
#      </Menu>
#    </CustomTools>

import ImarisLib
import json
import os
import sys
import time
from subprocess import *

# GUI Imports
from Tkinter import *
from ttk import Button, Radiobutton
import tkFileDialog
import tkMessageBox
from tkSimpleDialog import Dialog


# IPython Imports
try:
    import IPython
except ImportError, ie:
    print 'Could not import IPython'
    tkMessageBox.showwarning(
        "Failed to import IPython",
        "IPython needs to be installed. See instructions at:\n"
        "http://ipython.org/ipython-doc/2/install/install.html"
    )


class IPSettingsModel(object):

    BP_SETTINGS_MAC = os.path.expanduser("~") +\
        "/Library/Application Support/Bitplane"
    BP_SETTINGS_WIN = os.path.expanduser("~") +\
        "/AppData/Local/Bitplane"

    def __init__(self, notebook_dir):
        self.notebook_dir = notebook_dir

    def serialise(self):
        return {'notebook_dir': self.notebook_dir}

    @classmethod
    def save_settings(cls, settings_model, path):
        base_dir = os.path.dirname(path)
        if not os.path.exists(base_dir):
            os.makedirs(base_dir)

        with open(path, "w") as outfile:
            json.dump(settings_model.serialise(), outfile)

    @classmethod
    def read_settings(cls, path):
        json_data = open(path)
        data = json.load(json_data)
        json_data.close()

        return IPSettingsModel(data["notebook_dir"])

    @classmethod
    def get_platform_base_path(cls):
        if sys.platform == 'darwin':
            return IPSettingsModel.BP_SETTINGS_MAC
        elif sys.platform == 'Windows':
            return IPSettingsModel.BP_SETTINGS_WIN
        else:
            return os.path.expanduser("~")


class IPSettingsDialog(object, Dialog):

    def __init__(self, parent, settings, title):
        self.settings = settings
        Dialog.__init__(self, parent, title)

    def body(self, parent):
        self.tkVar = IntVar()
        self.tkVar.set(-1)
        tkRb1 = Radiobutton(parent, text="QT Console", variable=self.tkVar,
                            value=0, command=self.radio_select)
        tkRb1.grid(row=0)
        tkRb2 = Radiobutton(parent, text="Notebook", variable=self.tkVar,
                            value=1, command=self.radio_select)
        tkRb2.grid(row=1)

        self.tkDir = StringVar()
        self.tkDir.set(self.settings.notebook_dir)
        self.tkDirEntry = Entry(parent, textvariable=self.tkDir,
                                state="disabled")
        self.tkDirEntry.grid(row=2, column=0)
        self.tkBrowseButton = Button(parent, text="Browse", state="disabled",
                                     command=self.get_directory)
        self.tkBrowseButton.grid(row=2, column=1)

    def apply(self):
        rad = int(self.tkVar.get())
        note_dir = str(self.tkDir.get())
        self.result = rad, note_dir

    def radio_select(self):
        if self.tkVar.get() == 1:
            self.tkDirEntry.config(state="normal")
            self.tkBrowseButton.config(state="normal")
        else:
            self.tkDirEntry.config(state="disabled")
            self.tkBrowseButton.config(state="disabled")

    def get_directory(self):
        options = {'mustexist': True,
                   'title': 'Please select a directory for IPython notebooks'}
        folder_path = tkFileDialog.askdirectory(**options)
        self.tkDir.set(folder_path)


def XTIPythonConnect(aImarisId):
    settings_file_name = "xtipc_settings.json"
    settings_path = os.path.join(IPSettingsModel.get_platform_base_path(),
                                 settings_file_name)

    # Check if settings file exist otherwise create a new model
    if os.path.exists(settings_path):
        settings_model = IPSettingsModel.read_settings(settings_path)
    else:
        settings_model = IPSettingsModel(os.path.expanduser("~"))

    vImarisLib = ImarisLib.ImarisLib()

    # Get an imaris object with id aImarisId
    vImaris = vImarisLib.GetApplication(aImarisId)

    # Check if the object is valid
    if vImaris is None:
        print 'Could not connect to Imaris!'
        tkMessageBox.showwarning(
            "connection failed",
            "Could not connect to Imaris!"
        )
        time.sleep(2)
        return

    rootTkWindow = Tk()
    rootTkWindow.withdraw()
    dialog = IPSettingsDialog(rootTkWindow, settings_model, "IPython Flavours")

    rad_selection, note_dir = dialog.result

    if settings_model.notebook_dir != note_dir:
        settings_model.notebook_dir = note_dir
        IPSettingsModel.save_settings(settings_model, settings_path)

    id_string = "--IPKernelApp.exec_lines=[\'aImarisId=" +\
                str(aImarisId) + "\']"

    if rad_selection == 0:
        IPython.start_ipython(argv=["qtconsole", id_string])
    elif rad_selection == 1:
        notebook_dir = "--notebook-dir=%s" % note_dir
        IPython.start_ipython(argv=["notebook", notebook_dir, id_string])
    else:
        return

    rootTkWindow.quit()
