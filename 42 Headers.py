import sublime, sublime_plugin
import os, time, datetime, re
from os.path import join, split, getctime, dirname, realpath

PLUGIN_NAME = '42 Headers'
global IS_INIT
IS_INIT = False
PACKAGE_FILE = lambda fileName : join(sublime.packages_path(), PLUGIN_NAME, fileName)
SETTINGS_HAS_HEADER_KEY = 'hasHeader'
HEADER_SUB_DIR = 'headers'

DATE_TIME_FORMAT = '%Y/%m/%d %H:%M:%S'
LOGIN = os.environ.get('USER', 'anonymous')
MAIL = '%s@student.42.fr' % LOGIN
BY = '%s <%s>' % (LOGIN, MAIL)
TIMESTAMP = lambda stamp : '%s by %s' % (stamp, LOGIN)

def LOAD_HEADER(fileName) :
    with open(PACKAGE_FILE(join(HEADER_SUB_DIR, fileName)), 'r') as headerFile :
        return headerFile.read()

HEADERS = {
    '^Makefile$' : 'Makefile.header',
    '^.*\.c|h$'  : 'C.header'
}

def init() :
    global IS_INIT
    IS_INIT = True
    for k, v in HEADERS.items() :
        HEADERS[k] = LOAD_HEADER(v)

def getHeader(filePath) :
    global IS_INIT
    if not IS_INIT : init()
    _, fileName = split(filePath)

    for pattern, header in HEADERS.items() :
        if re.search(pattern, fileName) :
            creationDateTime = datetime.datetime.fromtimestamp(getctime(filePath))
            created = TIMESTAMP(creationDateTime.strftime(DATE_TIME_FORMAT))
            updated = TIMESTAMP(time.strftime(DATE_TIME_FORMAT))
            return header % (fileName, BY, created, updated)

class create_headerCommand(sublime_plugin.TextCommand) :
    def run(self, edit) :
        if not self.view.settings().get(SETTINGS_HAS_HEADER_KEY) :
            header = getHeader(self.view.file_name())
            if header :
                self.view.insert(edit, 0, header)
                self.view.settings().set(SETTINGS_HAS_HEADER_KEY, True)

class update_headerCommand(sublime_plugin.TextCommand) :
    def run(self, edit) :
        if self.view.settings().get(SETTINGS_HAS_HEADER_KEY) :
            header = getHeader(self.view.file_name())
            if header :
                headerRegion = sublime.Region(0, len(header))
                self.view.replace(edit, headerRegion, header)

class disable_headerCommand(sublime_plugin.TextCommand) :
    def run(self, edit) :
        header = getHeader(self.view.file_name())
        if header :
            headerRegion = sublime.Region(0, len(header))
            self.view.erase(edit, headerRegion)
            self.view.settings().set(SETTINGS_HAS_HEADER_KEY, False)

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

class eventListener(sublime_plugin.EventListener) :

    def on_pre_save(self, view) :
        view.window().run_command('update_header')
        view.window().run_command('rstrip_lines')
        view.window().run_command('add_missing_endline')

    def on_load(self, view) :
        header = getHeader(view.file_name())
        hasHeader = False
        if header :
            staticHeaderLength = header.find('\n')
            staticRegion = sublime.Region(0, staticHeaderLength)
            hasHeader = header[:staticHeaderLength] == view.substr(staticRegion)
        view.settings().set(SETTINGS_HAS_HEADER_KEY, hasHeader)
