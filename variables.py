import wx
import os

# main
APPNAME = 'Tasks'
FULLNAME = 'WinTasks'
APPVERSION = 1
APPDESCRIPTION = 'A program to manage tasks with or without deadlines'
APPDEVELOPER = 'KALEIDAGRAPH'

REPO = r'https://github.com/kaleidagraph/Tasks'
TWITTER = r'https://twitter.com/kaleidawave'
SOURCEFORGE = r'http://sourceforge.net/p/win-tasks'
SURVEY = r'https://docs.google.com/forms/d/e/1FAIpQLSeaUMfuXeK2lIWVBs4CdHx-5ITOob7XRzkuuOWeuLnvvYm-Ww/viewform?usp=sf_link'
UPDATE_URL = r'https://raw.githubusercontent.com/kaleidagraph/Tasks/master/updateInfo.json'
HOMEPAGE = r'https://github.com/kaleidagraph/Tasks/master/README.md'

TPROP = ['Title', 'Description', 'Sub Tasks', 'Date Setting', 'Completion Date', 'Date Created', 'Importance', 'Category', 'Completiton']
DEFAULT_TASK = ['', '', ([['', False]] * 6), 0, None, None, 0, 0, 0]
TABLE_HEADERS = ['Title', 'Importance', 'Category', 'Completion Date', 'Completion']

DEFAULT_SETTINGS = {'numOpens': 0, 'categories': (['None'] + [str(Y) for Y in range(1, 9)]), 'tabelHighlighting': True, 'updateChecking': True, 'messages': True, 'deleteOnCompletion': False}
CUSTOM_SETTINGS = ['Highlighting overdue tasks in the table', 'Check for updates on launch', 'Show occasional hint messages', 'Delete task on completion']
EDIT_SETTINGS_KEYS = ['tabelHighlighting', 'updateChecking', 'messages', 'deleteOnCompletion']

# Files
TASKS = 'tasks.json'
SETTINGS = 'settings.json'
ICON_FILE = 'icon.ico'

# wx
ICON = wx.Icon(ICON_FILE, wx.BITMAP_TYPE_ICO)

NORESIZE = wx.DEFAULT_FRAME_STYLE & ~(wx.RESIZE_BORDER | wx.MAXIMIZE_BOX)
FONT1 = wx.Font(18, wx.FONTFAMILY_DEFAULT, wx.FONTSTYLE_NORMAL, wx.FONTWEIGHT_NORMAL, False)
FONT2 = wx.Font(12, wx.FONTFAMILY_DEFAULT, wx.FONTSTYLE_NORMAL, wx.FONTWEIGHT_NORMAL, False)
FONTWING = wx.Font(16, wx.FONTFAMILY_DEFAULT, wx.FONTSTYLE_NORMAL, wx.FONTWEIGHT_NORMAL, False, faceName='Wingdings')  # using 'l' for bulletpoints 'n' for square

BLACK = wx.Colour(0, 0, 0)
WHITE = wx.Colour(255, 255, 255)
ALERTRED = wx.Colour(239, 16, 20)
ALERTORANGE = wx.Colour(252, 115, 17)
ALERTGREEN = wx.Colour(55, 204, 6)

COLOURS = [
    wx.Colour(236, 95, 103),   # red
    wx.Colour(249, 145, 87),   # orange
    wx.Colour(250, 200, 99),   # yellow
    wx.Colour(153, 199, 148),  # light green
    wx.Colour(95, 179, 179),   # turqoise
    wx.Colour(102, 153, 204),  # blue
    wx.Colour(197, 148, 197),  # purple
    wx.Colour(171, 121, 103)   # brown
]
