from datetime import datetime, date, MAXYEAR
import wx
import urllib.request
import json
from random import randint
from variables import APPNAME, UPDATE_URL, SOURCEFORGE, APPVERSION, SURVEY
import webbrowser

# wxPy datetime to python datetime From https://www.blog.pythonlibrary.org/2014/08/27/wxpython-converting-wx-datetime-python-datetime/, Thanks MIKE!


def pydate2wxdate(Date):
    assert isinstance(Date, (datetime, date))
    tt = Date.timetuple()
    dmy = (tt[2], tt[1] - 1, tt[0])
    return wx.DateTime.FromDMY(*dmy)


def wxdate2pydate(Date):
    assert isinstance(Date, wx.DateTime)
    if Date.IsValid():
        ymd = map(int, Date.FormatISODate().split('-'))
        return date(*ymd)
    else:
        return None

# My utils from here


def ParseDateTime(Date):  # return [isoverdue, strdate]
    if type(Date) is str:
        return (False, Date, '')
    today = datetime.now().replace(hour=0, minute=0, second=0, microsecond=0)
    difference = (Date - today).days
    if difference <= -7:
        return (True, Date.strftime('%a %d %b %y'), Date.strftime(' %H:%M'))
    elif -7 < difference < -1:
        return (True, Date.strftime('Last %A'), Date.strftime(' @ %H:%M'))
    elif difference == -1:
        return (True, 'Yesterday', Date.strftime(' @ %H:%M'))
    elif difference == 0:
        return (True, 'Today', Date.strftime(' @ %H:%M'))
    elif difference == 1:
        return (False, 'Tommorow', Date.strftime('@ %H:%M'))
    elif 1 < difference <= 7:
        return (False, Date.strftime('Next %A'), Date.strftime(' @ %H:%M'))
    else:
        return (False, Date.strftime('%a %d %b %y'), Date.strftime(' %H:%M'))


def checkForUpdate():
    try:
        with urllib.request.urlopen(UPDATE_URL) as page:
            data = json.loads(page.read().decode())
        if data['version'] > APPVERSION:
            result = wx.MessageDialog(None, 'A new version is available. This update adds: {}. Do you want to install?'.format(data['changes']), APPNAME + ' Update', wx.YES_NO | wx.ICON_QUESTION).ShowModal()
            if result == wx.ID_YES:
                webbrowser.open(SOURCEFORGE)
                return True
            else:
                return False
        else:
            return False
    except Exception as e:
        return False


def hints():
    x = randint(0, 25)
    if x == 0:
        wx.MessageDialog(None, 'Having Issues Or Want To Suggest A Change? Follow Me On Twitter @kaleidawave', APPNAME).ShowModal()
    if x == 1:
        result = wx.MessageDialog(None, 'Liking tasks? As the project is in early development I am looking for feedback. Consider completing this short questionaire on the program?', APPNAME + ' Update', wx.YES_NO | wx.ICON_QUESTION).ShowModal()
        if result == wx.ID_YES:
            webbrowser.open(SURVEY)


def dateSort(date):
    if type(date) is str:
        return datetime(MAXYEAR, 1, 1)
    else:
        return date


def SkipNonNum(event):
    if event.GetKeyCode() in [8, 48, 49, 50, 51, 52, 53, 54, 55, 56, 57]:  # 8 is backspace, 48-57 are numbers
        event.Skip()
