import wx
import wx.adv

from datetime import datetime
import webbrowser

from variables import *
from utils import pydate2wxdate, wxdate2pydate, ParseDateTime, SkipNonNum
# toaster.show_toast('Hello World!!!', 'Python is 10 seconds awsm!', duration=10, threaded=True)


class TaskEditor(wx.Frame):
    def __init__(self, parent, categories, values=DEFAULT_TASK, edit=False):
        wx.Frame.__init__(self, None, title='Task Creator', style=NORESIZE, size=(480, 480))
        self.SetIcon(ICON)
        self.edit = edit
        self.calWindow = None
        self.panel = wx.Panel(self)
        self.parent = parent
        self.setting = int(values[3])
        self.subtasks = values[2]
        self.categories = categories
        self.values = values
        self.Draw(values)
        self.DateSetting(None)
        self.Center()
        self.Bind(wx.EVT_CLOSE, self.Exit, self)
        self.Show()

    def Draw(self, values):
        wx.StaticText(self.panel, 1, 'Edit Task' if self.edit else 'Create A Task', pos=(5, 12)).SetFont(FONT1)

        # title
        wx.StaticText(self.panel, 1, 'Title:', pos=(5, 54))
        self.title = wx.TextCtrl(self.panel, 1, values[0], pos=(40, 50), size=(415, 23))
        self.title.SetMaxLength(80)

        # description
        wx.StaticText(self.panel, 1, 'Description:', pos=(5, 85))
        self.description = wx.TextCtrl(self.panel, 1, values[1], pos=(5, 105), size=(450, 120), style=wx.TE_MULTILINE)
        self.description.SetMaxLength(460)

        # importance
        wx.StaticText(self.panel, 1, 'Importance:', pos=(5, 237))
        self.importanceSetting = wx.TextCtrl(self.panel, 1, str(values[6]), pos=(75, 235), size=(20, 19))
        self.importanceSetting.SetMaxLength(1)
        self.importanceSetting.Bind(wx.EVT_CHAR, SkipNonNum)  # skips non number characters

        # categories
        wx.StaticText(self.panel, 1, 'Category:', pos=(120, 237))
        self.categoryColour = wx.StaticText(self.panel, 1, 'n', pos=(177, 234))
        self.categoryColour.SetFont(FONTWING)  # wingdings
        if values[7] is not 0:
            self.categoryColour.SetForegroundColour(COLOURS[values[7] - 1])
        else:
            self.categoryColour.SetForegroundColour(BLACK)

        self.categorySetting = wx.Choice(self.panel, 1, choices=self.categories, pos=(196, 233))
        self.categorySetting.SetSelection(values[7])
        self.categorySetting.Bind(wx.EVT_CHOICE, self.changeCategory)

        # subtasks
        wx.StaticText(self.panel, 1, 'Sub Tasks:', pos=(5, 265))
        self.subTasks = list()
        for x in range(2):
            for y in range(3):
                if len(values[2]) > (y + (3 * x)):
                    input1 = wx.TextCtrl(self.panel, 1, values[2][y + (3 * x)][0], pos=(27 + (x * 220), 290 + (y * 27)), size=(140, 23))
                    input1.SetMaxLength(18)
                    self.subTasks.append([input1, values[2][y + (3 * x)][1]])
                else:
                    self.subTasks.append([wx.TextCtrl(self.panel, 1, '', pos=(27 + (x * 220), 293 + (y * 27)), size=(140, 23)), False])

                wx.StaticText(self.panel, 1, 'w', pos=(7 + (x * 223), 291 + (y * 27))).SetFont(FONTWING)  # bullet point wingding

        # completiondate
        wx.StaticText(self.panel, 1, 'Competiton Date:', pos=(5, 390))

        self.timeSetting = wx.Choice(self.panel, 1, choices=['None       ', 'Date', 'Time', 'Date & Time'], pos=(5, 407))
        self.timeSetting.SetSelection(self.setting)
        self.Bind(wx.EVT_CHOICE, self.DateSetting, self.timeSetting)

        self.dateControl = wx.adv.DatePickerCtrl(self.panel, 1, datetime.now(), pos=(110, 407))
        if self.setting is 1 or self.setting is 3:
            self.dateControl.SetValue(pydate2wxdate(values[4].date()))

        self.calButton = wx.Button(self.panel, 1, 'Cal', pos=(202, 407), size=(35, 23))
        self.calButton.Bind(wx.EVT_BUTTON, self.OpenCal)

        self.timeControl = wx.adv.TimePickerCtrl(self.panel, 1, datetime.now(), pos=(245, 407), size=(50, -1))
        if self.setting is 2 or self.setting is 3:
            time = self.values[4]
            self.timeControl.SetTime(time.hour, time.minute, 0)  # self.dateControl.SetTime(time.hour, time.minute) AttributeError: 'DatePickerCtrl' object has no attribute 'SetTime'

        # complete button
        finish = wx.Button(self.panel, 1, ('Edit Task' if self.edit else 'Create Task'), pos=(368, 407))
        finish.Bind(wx.EVT_BUTTON, self.ReturnResults)

    def changeCategory(self, event):
        category = self.categorySetting.GetCurrentSelection()
        if category > 0:
            self.categoryColour.SetForegroundColour(COLOURS[category - 1])
        else:
            self.categoryColour.SetForegroundColour(BLACK)
        self.categoryColour.Refresh()

    def DateSetting(self, event):
        self.setting = self.timeSetting.GetSelection()
        if self.setting == 0:  # None
            self.dateControl.Disable()
            self.timeControl.Disable()
            self.calButton.Disable()

        elif self.setting == 1:  # Date
            self.dateControl.Enable()
            self.calButton.Enable()
            self.timeControl.Disable()

        elif self.setting == 2:  # Time
            self.dateControl.Disable()
            self.calButton.Disable()
            self.timeControl.Enable()

        else:  # Date & Time
            self.dateControl.Enable()
            self.calButton.Enable()
            self.timeControl.Enable()

    def ChangeDate(self, date):
        self.dateControl.SetValue(date)

    def OpenCal(self, event):
        self.calWindow = CalendarDialog(self, self.dateControl.GetValue())

    def Exit(self, event):
        try:
            self.calWindow.Close(True)
        except Exception as e:
            pass
        self.Destroy()

    def ReturnResults(self, event):
        task = list()
        # title
        if self.title.Value.strip() is '':
            wx.MessageDialog(None, 'Title is empty', APPNAME).ShowModal()
            return
        else:
            task.append(self.title.Value.strip())
        # description
        if self.description.Value.strip() is '':
            task.append('No Description')
        else:
            task.append(self.description.Value.strip())

        # subtasks
        subtask = list()
        for x in self.subTasks:
            if x[0].Value.strip() is '':
                continue
            else:
                subtask.append([x[0].Value.strip(), x[1]])
        task.append(subtask)

        # date setting
        task.append(self.setting)

        # completion date
        now = datetime.now().replace(second=0, microsecond=0)
        dateValue = wxdate2pydate(self.dateControl.GetValue())
        date = datetime.combine(dateValue, datetime.min.time())

        timeValues = self.timeControl.GetTime()[:2]  # tuple (hour, minutes, ) ignoring seconds
        time = now.replace(hour=timeValues[0], minute=timeValues[1], second=0, microsecond=0)
        if self.setting == 0:  # None
            task.append('None')
        elif self.setting == 1:  # Date
            if date < now.replace(hour=0, minute=0, second=0, microsecond=0):
                wx.MessageDialog(None, 'Cannot Set Due Date In The Past', APPNAME).ShowModal()
                return
            else:
                task.append(date)
        elif self.setting == 2:  # Time
            if time < now:
                wx.MessageDialog(None, 'Cannot Set Due Time In The Past', APPNAME).ShowModal()
                return
            else:
                task.append(time)
        else:  # Date & Time
            dateAndTime = date.replace(hour=timeValues[0], minute=timeValues[1], second=0, microsecond=0)
            if dateAndTime < now:  # may be a problem here
                wx.MessageDialog(None, 'Cannot Set Due Time In The Past', APPNAME).ShowModal()
                return
            else:
                task.append(dateAndTime)

        # date created
        if self.values[5] is None:
            task.append(now)
        else:
            task.append(self.values[5])

        # importance
        if self.importanceSetting.Value is '':
            task.append(0)
        else:
            task.append(int(self.importanceSetting.Value))

        # category
        task.append(self.categorySetting.GetSelection())

        # completition
        task.append(self.values[8])
        # task.append(options)
        if self.edit:
            self.parent.AlterTask(task)
        else:
            self.parent.AddTask(task)
        self.Close(True)


class CalendarDialog(wx.Frame):
    def __init__(self, parent, date):
        wx.Frame.__init__(self, None, title='Calendar', style=NORESIZE, size=(247, 211))
        self.SetIcon(ICON)
        self.panel = wx.Panel(self)
        self.parent = parent
        self.calendar = wx.adv.CalendarCtrl(self.panel, 1, date, pos=(0, 0))
        self.done = wx.Button(self.panel, 2, 'Done', pos=(0, 149), size=(231, 23))
        self.done.Bind(wx.EVT_BUTTON, self.submit)
        self.Center()
        self.Show()

    def submit(self, event):
        self.parent.ChangeDate(self.calendar.GetDate())
        self.Close(True)


class CategoryDialog(wx.Frame):
    def __init__(self, categories, parent):
        wx.Frame.__init__(self, None, title='Categories', style=NORESIZE, size=(417, 205))
        self.SetIcon(ICON)
        self.panel = wx.Panel(self)
        self.categories, self.parent = categories, parent

        self.categoryControls = list()
        for x in range(2):
            for y in range(4):
                inputCat = wx.TextCtrl(self.panel, 1, self.categories[y + (4 * x)], size=(170, 23), pos=(25 + (200 * x), 10 + (27 * y)))
                inputCat.SetMaxLength(19)
                self.categoryControls.append(inputCat)
                label = wx.StaticText(self.panel, 1, 'n', pos=(5 + (200 * x), 10 + (27 * y)))  # 'n' = square
                label.SetFont(FONTWING)  # wingdings
                label.SetForegroundColour(COLOURS[y + (4 * x)])  # add color to the square

        self.Bind(wx.EVT_CLOSE, self.submit, self)

        self.done = wx.Button(self.panel, 2, 'Done', pos=(308, 134))
        self.done.Bind(wx.EVT_BUTTON, self.submit)

        self.Center()
        self.Show()

    def submit(self, event):
        self.categories = list()
        for y, x in enumerate(self.categoryControls):
            if x.Value.strip() == '':
                self.categories.append(str(y))
            else:
                self.categories.append(x.Value.strip())
        if len(set(self.categories)) is not len(self.categories) and event.GetEventType() is not wx.EVT_CLOSE:
            wx.MessageDialog(None, 'Cannot have two or more categories with the same name', APPNAME).ShowModal()
            return
        self.parent.EditCategories(self.categories)
        self.Destroy()


class SettingsDialog(wx.Frame):
    def __init__(self, settings, parent):
        wx.Frame.__init__(self, None, title='Settings', style=NORESIZE, size=(320, 185))
        self.SetIcon(ICON)
        self.panel = wx.Panel(self)
        self.settings, self.parent = settings, parent
        self.tickboxes = list()
        for y, x in enumerate(zip(CUSTOM_SETTINGS, EDIT_SETTINGS_KEYS)):
            wx.StaticText(self.panel, 1, x[0], pos=(5, 10 + (y * 25))).SetFont(FONT2)
            cb = wx.CheckBox(self.panel, 1, pos=(280, 12 + (y * 25)))
            cb.SetValue(self.settings[x[1]])
            self.tickboxes.append(cb)

        self.Bind(wx.EVT_CLOSE, self.submit, self)

        self.done = wx.Button(self.panel, 2, 'Done', pos=(207, 115))
        self.done.Bind(wx.EVT_BUTTON, self.submit)
        self.Center()
        self.Show()

    def submit(self, event):
        for x, y in zip(EDIT_SETTINGS_KEYS, self.tickboxes):
            self.settings[x] = y.GetValue()
        self.parent.SetSettings(self.settings)
        self.Destroy()


class AboutDialog(wx.Frame):
    def __init__(self):
        wx.Frame.__init__(self, None, title='About', style=NORESIZE, size=(315, 293))
        self.SetIcon(ICON)
        self.panel = wx.Panel(self)
        text = wx.StaticText(self.panel, 1, 'About ' + APPNAME, pos=(5, 5))
        text.SetFont(FONT1)

        about = wx.StaticText(self.panel, 1, '{}. Created By {}. Current Version Is: {}'.format(APPDESCRIPTION, APPDEVELOPER, APPVERSION), pos=(5, 45))
        about.Wrap(290)

        for y, x in enumerate(zip(['Home', 'Developer Twitter', 'Improvement Questionaire', 'Sourceforge Download', 'Github Repository'], [HOMEPAGE, TWITTER, SURVEY, SOURCEFORGE, REPO])):
            but = wx.Button(self.panel, 1, x[0], pos=(5, 115 + (27 * y)), size=(290, 25), name=x[1])
            but.Bind(wx.EVT_BUTTON, lambda event: webbrowser.open(event.GetEventObject().GetName()))

        self.Center()
        self.Show()
