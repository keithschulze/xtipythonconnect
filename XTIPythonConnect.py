#
#
#  Python IPythonConnect XTension
#
#  Copyright (c) 2014 Keith Schulze (keith.schulze@monash.edu), BSD-style copyright and disclaimer apply
#
#    <CustomTools>
#      <Menu>
#       <Item name="IPython Connect" icon="Python" tooltip="Opens an notebook instance.">
#         <Command>PythonXT::XTIPythonConnect(%i)</Command>
#       </Item>
#      </Menu>
#    </CustomTools>

import ImarisLib
import IPython
import os
import sys


def XTIPythonConnect(aImarisId):

    vImarisLib = ImarisLib.ImarisLib()

    # Get an imaris object with id aImarisId
    vImaris = vImarisLib.GetApplication(aImarisId)

    # Check if the object is valid
    if vImaris is None:
        print "Could not connect to Imaris!"
        time.sleep(2)
        return

    filepath = vImaris.GetCurrentFileName()
    base_dir = os.path.dirname(filepath)
    id_string = "--IPKernelApp.exec_lines=[\'aImarisId=" + str(aImarisId) + "\']"
    notebook_dir = "--notebook-dir=%s" % (base_dir,)

    # IPython.start_ipython(argv=["notebook", "--notebook-dir=%s" % (base_dir,)])
    IPython.start_ipython(argv=["notebook", notebook_dir, id_string])
