from sublime import load_settings

import os

class Settings:

    SETTINGS_FILE = '42-headers.sublime-settings'

    LOGIN_KEY = 'login'

    DATE_TIME_FORMAT = '%Y/%m/%d %H:%M:%S'

    def __init__(self):
        self.all = load_settings(Settings.SETTINGS_FILE)

        self.update_login()
        self.all.add_on_change(Settings.LOGIN_KEY, self.update_login)

    def update_login(self):
        self.login = self.all.get(
            Settings.LOGIN_KEY,
            os.getenv('USER', 'anonymous')
        )

    def timestamp(self, stamp):
        formatted = stamp.strftime(Settings.DATE_TIME_FORMAT)

        return '%s by %s' % (formatted, self.login)

    def by(self):
        mail = '%s@student.42.fr' % self.login

        return '%s <%s>' % (self.login, mail)

