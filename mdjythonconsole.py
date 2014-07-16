import sys
from javax.swing import JFrame, JScrollPane
"""
        much as i was looking forward to rewriting the whole terminal experience,
        somebody already did:
                http://code.google.com/p/jythonconsole/
        let us grab the most recent version here:
                wget http://jythonconsole.googlecode.com/files/jythonconsole-0.0.7.zip
                unzip jythonconsole-0.0.7.zip
                mv jythonconsole-0.0.7 jythonconsole
                touch jythonconsole/__init__.py
        you'll then have to add it to the jython path (see below).
"""

# by default, MagicDraw seems to add 
#   $MD_HOME/Lib 
# to the jython path when it means to add 
#   $MD_HOME/plugins/com.nomagic.magicdraw.jpython/jython2.5.1/Lib
# let us fix this.
real_jython_lib_path = sys.currentWorkingDir + "/plugins/com.nomagic.magicdraw.jpython/jython2.5.1/Lib"
if real_jython_lib_path not in sys.path:
        sys.path.append(sys.currentWorkingDir + "/plugins/com.nomagic.magicdraw.jpython/jython2.5.1/Lib")

# also, the location of this script is not added. let us fix this as well so we can import things
# TODO: automate finding this location. 
# PROBLEM: __file__ is not populated, and inspect is not available
script_path = "/home/gtpmasevm/MagicDrawJythonTerminal"
if script_path not in sys.path:
    sys.path.append(script_path)

from jythonconsole.console import Console

from com.nomagic.magicdraw.core import Application

class MDConsole(Console):
    
    # BANNER = Console.BANNER + ["MagicDraw OpenAPI Version %s" % Application.getInstance().openAPIVersion]
    def __init__(self, namespace={}):
        """
            Create a MagicDraw Jython Console.
            namespace is an optional and should be a dictionary or Map
        """

        # populate with the application and current project
        namespace['app'] = Application.getInstance()
        # TODO: probably need to listen for this changing, huh?
        namespace['proj'] = namespace['app'].getProject()
        # TODO: probably need to listen for this changing, huh?
        namespace['model'] = namespace['proj'].getModel()

        Console.__init__(self, namespace)

class MDJythonFrame(JFrame):
    """ This is just like the default JythonFrame, but without the MagicDraw-killing feature
    """
    def __init__(self):
        self.title = "MagicDraw Jython"
        self.size = (600, 400)

def main(namespace={}):
    frame = MDJythonFrame()
    console = MDConsole(namespace)
    frame.getContentPane().add(JScrollPane(console.text_pane))
    frame.visible = True

if __name__ == "__main__":
    main()

