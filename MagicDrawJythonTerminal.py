from com.nomagic.magicdraw.core import Application
from com.nomagic.magicdraw.ui.dialogs import MDDialogParentProvider
from org.python.util import PythonInterpreter
from javax.swing import JOptionPane 
from javax.swing import JFrame 
from javax.swing import JButton 
from javax.swing import JScrollPane 
from javax.swing import JTextArea 
from javax.swing import JTextField 
from java.awt import BorderLayout
from java.awt import Dimension
from java.awt import Color
from java.io import OutputStream
from java.io import PrintStream
from java.io import Writer
from java.io import PrintWriter
from java.lang import String
from java.lang import StringBuilder
from java.lang import System

import sys

# useful for debugging
# JOptionPane.showMessageDialog(None, "debug message")

###
# Minimal writer subclass for writer based output 
class TerminalWriter(Writer):    
    def __init__(self, textArea):
        Writer.__init__(self)
        self.terminal = textArea
        
    def flush(self):
        return
    
    def close(self):
        return
    
    def write(self, cbuf, offset, len):
        s = String(cbuf, offset, len)
        self.terminal.append(s)

###
# Minimal outputstream subclass for outputstream based output
# note, this is currently how this is wired up
class TerminalOutputStream(OutputStream):
    sb = StringBuilder()
    
    def __init__(self, textArea):
        OutputStream.__init__(self)
        self.terminal = textArea
        
    def flush(self):
        return
    
    def close(self):
        return
    
    def write(self, b):
        if b == '\r':
            return
        if b == '\n':
            self.textArea.append(self.sb.toString())
            self.sb.setLength(0)
        self.sb.append(b)
    
    def write(self, cbuf, offset, len):
        s = String(cbuf, offset, len)
        self.terminal.append(s)

        
###
# JFrame subclass for the main application window
class MagicDrawJythonTerminal(JFrame):
    inputField = JTextField()    
    scrollPane = JScrollPane()
    terminalArea = JTextArea()
    interpreter = PythonInterpreter()
    terminalOut = TerminalOutputStream(terminalArea)
    printStream = PrintStream(terminalOut, True)
# use these if you want writer based output instead of the outputstream
    terminalOut = TerminalWriter(terminalArea)
    printWriter = PrintWriter(terminalOut, True)
    
    def __init__(self):
        JFrame.__init__(self, 'MagicDraw Jython Console')
        # grab the current out and err so we can set them back later (for the main java
        # System.out/err, not the PythonInterpreter
        self.__outOriginal = System.out
        self.__errOriginal = System.err
        # use the printStream as it updates the textarea
        System.setOut(self.printStream)
        System.setErr(self.printStream)
        self.CreateComponents()
        self.setVisible(True) 
        self.requestFocus()
        self.inputField.requestFocus()
    
    def __del__(self):
        System.setOut(self.__outOriginal)
        System.setErr(self.__errOriginal)
        print 'Goodbye'
    
    # this is called when enter is pressed in the input textfield
    def CommandEntered(self, event):
        if event.source.text == 'exit':
            # let's kill the frame
            System.setOut(self.__outOriginal)
            System.setErr(self.__errOriginal)
            self.dispose()
        else:
            # echo the input to the text area using the printstream
            s = 'in : ' + event.source.text
            self.printStream.println(s)
            
            # try the main interp (the getLocals was just to see if I could interact with it)
            # it's not returning anything
            # eval(event.source.txt)
            
            # set the input text blank and give it focus back. we don't get here if we try to use 
            # the interpreter, though we do when we don't try to interact with the interpreter 
            self.inputField.setText('')
            self.inputField.requestFocus()

    def CreateComponents(self):
# use these if you want the writer based output
#        self.interpreter.setOut(self.printWriter)
#        self.interpreter.setErr(self.printWriter)
        self.interpreter.setOut(self.printStream)
        self.interpreter.setErr(self.printStream)
        
        self.inputField.actionPerformed=self.CommandEntered
        self.inputField.setBackground(Color.BLACK)
        self.inputField.setForeground(Color.GREEN)
        
        self.terminalArea.setBackground(Color.BLACK)
        self.terminalArea.setForeground(Color.GREEN)
        self.terminalArea.setEditable(False)
        self.terminalArea.setPreferredSize(Dimension(800, 600))
    
        self.setLayout(BorderLayout())
        self.scrollPane.getViewport().add(self.terminalArea)
        self.add(self.scrollPane)
        self.add(self.inputField, BorderLayout.SOUTH)
        self.setPreferredSize(self.getPreferredSize())
        self.pack()
    
# Main script 
#PythonInterpreter.initialize(System.getProperties(), None, None)
#project = Application.getInstance().getProject()
t = MagicDrawJythonTerminal()
