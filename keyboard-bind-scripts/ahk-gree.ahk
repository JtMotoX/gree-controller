#SingleInstance force
SetWorkingDir %A_ScriptDir%

; REMAP AC CONTROLS
#0::Run "server-gree.vbs" toggle-power 0 ; WIN+0
#-::Run "server-gree.vbs" cool -1 ; WIN+-
#=::Run "server-gree.vbs" cool 1 ; WIN+=
