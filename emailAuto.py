import imaplib
import email
import os
import re
from datetime import date
import email
from email.header import decode_header

emails = []
mails = []

# gmail login information
EMAIL_ADDRESS = os.environ.get('GM_USER')
EMAIL_PASSWORD = os.environ.get('GM_PASSWORD')

# establish connections with gmail acc
imap = imaplib.IMAP4_SSL("imap.gmail.com")
imap.login(EMAIL_ADDRESS, EMAIL_PASSWORD)

# selecting inbox and choose relevant emails
imap.select("INBOX")

# emails that need to be deleted
file = open('emails.txt', 'r', encoding='utf-8')
while True:
    holder = file.readline().rstrip('\n')
    if (holder == ""):
        file.close()
        break
    else:
        emails.append(holder)

# gather emails from mailbox
for e in emails:
    status, msg = imap.search(None, 'FROM '+e)
    if msg[0]:
        msg = msg[0].split(b' ')
        mails.extend(msg)

# number of mails deletion
print("mails being deleted: ", len(mails))

if len(mails) > 0:
    for mail in mails:
        _, msg = imap.fetch(mail, "(RFC822)")
        for response in msg:
            if isinstance(response, tuple):
                msg = email.message_from_bytes(response[1])
                # decode the email subject
                subject = decode_header(msg["Subject"])[0][0]
                if isinstance(subject, bytes):
                    # if it's a bytes type, decode to str
                    subject = subject.decode()
                print("Deleting: ", subject, mail)

        imap.store(mail, "+FLAGS", "\\Deleted")
        print("Deleted: " + mail.decode())
else:
    print("No new spam mails to be deleted!")

imap.expunge()
imap.close()
imap.logout()