from mttkinter import mtTkinter as tk
from tkinter import ttk
import smtplib

from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.mime.image import MIMEImage

def insertsubtitle():
    inputTextTxt = inputText.get(1.0, "end")[:-1]
    if inputTextTxt == '':
        inputText.insert('end', '<subt></subt>')
    else:
        inputText.insert('end', '\n<subt></subt>')
    inputText.focus_set()
    inputTextTxtStock = inputText.get(1.0, "end")
    row = inputTextTxtStock.count('\n')
    column = 6
    inputText.mark_set("insert", "%d.%d" % (row, column))

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
        else:
            progText = addNewLines('Could not send, please try again later', 50)
        resultLabel.configure(text=progText, fg='#ff0000', height=progText.count('\n')+1)
        progText = addNewLines(text, 50)
        errorLabel.configure(text=("Error: "+progText), height=progText.count('\n')+1)
    else:
        resultLabel.configure(text='Sent!', fg='#00ff00', height=1)
        errorLabel.grid_remove()
    errorLabel.update()
    resultLabel.update()
def resetResult(arg):
    resultLabel.configure(text='Not sent', fg="#5d5d5d", height=1)
    errorLabel.grid_remove()
    errorLabel.update()
    resultLabel.update()

def send():
    sendBtn.update()
    # Create message container - the correct MIME type is multipart/alternative.
    msgRoot = MIMEMultipart('related')
    # msg['Subject'] = subjectEntry.get()
    msgRoot['Subject'] = "Link"
    msgRoot['From'] = mailFromEntry.get()
    msgRoot['To'] = mailToEntry.get()

    msgAlternative = MIMEMultipart('alternative')
    msgRoot.attach(msgAlternative)

    # Create the body of the message (a plain-text and an HTML version).
    # text = inputText.get(1, 'end')[:-1]
    text = "Hey"
    entireHtml = open('customEntireMail.html', "r").read()
    html = entireHtml

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
        server = smtplib.SMTP_SSL('smtp.gmail.com', 465)
        # server = smtplib.SMTP_SSL('send.one.com', 465)
        server.ehlo()
        # server.login('vigor.turujlija@gmail.com', 'mdorutrbqojgdxwn')
        # server.login('vigor@elvigo.com', 'stov04are')
        server.login('vitu0216@fridaskolan.se', '0402169114')
        server.sendmail(mailFromEntry.get(), mailToEntry.get(), msgRoot.as_string())
        server.quit()
        server.close()
        displayResult(True)
    except smtplib.SMTPException as e:
        displayResult(False, text=str(e))

root = tk.Tk()
root.title("Mail Styler")

rowCount=0

tk.Label(root, height=1, width=5, text='From', anchor='w').grid(column=0, row=rowCount, padx=10)
mailFromEntry = tk.Entry(root, width=35)
mailFromEntry.grid(column=1, row=rowCount, padx=10)
mailFromEntry.bind('<KeyRelease>', resetResult)

rowCount += 1

tk.Label(root, height=1, width=5, text='To', anchor='w').grid(column=0, row=rowCount, padx=10)
mailToEntry = tk.Entry(root, width=35)
mailToEntry.grid(column=1, row=rowCount, padx=10)
mailToEntry.bind('<KeyRelease>', resetResult)

rowCount += 1

tk.Label(root, height=1, width=5, text='Subject', anchor='w').grid(column=0, row=rowCount, padx=10)
subjectEntry = tk.Entry(root, width=35)
subjectEntry.grid(column=1, row=rowCount, padx=10)
subjectEntry.bind('<KeyRelease>', resetResult)

rowCount += 1

tk.Label(root, text='Message:', height=1).grid(padx=10, row=rowCount, sticky='ew', columnspan=2)

rowCount += 1

inputText = tk.Text(root, width=40, height=20, highlightthickness='0', borderwidth=2, relief="sunken")
inputText.grid(column=0, row=rowCount, columnspan=2, padx=10, sticky='ew')
inputText.bind('<KeyRelease>', resetResult)

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
