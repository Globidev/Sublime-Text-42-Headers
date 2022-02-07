from sublime import load_settings

import os

class Settings:

    SETTINGS_FILE = '42-headers.sublime-settings'

    LOGIN_KEY = 'login'
    
    MAIL_KEY = 'mail'

    DATE_TIME_FORMAT = '%Y/%m/%d %H:%M:%S'

    # If SOFT is True, the update is only done if the redo stack is empty
    SOFT = False

    def __init__(self):
        self.all = load_settings(Settings.SETTINGS_FILE)
        self.update_login()
        self.all.add_on_change(Settings.LOGIN_KEY, self.update_login)
        self.update_mail()
        self.all.add_on_change(Settings.MAIL_KEY, self.update_mail)

    def update_login(self):
        self.login = self.all.get(
            Settings.LOGIN_KEY,
            os.getenv('USER', 'anonymous')
        )

    def update_mail(self):
        self.mail = self.all.get(
            Settings.MAIL_KEY, self.login + '@student.42.fr',
        )

    def timestamp(self, stamp):
        formatted = stamp.strftime(Settings.DATE_TIME_FORMAT)

        return '%s by %s' % (formatted, self.login)

    def by(self):
        return '%s <%s>' % (self.login, self.mail)

