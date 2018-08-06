import wx
from wx.lib.intctrl import IntCtrl, EVT_INT
import wx.adv
import webbrowser
import extgui
import files
from utils import *
from variables import *


class Tasks(wx.Frame):
    def __init__(self):
        wx.Frame.__init__(self, None, title=APPNAME, size=(800, 680))  # , style=NORESIZE
        self.SetMinSize(wx.Size(800, 680))  # sets min size
        self.tasks, self.settings = files.Load()  # loads settings and tasks
        self.SetIcon(ICON)  # set icon

        # update checking
        if self.settings['updateChecking']:
            self.settings['updateChecking'] = checkForUpdate()

        # initilise some variables
        self.selectedtask = -1
        self.selectedcol = -1
        self.ascending = True
        self.editCategoriesWindow, self.editSettingsWindow, self.taskWindow, self.editCreateTaskWindow, self.AboutWindow = None, None, None, None, None

        self.categories = self.settings['categories']
        self.settings['numOpens'] += 1
        if self.settings['numOpens'] > 5 and self.settings['messages']:
            hints()  # shows some informative messages

        self.Bind(wx.EVT_CLOSE, self.Exit, self)
        self.InitUI()

        self.Maximize(True)
        self.Show(True)

    def InitUI(self):
        # panles used for centering
        mainpanel = wx.Panel(self)
        self.centerpanel = wx.Panel(mainpanel)
        sizer = wx.BoxSizer(wx.VERTICAL)

        self.status = self.CreateStatusBar()

        # top bar creation
        fileMenu = wx.Menu()
        createTaskItem = fileMenu.Append(-1, '&Create Task \tCtrl-n', 'Create a new task')
        deleteTaskItem = fileMenu.Append(-1, '&Delete Task \tCtrl-r', 'Remove current task')
        settingsItem = fileMenu.Append(-1, '&Edit Settings', 'Edit current settings')
        aboutItem = fileMenu.Append(-1, '&About', 'Information about the program')

        helpMenu = wx.Menu()
        githubItem = helpMenu.Append(-1, 'Source', 'Link to the Github repository')
        twitterItem = helpMenu.Append(-1, 'Twitter', 'Follow progress and support')
        surveyItem = helpMenu.Append(-1, 'Survey', 'Help improve the program with your feedback')

        menuBar = wx.MenuBar()
        menuBar.Append(fileMenu, '&File')
        menuBar.Append(helpMenu, '&About')
        self.SetMenuBar(menuBar)

        self.Bind(wx.EVT_MENU, lambda event: webbrowser.open(REPO), githubItem)
        self.Bind(wx.EVT_MENU, lambda event: webbrowser.open(TWITTER), twitterItem)
        self.Bind(wx.EVT_MENU, lambda event: webbrowser.open(SURVEY), surveyItem)
        self.Bind(wx.EVT_MENU, self.CreateTaskWindow, createTaskItem)
        self.Bind(wx.EVT_MENU, self.RemoveTask, deleteTaskItem)
        self.Bind(wx.EVT_MENU, self.EditSettings, settingsItem)
        self.Bind(wx.EVT_MENU, self.About, aboutItem)

        # drawing
        self.DrawTop()
        self.DrawLower()
        self.Sort(None)

        # finish centering
        sizer.AddStretchSpacer()
        sizer.Add(self.centerpanel, 0, wx.CENTER)
        sizer.AddStretchSpacer()
        mainpanel.SetSizer(sizer)

    def DrawTop(self):

        # create task button
        createTaskBtn = wx.Button(self.centerpanel, 1, 'Create Task', pos=(667, 20))
        createTaskBtn.Bind(wx.EVT_BUTTON, self.CreateTaskWindow)
        createTaskBtn.Bind(wx.EVT_ENTER_WINDOW, lambda event: self.status.SetStatusText('Create a new task'))
        createTaskBtn.Bind(wx.EVT_LEAVE_WINDOW, lambda event: self.status.SetStatusText(''))

        # edit task button
        editCategoriesBtn = wx.Button(self.centerpanel, 1, 'Edit Categories', pos=(557, 20))
        editCategoriesBtn.Bind(wx.EVT_BUTTON, self.CategoriesWindow)
        editCategoriesBtn.Bind(wx.EVT_ENTER_WINDOW, lambda event: self.status.SetStatusText('Edit Categories'))
        editCategoriesBtn.Bind(wx.EVT_LEAVE_WINDOW, lambda event: self.status.SetStatusText(''))

        # header
        wx.StaticText(self.centerpanel, 1, 'Tasks:', pos=(25, 20)).SetFont(FONT1)

        # task list
        self.list = wx.ListCtrl(self.centerpanel, 1, style=wx.LC_REPORT | wx.SUNKEN_BORDER | wx.LC_SINGLE_SEL, pos=(25, 60), size=(730, 195))
        self.Bind(wx.EVT_LIST_ITEM_SELECTED, self.SelectTask, self.list)
        self.Bind(wx.EVT_LIST_ITEM_DESELECTED, self.DeselectTask, self.list)
        self.Bind(wx.EVT_LIST_COL_BEGIN_DRAG, lambda event: event.Veto(), self.list)  # Don't let the user change the width of columns
        self.Bind(wx.EVT_LIST_COL_CLICK, self.ColumnClick, self.list)

    def DrawLower(self):

        # task box
        self.taskPanel = wx.StaticBox(self.centerpanel, 1, ' Task:   ', pos=(25, 265), size=(730, 315))  # Added some spaces to give the label a bit more room

        # title
        self.taskTitle = wx.StaticText(self.taskPanel, 1, '', pos=(15, 25), size=(680, 40), style=wx.ST_NO_AUTORESIZE | wx.ST_ELLIPSIZE_END)  # if overflow turn to ellipse
        self.taskTitle.SetFont(FONT2)

        # desciption
        self.taskDescription = wx.StaticText(self.taskPanel, 1, '', pos=(15, 55), size=(680, 105), style=wx.ST_NO_AUTORESIZE)
        self.taskDescription.Wrap(680)  # wraps to 680 pixels

        # date
        self.taskDate = wx.StaticText(self.taskPanel, 1, '', pos=(15, 185))
        self.taskDate.SetFont(FONT2)

        # completion
        self.taskCompletionInput = IntCtrl(self.taskPanel, 1, 0, pos=(110, 210), size=(35, 19), min=0, max=100)
        self.taskCompletionInput.Hide()
        self.Bind(EVT_INT, self.CompletionChanged, self.taskCompletionInput)
        self.taskCompletion = wx.StaticText(self.taskPanel, 1, '', pos=(15, 210))
        self.taskCompletion.SetFont(FONT2)
        self.taskCompletionPer = wx.StaticText(self.taskPanel, 1, '', pos=(152, 210))
        self.taskCompletionPer.SetFont(FONT2)

        # categories
        self.categoryLabel = wx.StaticText(self.taskPanel, 1, '', pos=(15, 235))
        self.categoryLabel.SetFont(FONT2)
        self.categoryIcon = wx.StaticText(self.taskPanel, 1, '', pos=(85, 233))
        self.categoryIcon.SetFont(FONTWING)
        self.categoryText = wx.StaticText(self.taskPanel, 1, '', pos=(105, 235))
        self.categoryText.SetFont(FONT2)

        # subtaks
        self.subtaskLabels, self.subtaskTicks = list(), list()
        self.subtaskLabel = wx.StaticText(self.taskPanel, 1, '', pos=(305, 180))
        self.subtaskLabel.SetFont(FONT2)

        for x in range(2):
            for y in range(3):
                label = wx.StaticText(self.taskPanel, 1, '', pos=(325 + (x * 115), 210 + (y * 25)))
                self.subtaskLabels.append(label)
                tick = wx.CheckBox(self.taskPanel, 1, name=str(y + (3 * x)), pos=(305 + (x * 115), 210 + (y * 25)))
                tick.Hide()
                self.Bind(wx.EVT_CHECKBOX, self.CheckSubtask, tick)
                self.subtaskTicks.append(tick)

        # edit button
        self.taskEdit = wx.Button(self.taskPanel, 1, 'Edit Task', pos=(15, 275))
        self.taskEdit.Bind(wx.EVT_BUTTON, self.EditTaskWindow)
        self.taskEdit.Bind(wx.EVT_ENTER_WINDOW, lambda event: self.status.SetStatusText('Edit Selected Task'))  # For the tips bar
        self.taskEdit.Bind(wx.EVT_LEAVE_WINDOW, lambda event: self.status.SetStatusText(''))
        self.taskEdit.Disable()

        # delete button
        self.taskDelete = wx.Button(self.taskPanel, 1, 'Delete Task', pos=(105, 275))
        self.taskDelete.Bind(wx.EVT_BUTTON, self.RemoveTask)
        self.taskDelete.Bind(wx.EVT_ENTER_WINDOW, lambda event: self.status.SetStatusText('Delete Selected Task'))  # For the tips bar
        self.taskDelete.Bind(wx.EVT_LEAVE_WINDOW, lambda event: self.status.SetStatusText(''))
        self.taskDelete.Disable()

        # shows if their is no selected task
        self.noTask = wx.StaticText(self.taskPanel, 1, 'No Task Selected', pos=(310, 125))
        self.noTask.SetFont(FONT2)

    def UpdateTasks(self):
        self.list.ClearAll()
        self.AddColumns()  # clear all also removes columns :( so have to add them back
        for y, task in enumerate(self.tasks):
            row = self.list.InsertItem(0, task[0])  # title
            importance = task[6]
            self.list.SetItem(row, 1, str(importance))  # importance
            if (importance > 7) and self.settings['tabelHighlighting']:
                self.list.SetItemBackgroundColour(row, ALERTORANGE)
                self.list.SetItemTextColour(row, WHITE)

            self.list.SetItem(row, 2, self.categories[task[7]])  # category

            # completion date
            overdue, date, time = ParseDateTime(task[4])
            if overdue and self.settings['tabelHighlighting']:  # hightlighting overdue objects if setting is ticked
                self.list.SetItemBackgroundColour(row, ALERTRED)
                self.list.SetItemTextColour(row, WHITE)
            if task[3] == 2 or task[3] == 3:
                self.list.SetItem(row, 3, date + time)
            else:
                self.list.SetItem(row, 3, date)

            completion = task[8]
            self.list.SetItem(row, 4, str(completion))  # current completion
            if (completion == 100) and self.settings['tabelHighlighting']:  # hightlighting overdue objects if setting is ticked
                self.list.SetItemBackgroundColour(row, ALERTGREEN)
                self.list.SetItemTextColour(row, WHITE)

    def AddColumns(self):
        for x, y in enumerate(zip(TABLE_HEADERS, [145, 75, 100, 110, 90])):
            self.list.InsertColumn(x, y[0], width=y[1])

    def Exit(self, event):
        if self.settings['deleteOnCompletion']:
            newTasks = [x for x in self.tasks if x[8] is not 100]
        else:
            newTasks = list(self.tasks)

        files.Save(newTasks, self.settings)  # saves files

        for x in [self.editCategoriesWindow, self.editSettingsWindow, self.taskWindow, self.editCreateTaskWindow, self.AboutWindow]:  # close all open windows
            try:
                x.Close(True)
            except Exception as e:
                pass
        self.Destroy()

    def SelectTask(self, event=None):
        if self.list.GetFirstSelected() == -1:  # buffer for whencalled when there is nothing selected?
            return
        else:
            self.selectedtask = len(self.tasks) - self.list.GetFirstSelected() - 1  # list view is in reverse order to actual tasks list

            task = self.tasks[self.selectedtask]
            self.taskTitle.SetLabel(task[0])  # title
            self.taskDescription.SetLabel(task[1])  # description

            # date
            overdue, date, time = ParseDateTime(task[4])
            if task[3] == 2 or task[3] == 3:
                self.taskDate.SetLabel('Due Date: ' + date + time)
            else:
                self.taskDate.SetLabel('Due Date: ' + date)

            if overdue:
                self.taskDate.SetForegroundColour(ALERTRED)

            # completion
            self.taskCompletion.SetLabel('Completiton:')
            self.taskCompletionPer.SetLabel('%')
            self.taskCompletionInput.Show()
            self.taskCompletionInput.SetValue(task[8])

            # category
            category = task[7]
            self.categoryLabel.SetLabel('Category:')
            self.categoryIcon.SetLabel('n')
            self.categoryText.SetLabel(self.categories[category])
            if category is not 0:
                self.categoryIcon.SetForegroundColour(COLOURS[category - 1])
            else:
                self.categoryIcon.SetForegroundColour(BLACK)

            # subtasks
            if len(task[2]) is not 0:
                self.subtaskLabel.SetLabel('Subtasks:')
                for y, x in enumerate(task[2]):
                    self.subtaskLabels[y].SetLabel(x[0])
                    self.subtaskTicks[y].Show()
                    self.subtaskTicks[y].SetValue(x[1])

            # remove 'no task selected' message and enable buttons
            self.noTask.SetLabel('')
            self.taskEdit.Enable()
            self.taskDelete.Enable()

    # resets all changes made in SelectTask
    def DeselectTask(self, event=None):
        self.selectedtask = -1
        self.taskTitle.SetLabel('')
        self.taskDescription.SetLabel('')
        self.taskCompletion.SetLabel('')
        self.taskCompletionPer.SetLabel('')
        self.taskCompletionInput.Hide()
        self.taskDate.SetLabel('')
        self.taskDate.SetForegroundColour(wx.SystemSettings.GetColour(wx.SYS_COLOUR_BACKGROUND))
        self.categoryLabel.SetLabel('')
        self.categoryIcon.SetLabel('')
        self.categoryText.SetLabel('')
        self.subtaskLabel.SetLabel('')

        for y in range(6):  # subtasks
            self.subtaskLabels[y].SetLabel('')
            self.subtaskTicks[y].Hide()

        self.noTask.SetLabel('No Task Selected')
        self.taskEdit.Disable()
        self.taskDelete.Disable()

    def CreateTaskWindow(self, event):
        self.taskWindow = extgui.TaskEditor(self, self.categories)

    def EditTaskWindow(self, event):
        self.editCreateTaskWindow = extgui.TaskEditor(self, self.categories, self.tasks[self.selectedtask], True)

    def AddTask(self, task):  # this function is called from the task editor panel
        self.tasks.append(task)
        self.DeselectTask()
        self.UpdateTasks()

    def AlterTask(self, task):  # this function is called from the task editor panel
        self.tasks[self.selectedtask] = task
        self.UpdateTasks()
        self.DeselectTask()

    def RemoveTask(self, event):
        if self.selectedtask is not -1:
            del self.tasks[self.selectedtask]
            self.DeselectTask()
            self.UpdateTasks()
        else:
            wx.MessageDialog(None, 'No Task Selected', APPNAME).ShowModal()

    def CategoriesWindow(self, event):
        self.DeselectTask()
        self.editCategoriesWindow = extgui.CategoryDialog(self.categories[1:], self)

    def EditCategories(self, categories):
        self.categories = ['None'] + categories
        self.settings['categories'] = self.categories
        self.UpdateTasks()
        self.SelectTask()  # problem

    def SetSettings(self, settings):
        self.settings.update(settings)
        self.UpdateTasks()

    def EditSettings(self, event):
        self.editSettingsWindow = extgui.SettingsDialog(self.settings, self)

    def About(self, event):
        self.AboutWindow = extgui.AboutDialog()

    # subtask editing
    def CheckSubtask(self, event):
        box = event.GetEventObject()
        self.tasks[self.selectedtask][2][int(box.GetName())][1] = box.GetValue()

    def CompletionChanged(self, event):
        x = self.taskCompletionInput.GetValue()
        if 0 <= x <= 100:
            self.tasks[self.selectedtask][8] = x
            self.UpdateTasks()
        event.Skip()

    def ColumnClick(self, event):  # used for sorting
        index = event.GetColumn()
        if index is self.selectedcol:
            self.ascending = not self.ascending
            self.Sort(TABLE_HEADERS[index], self.ascending)
        else:
            self.selectedcol = index
            self.ascending = True
            self.Sort(TABLE_HEADERS[index], self.ascending)

    # sorting the task list
    def Sort(self, rule, ascend=True):
        if rule is TABLE_HEADERS[0]:
            self.tasks.sort(key=lambda x: x[0])
        elif rule is TABLE_HEADERS[1]:
            self.tasks.sort(key=lambda x: x[6], reverse=True)
        elif rule is TABLE_HEADERS[2]:
            self.tasks.sort(key=lambda x: x[7])
        elif rule is TABLE_HEADERS[3]:
            self.tasks.sort(key=lambda x: dateSort(x[4]))
        elif rule is TABLE_HEADERS[4]:
            self.tasks.sort(key=lambda x: x[8])
        else:
            self.tasks.sort(key=lambda x: x[5])
        if not ascend:
            self.tasks = self.tasks[::-1]
        self.UpdateTasks()
