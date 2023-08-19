#SingleInstance force
SetWorkingDir %A_ScriptDir%

I_Icon = D:\OneDrive\Documents\AHK\Multipurpose_Alphabet_Icons_by_HYDRATTZ\Aikawns\G\lg.ico
ICON [I_Icon]	;Changes a compiled script's icon (.exe)
Menu, Tray, Icon, %I_Icon%	;Changes menu tray icon

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
