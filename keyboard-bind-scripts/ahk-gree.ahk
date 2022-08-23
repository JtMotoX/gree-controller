#SingleInstance force
SetWorkingDir %A_ScriptDir%

#0::
RAlt & 0::
Run "server-gree.vbs" toggle-power 0
return

#-::
RAlt & -::
Run "server-gree.vbs" cool -1
return

#=::
RAlt & +::
Run "server-gree.vbs" cool 1
return
