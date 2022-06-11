Dim Arg, mode, adjust
Set Arg = WScript.Arguments
mode = Arg(0)
adjust = Arg(1)

Dim objXmlHttpMain , URL

strJSONToSend = "{""mode"":""" + mode + """, ""adjust"":" + adjust + "}"

URL="http://192.168.168.11:5001/temperature-adjust" 
Set objXmlHttpMain = CreateObject("Msxml2.ServerXMLHTTP") 
On Error Resume Next   'enable error handling
objXmlHttpMain.open "POST",URL, False 
objXmlHttpMain.setRequestHeader "Authorization", "Bearer <api secret id>"
objXmlHttpMain.setRequestHeader "Content-Type", "application/json"
objXmlHttpMain.send strJSONToSend
If Err Then            'handle errors
	WScript.Echo Err.Description & " [0x" & Hex(Err.Number) & "]"
	WScript.Quit 1
End If
On Error Goto 0        'disable error handling again
