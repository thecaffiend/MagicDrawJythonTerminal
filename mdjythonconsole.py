import sys
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
# TODO: automate finding this location
sys.path.append("/opt/magicdraw/plugins/com.nomagic.magicdraw.jpython/jython2.5.1/Lib")

# also, the location of this script is not added. let us fix this as well.
# TODO: automate finding this location
sys.path.append("/home/gtpmasevm/MagicDrawJythonTerminal")

from jythonconsole import console
console.main()
