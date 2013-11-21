import sublime, sublime_plugin
import os, time, datetime
from os.path import join, split, getctime

PLUGIN_NAME = '42 Headers'

MAKEFILE_HEADER_FILE = 'Makefile.header'
C_HEADER_FILE = 'c.header'

MAKEFILE_FILE_NAME = 'Makefile'

DATE_TIME_FORMAT = '%Y/%m/%d %H:%M:%S'

SETTINGS_HAS_HEADER_KEY = 'hasHeader'

DEFAULT_LOGIN = 'anonymous'

HEADER_SIZE = 892

MAIL_PATTERN = '%s@student.42.fr'

def getHeader(filePath) :
    _, fileName = split(filePath)

    login = os.environ.get('USER', DEFAULT_LOGIN)
    mail = MAIL_PATTERN % login

    by = '%s <%s>' % (login, mail)
    creationDateTime = datetime.datetime.fromtimestamp(getctime(filePath))
    created = '%s by %s' % (creationDateTime.strftime(DATE_TIME_FORMAT), login)
    updated = '%s by %s' % (time.strftime(DATE_TIME_FORMAT), login)

    headerFile = None
    if fileName == MAKEFILE_FILE_NAME :
        headerFile = MAKEFILE_HEADER_FILE
    else :
        _, ext = os.path.splitext(fileName)
        if ext == '.c' or ext == '.h' :
            headerFile = C_HEADER_FILE

    if headerFile :
        headerPath = join(sublime.packages_path(), PLUGIN_NAME, headerFile)
        with open(headerPath, 'r') as headerFile :
            return headerFile.read() % (fileName, by, created, updated)

class create_headerCommand(sublime_plugin.TextCommand) :
    def run(self, edit) :
        header = getHeader(self.view.file_name())
        if header :
            self.view.insert(edit, 0, header)
            self.view.settings().set(SETTINGS_HAS_HEADER_KEY, True)

class update_headerCommand(sublime_plugin.TextCommand) :
    def run(self, edit) :
        if self.view.settings().has(SETTINGS_HAS_HEADER_KEY) :
            header = getHeader(self.view.file_name())
            headerRegion = sublime.Region(0, HEADER_SIZE)
            self.view.replace(edit, headerRegion, header)

class remove_headerCommand(sublime_plugin.TextCommand) :
    def run(self, edit) :
        if self.view.settings().has(SETTINGS_HAS_HEADER_KEY) :
            headerRegion = sublime.Region(0, HEADER_SIZE)
            self.view.erase(edit, headerRegion)
            self.view.settings().erase(SETTINGS_HAS_HEADER_KEY)

class add_missing_endlineCommand(sublime_plugin.TextCommand) :
    def run(self, edit) :
        textSize = self.view.size();
        i = textSize - 1
        while self.view.substr(i) == '\n' :
            i -= 1;
        regionToReplace = sublime.Region(i + 1, textSize)
        self.view.replace(edit, regionToReplace, '\n')

class rstrip_linesCommand(sublime_plugin.TextCommand) :
    def run(self, edit) :
        fullRegion = sublime.Region(0, self.view.size())
        lines = self.view.lines(fullRegion)
        for line in reversed(lines) :
            lineRegion = self.view.line(line)
            stripped = self.view.substr(lineRegion).rstrip()
            self.view.replace(edit, lineRegion, stripped)

class update_headerListener(sublime_plugin.EventListener) :
    def on_pre_save(self, view) :
        view.window().run_command('update_header')
        view.window().run_command('rstrip_lines')
        view.window().run_command('add_missing_endline')
