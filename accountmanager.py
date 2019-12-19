from tkinter import ttk

class AccountManager:

    json = __import__('json')
    time = __import__('time')
    mttkinter = __import__('mttkinter')
    tk = mttkinter.mtTkinter
    tkinter = __import__('tkinter', globals(), locals(), ['ttk'], 0)
    ttk = tkinter.ttk
    threading = __import__('threading')
    math = __import__('math')
    TestFile = __import__('testfile').TestFile

    def __init__(self, updateAccountsIn, enableManageBtnIn):

        self.updateAccounts = updateAccountsIn
        self.enableManageBtn = enableManageBtnIn


        self.root = self.tk.Tk()
        self.root.title('Accounts')
        self.root.bind("<Destroy>", self.destroy)

        self.loadWidgets()

        self.tk.mainloop()

    def loadWidgets(self):
        self.updateAccounts()
        self.remove_all(self.root)
        rowCount = 0

        self.tk.Label(self.root, text='<email>').grid(row=rowCount, column=0)
        self.tk.Label(self.root, text='<password>').grid(row=rowCount, column=1)
        self.tk.Label(self.root, text='<smtp server>').grid(row=rowCount, column=2)

        rowCount += 1

        # frame = self.tk.Frame(self.root)
        self.usernameEntry = self.tk.Entry(self.root, text='username')
        self.usernameEntry.grid(row=rowCount, column=0)
        self.passwordEntry = self.tk.Entry(self.root, text='password')
        self.passwordEntry.grid(row=rowCount, column=1)
        self.serverEntry = self.tk.Entry(self.root, text='server')
        self.serverEntry.grid(row=rowCount, column=2)
        self.addBtn = self.tk.Button(self.root, text='Add', command=self.addAccount)
        self.addBtn.grid(row=rowCount, column=3)

        self.TestFile()
        savedJson = open('logins.json', "r").read()
        jsonvar = self.json.loads(savedJson)
        rowCount += 1
        for elem in jsonvar:
            self.tk.Label(self.root, text=elem['username']).grid(row=rowCount, column=0, sticky='w', padx=10)
            self.tk.Label(self.root, text=elem['password']).grid(row=rowCount, column=1, sticky='w', padx=10)
            self.tk.Label(self.root, text=elem['server']).grid(row=rowCount, column=2, sticky='w', padx=10)
            self.tk.Button(self.root, text='remove', command=lambda: (self.deleteAccount(elem['username']))).grid(row=rowCount, column=3)
            rowCount += 1

    def addAccount(self):
        if self.usernameEntry.get() == '':
            self.usernameEntry.focus_set()
        elif self.passwordEntry.get() == '':
            self.passwordEntry.focus_set()
        elif self.serverEntry.get() == '':
            self.serverEntry.focus_set()
        else:
            if self.checkSaved(self.usernameEntry.get(), self.passwordEntry.get(), self.serverEntry.get()) is not True:
                jsonvar = self.json.loads('{}')
                jsonvar['username'] = self.usernameEntry.get()
                jsonvar['password'] = self.passwordEntry.get()
                jsonvar['server'] = self.serverEntry.get()

                self.TestFile()
                savedJson = open('logins.json', "r").read()
                oldJson = self.json.loads(savedJson)
                oldJson.append(jsonvar)
                with open('logins.json', 'w') as outfile:
                    self.json.dump(oldJson, outfile)
                self.usernameEntry.delete(0, 'end')
                self.passwordEntry.delete(0, 'end')
                self.serverEntry.delete(0, 'end')
                self.loadWidgets()
            else:
                self.usernameEntry.focus_set()
    def checkSaved(self, username, password, server):
        self.TestFile()
        savedJson = open('logins.json', "r").read()
        jsonvar = self.json.loads(savedJson)
        for elem in jsonvar:
            if elem['username'] == username:
                return True
        return False

    def deleteAccount(self, username):
        self.TestFile()
        savedJson = open('logins.json', "r").read()
        jsonvar = self.json.loads(savedJson)
        jsonWork = self.json.loads('[]')
        for elem in jsonvar:
            if elem['username'] == username:
                pass
            else:
                jsonWork.append(elem)
        with open('logins.json', 'w') as outfile:
            self.json.dump(jsonWork, outfile)
        self.loadWidgets()

    def all_children (self, window) :
        _list = window.winfo_children()

        for item in _list :
            if item.winfo_children() :
                _list.extend(item.winfo_children())

        return _list
    def remove_all(self, window):
        widget_list = self.all_children(window)
        for item in widget_list:
            item.grid_remove()

    def destroy(self, event):
        self.enableManageBtn()
        self.updateAccounts()
