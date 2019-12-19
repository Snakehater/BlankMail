from mttkinter import mtTkinter as tk
from tkinter import ttk
import smtplib
import json
import html
from accountmanager import AccountManager
from testfile import TestFile

from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.mime.image import MIMEImage

TestFile()


root = tk.Tk()
root.title("Mail Styler")
selectedLogin = tk.StringVar(root)

def updateFromEntry(event):
    mailFromEntry.delete(0, 'end')
    mailFromEntry.insert(0, selectedLogin.get())

def updateAccounts():
    TestFile()
    selectedLogin.set('Login')
    savedJson = open('logins.json', "r").read()
    jsonvar = json.loads(savedJson)
    choices = {''}
    for elem in jsonvar:
        choices.add(elem['username'])
    dropDown = ttk.OptionMenu(accountsFrame, selectedLogin, *choices)
    dropDown.grid(row=0, column=0, sticky='e')

def openAccountManager():
    disableManageBtn()
    AccountManager(updateAccounts, enableManageBtn)

def disableManageBtn():
    manageBtn.configure(state="disabled")
    manageBtn.update()

def enableManageBtn():
    manageBtn.configure(state="enabled")
    manageBtn.update()

def disableSendBtn():
    sendBtn.configure(state="disabled")
    sendBtn.update()

def enableSendBtn():
    sendBtn.configure(state="enabled")
    sendBtn.update()

def generateHtml(title, jsonStr):
    jsonvar = json.loads(jsonStr)
    shellHtml = open('customMailShell.html', "r").read()
    titleHtml = open('title.html', "r").read()
    subtitleHtml = open('subtitle.html', "r").read()
    contentHtml = open('content.html', "r").read()

    htmls = list('')
    htmls.append(titleHtml.replace('<!-- input -->', html.escape(title).replace(' ', '&nbsp;')))
    for eachJson in jsonvar:
        if eachJson['type'] == 'subt':
            htmls.append(subtitleHtml.replace('<!-- input -->', html.escape(eachJson['content'])))
        else:
            htmls.append(contentHtml.replace('<!-- input -->', html.escape(eachJson['content'])))
        htmls.append('\n')
    shellParsed = shellHtml.replace('<!-- allContent -->', ''.join(htmls))
    return shellParsed

def generateList():
    text = inputText.get(1.0, "end")[:-1]
    jsonvar = json.loads('[]')
    contentadder = list('')
    subtitleadder = list('')
    idx=0
    error = False
    lastOpenSubtitle = 0
    while idx < len(text):
        char = text[idx]
        # print(char)
        if char == '<':
            lastOpenSubtitle = idx
            if contentadder != list(''):
                jsonvar.append({'type':'cont', 'content':''.join(contentadder)})
                contentadder = list('')
            contentadder = list('')
            running = True
            while idx < len(text) and running:
                idx += 1
                char = text[idx]
                if idx >= len(text) and char != '>':
                    running = False
                    error = True
                elif char == '>':
                    running = False
                else:
                    subtitleadder.append(char)
            if idx == len(text) and char != '>':
                print('error')
            jsonvar.append({'type':'subt', 'content':''.join(subtitleadder)})
            subtitleadder = list('')
        else:
            contentadder.append(char)
        idx += 1
    if contentadder != list(''):
        jsonvar.append({'type':'cont', 'content':''.join(contentadder)})
        contentadder = list('')

    if error is True:
        displayResult(False, code=-1)
        inputText.focus_set()
        return None


    return json.dumps(jsonvar)

def insertsubtitle():
    inputTextTxt = inputText.get(1.0, "end")[:-1]
    if inputTextTxt == '':
        inputText.insert('end', '<>')
    else:
        inputText.insert('end', '\n<>')
    inputText.focus_set()
    inputTextTxtStock = inputText.get(1.0, "end")
    row = inputTextTxtStock.count('\n')
    column = 1
    inputText.mark_set("insert", "%d.%d" % (row, column))

def send():
    disableSendBtn()
    jsonStr = generateList()
    subject = subjectEntry.get()
    html = generateHtml(subject, jsonStr)
    text = inputText.get(1.0, "end")[:-1]
    sender = mailFromEntry.get()
    recipient = mailToEntry.get()

    if selectedLogin.get() == 'Login':
        dropDown.focus_set()
        displayResult(False, code=-3)
    elif sender == '':
        mailFromEntry.focus_set()
        displayResult(False, code=-2)
    elif recipient == '':
        mailToEntry.focus_set()
        displayResult(False, code=-2)
    elif subject == '':
        subjectEntry.focus_set()
        displayResult(False, code=-2)
    elif inputText == '':
        inputText.focus_set()
        displayResult(False, code=-1)
    else:
        sendMail(selectedLogin.get(), subject, sender, recipient, html, text)#'vitu0216@fridaskolan.se'

def addNewLines(text, maxChars):
    idx = 0
    counter = 0
    spaceAdded = False
    lastSpace = 0
    returnString = list('')
    for char in text:
        returnString.append(char)
        if char is ' ':
            lastSpace = idx
            spaceAdded = True

        if spaceAdded is True and counter == maxChars+1:
            counter = 0
            returnString[lastSpace] = '\n'
        counter += 1
        idx += 1
    return ''.join(returnString)

def displayResult(confirmed, text='', code=534):
    if confirmed is not True:
        errorLabel.grid(padx=10, row=errorLabelRow, sticky='ew', columnspan=2)
        if code is 534:
            progText = addNewLines('Something went wrong, login credentials may be wrong or "less secure apps" are disabled within your google account settings', 50)
        elif code is 550:
            progText = addNewLines('This message was classified as SPAM and may not be delivered', 50)
        elif code is 421:
            progText = addNewLines('The service is not available and the connection will be closed.', 50)
        elif code is 451:
            progText = addNewLines('The command has been aborted due to a server error. Not your fault.', 50)
        elif code is 555:
            progText = addNewLines('The server does not recognize the email address format, and delivery is not possible.', 50)
        elif code is -1:
            progText = addNewLines('Input field is invalid, check "< and >"', 50)
        elif code is -2:
            progText = addNewLines('Input field is invalid', 50)
        elif code is -3:
            progText = addNewLines('Please select or/and add account details', 50)
        else:
            progText = addNewLines('Could not send, please try again later', 50)
        resultLabel.configure(text=progText, fg='#ff0000', height=progText.count('\n')+1)
        progText = addNewLines(text, 50)
        if text is not '':
            passerrorLabel.configure(text=("Error: "+progText), height=progText.count('\n')+1)
    else:
        resultLabel.configure(text='Sent!', fg='#00ff00', height=1)
        errorLabel.grid_remove()
    errorLabel.update()
    resultLabel.update()
    enableSendBtn()
def resetResult(arg):
    resultLabel.configure(text='Not sent', fg="#5d5d5d", height=1)
    errorLabel.grid_remove()
    errorLabel.update()
    resultLabel.update()

def sendMail(username, subject, sender, recipient, html, text):
    sendBtn.update()
    # Get logins and then get data associated with username
    try:
        savedJson = open('logins.json', "r").read()
        jsonvar = json.loads(savedJson)
        loginElem = json.loads('{}')
        for elem in jsonvar:
            if elem['username'] == username:
                loginElem = elem
                break
        if username != 'Login':
            # Create message container - the correct MIME type is multipart/alternative.
            msgRoot = MIMEMultipart('related')
            # msg['Subject'] = subjectEntry.get()
            msgRoot['Subject'] = subject
            msgRoot['From'] = sender
            msgRoot['To'] = recipient

            msgAlternative = MIMEMultipart('alternative')
            msgRoot.attach(msgAlternative)

            # Create the body of the message (a plain-text and an HTML version).
            # text = inputText.get(1, 'end')[:-1]
            text = text
            # entireHtml = open('customEntireMail.html', "r").read()
            # html = html

            # Record the MIME types of both parts - text/plain and text/html.
            part1 = MIMEText(text, 'plain')
            part2 = MIMEText(html, 'html')

            # Attach parts into message container.
            # According to RFC 2046, the last part of a multipart message, in this case
            # the HTML message, is best and preferred.
            msgAlternative.attach(part1)
            msgAlternative.attach(part2)

            # This example assumes the image is in the current directory
            githubpng = open('github.png', 'rb')
            githubimage = MIMEImage(githubpng.read())
            githubpng.close()

            googleplaypng = open('googleplay.png', 'rb')
            googleplayimage = MIMEImage(googleplaypng.read())
            googleplaypng.close()

            instagrampng = open('instagram.png', 'rb')
            instagramimage = MIMEImage(instagrampng.read())
            instagrampng.close()

            snapchatpng = open('snapchat.png', 'rb')
            snapchatimage = MIMEImage(snapchatpng.read())
            snapchatpng.close()

            twitterpng = open('twitter.png', 'rb')
            twitterimage = MIMEImage(twitterpng.read())
            twitterpng.close()

            # Define the image's ID as referenced above
            githubimage.add_header('Content-ID', '<githubpng>')
            msgRoot.attach(githubimage)
            googleplayimage.add_header('Content-ID', '<googleplaypng>')
            msgRoot.attach(googleplayimage)
            instagramimage.add_header('Content-ID', '<instagrampng>')
            msgRoot.attach(instagramimage)
            snapchatimage.add_header('Content-ID', '<snapchatpng>')
            msgRoot.attach(snapchatimage)
            twitterimage.add_header('Content-ID', '<twitterpng>')
            msgRoot.attach(twitterimage)

            # # Send the message via local SMTP server.
            # s = smtplib.SMTP('localhost')
            # # sendmail function takes 3 arguments: sender's address, recipient's address
            # # and message to send - here it is sent as one string.
            # s.sendmail(mailFromEntry.get(), mailToEntry.get(), msg.as_string())
            # s.quit()
            try:
                server = smtplib.SMTP_SSL(loginElem['server'], 465) #'smtp.gmail.com'
                # server = smtplib.SMTP_SSL('send.one.com', 465)
                server.ehlo()
                # server.login('vigor.turujlija@gmail.com', 'mdorutrbqojgdxwn')
                # server.login('vigor@elvigo.com', 'stov04are')
                server.login(loginElem['username'], loginElem['password'])
                server.sendmail(sender, recipient, msgRoot.as_string())
                server.quit()
                server.close()
                displayResult(True)
            except smtplib.SMTPException as e:
                displayResult(False, text=str(e))
        else:
            print("Please select or add login item")
    except Exception as e:
        print("Please select or add login item")

rowCount=0

accountsFrame = tk.Frame(root)

selectedLogin.set('Login')
savedJson = open('logins.json', "r").read()
jsonvar = json.loads(savedJson)
choices = {''}
for elem in jsonvar:
    choices.add(elem['username'])
dropDown = ttk.OptionMenu(accountsFrame, selectedLogin, *choices, command=updateFromEntry)
dropDown.grid(row=0, column=0, sticky='e')#.grid(padx=10, pady=10, sticky='w', row=rowCount)

manageBtn = ttk.Button(accountsFrame, text='manage', command=openAccountManager)
manageBtn.grid(row=0, column=1, sticky='w')#.grid(row=rowCount, sticky='w')

accountsFrame.grid(row=rowCount, column=0, columnspan=2, sticky='w')

rowCount += 1

tk.Label(root, height=1, width=5, text='From', anchor='w').grid(column=0, row=rowCount, padx=10)
mailFromEntry = tk.Entry(root, width=35)
# mailFromEntry.insert(0, 'vitu0216@fridaskolan.se')
mailFromEntry.grid(column=1, row=rowCount, padx=10)
mailFromEntry.bind('<KeyRelease>', resetResult)

rowCount += 1

tk.Label(root, height=1, width=5, text='To', anchor='w').grid(column=0, row=rowCount, padx=10)
mailToEntry = tk.Entry(root, width=35)
# mailToEntry.insert(0, 'vitu0216@fridaskolan.se')
mailToEntry.grid(column=1, row=rowCount, padx=10)
mailToEntry.bind('<KeyRelease>', resetResult)

rowCount += 1

tk.Label(root, height=1, width=5, text='Subject', anchor='w').grid(column=0, row=rowCount, padx=10)
subjectEntry = tk.Entry(root, width=35)
# subjectEntry.insert(0, "Lorem")
subjectEntry.grid(column=1, row=rowCount, padx=10)
subjectEntry.bind('<KeyRelease>', resetResult)

rowCount += 1

tk.Label(root, text='Message:', height=1).grid(padx=10, row=rowCount, sticky='ew', columnspan=2)

rowCount += 1

scrollbar = tk.Scrollbar(root)
scrollbar.grid(column=2, row=rowCount, sticky='w')

inputText = tk.Text(root, width=40, height=20, wrap='word', highlightthickness='0', borderwidth=2, relief="sunken", yscrollcommand=scrollbar.set)
inputText.grid(column=0, row=rowCount, columnspan=2, padx=10, sticky='ew')
inputText.bind('<KeyRelease>', resetResult)
inputText.insert("1.0", "<Lorem ipsum>\nLorem ipsum dolor sit amet, consectetur adipisicing elit, sed do eiusmod tempor incididunt ut labore et dolore magna aliqua. Ut enim ad minim veniam, quis nostrud exercitation ullamco laboris nisi ut aliquip ex ea commodo consequat. Duis aute irure dolor in reprehenderit in voluptate velit esse cillum dolore eu fugiat nulla pariatur. Excepteur sint occaecat cupidatat non proident, sunt in culpa qui officia deserunt mollit anim id est laborum.")

scrollbar.configure(command=inputText.yview)

rowCount += 1

ttk.Button(root, text='insert subtitle', width=len('insertsubtitle'), command=insertsubtitle).grid(column=0, row=rowCount, padx=10)

rowCount += 1

sendBtn = ttk.Button(root, text='Send', command=(lambda: send()))
sendBtn.grid(column=0, row=rowCount, columnspan=2, padx=10, pady=10, sticky='ew')

rowCount += 1

resultLabel = tk.Label(root, text='Not sent', height=1, fg="#5d5d5d")
# resultLabel = tk.Text(root, height=1, width=40, fg="#5d5d5d", wrap='word')
# resultLabel.insert('insert', 'Not sent')
resultLabel.grid(padx=10, row=rowCount, sticky='ew', columnspan=2)
resultRow=rowCount

rowCount += 1

errorLabel = tk.Label(root, text='', height=1, fg="#5d5d5d")
errorLabelRow = rowCount

tk.mainloop()
