from mttkinter import mtTkinter as tk
from tkinter import ttk
import smtplib

from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText

def send(arg):
    # Create message container - the correct MIME type is multipart/alternative.
    msg = MIMEMultipart('alternative')
    msg['Subject'] = "Link"
    msg['From'] = mailFromEntry.get()
    msg['To'] = mailToEntry.get()

    # Create the body of the message (a plain-text and an HTML version).
    text = "Hi!\nHow are you?\nHere is the link you wanted:\nhttp://www.python.org"
    html = """\
    <html>
      <head></head>
      <body>
        <p>Hi!<br>
           How are you?<br>
           Here is the <a href="http://www.python.org">link</a> you wanted.
        </p>
      </body>
    </html>
    """

    # Record the MIME types of both parts - text/plain and text/html.
    part1 = MIMEText(text, 'plain')
    part2 = MIMEText(html, 'html')

    # Attach parts into message container.
    # According to RFC 2046, the last part of a multipart message, in this case
    # the HTML message, is best and preferred.
    msg.attach(part1)
    msg.attach(part2)

    # Send the message via local SMTP server.
    s = smtplib.SMTP('localhost')
    # sendmail function takes 3 arguments: sender's address, recipient's address
    # and message to send - here it is sent as one string.
    s.sendmail(mailFromEntry.get(), mailToEntry.get(), msg.as_string())
    s.quit()

root = tk.Tk()
root.title("Stylish Mail")

rowCount=0

tk.Label(root, height=1, width=5, text='From', anchor='w').grid(column=0, row=rowCount, padx=10)
mailFromEntry = tk.Entry(root, width=35)
mailFromEntry.grid(column=1, row=rowCount, padx=10)

rowCount += 1

tk.Label(root, height=1, width=5, text='To', anchor='w').grid(column=0, row=rowCount, padx=10)
mailToEntry = tk.Entry(root, width=35)
mailToEntry.grid(column=1, row=rowCount, padx=10)

rowCount += 1

tk.Label(root, height=1, width=5, text='Subject', anchor='w').grid(column=0, row=rowCount, padx=10)
subjectEntry = tk.Entry(root, width=35)
subjectEntry.grid(column=1, row=rowCount, padx=10)

rowCount += 1

tk.Label(root, text='Message:', height=1).grid(padx=10, row=rowCount, sticky='ew', columnspan=2)

rowCount += 1

inputText = tk.Text(root, width=40, height=20, highlightthickness='0', borderwidth=2, relief="sunken")
inputText.grid(column=0, row=rowCount, columnspan=2, padx=10, sticky='ew')

rowCount += 1

sendBtn = ttk.Button(root, text='Send', command=(lambda: send()))
sendBtn.grid(column=0, row=rowCount, columnspan=2, padx=10, pady=10, sticky='ew')

tk.mainloop()
