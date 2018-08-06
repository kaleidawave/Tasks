#!/bin/python

import wx

# from win10toast import ToastNotifier
# toaster = ToastNotifier()

app = wx.App(False)

from maingui import Tasks

frm = Tasks()
app.MainLoop()
