import os
from dotenv import load_dotenv

load_dotenv()
sportmetoken = str(os.getenv("BOT_TOKEN"))

chatid = str(os.getenv("ADMIN_ID"))

logindata = {
    'inbox': {
        "username": str(os.getenv("INBOXMAIL")),
        "password": str(os.getenv("INBOXPWD"))
    },
    'gmail': {
        "username": str(os.getenv("GMAIL")),
        "password": str(os.getenv("GMAILPWD"))
    },
    'mail': {
        "username": str(os.getenv("MAIL")),
        "password": str(os.getenv("MAILPWD"))
    },
}
