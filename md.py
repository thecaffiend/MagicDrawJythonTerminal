from com.nomagic.uml2.ext.jmi.helpers import StereotypesHelper as halp
from com.nomagic.magicdraw.core import Application

app = Application.getInstance()
proj = app.getProject()
mod = proj.getModel()
sysml = halp.getProfile(proj, "SysML Profile")
req = halp.getStereotype(proj, "Requirement")

