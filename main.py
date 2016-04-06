from .headers import NoHeaderError, get_template
from .settings import Settings

from sublime import Region
from sublime_plugin import TextCommand, EventListener

from os.path import split, getctime
from datetime import datetime

import time

CREATION_DATE_PATTERN = r'\d{4}\/\d{2}\/\d{2} \d{2}:\d{2}:\d{2} by [^\s]+'

global settings

def plugin_loaded():
    global settings
    settings = Settings()

def generate_header(view):
    file_path = view.file_name()
    _, file_name = split(file_path)

    template = get_template(file_path)

    created = None
    if is_header_in_view(view):
        created_region = view.find(CREATION_DATE_PATTERN, 0)
        if created_region:
            created = view.substr(created_region)
    if created is None:
        # Using last change time since there is no reliable way to get the
        # creation time of a UNIX file
        created_stamp = datetime.fromtimestamp(getctime(file_path))
        created = settings.timestamp(created_stamp)

    updated = settings.timestamp(time)

    return template % (file_name, settings.by(), created, updated)

def is_header_in_view(view):
    try:
        header = get_template(view.file_name())
    except NoHeaderError:
        return False
    else:
        # Trying to match the first invariant part of the header
        invariant_content_length = header.find('%')
        invariant_content = header[:invariant_content_length]
        region = Region(0, invariant_content_length)

        return (invariant_content == view.substr(region))

class toggle_headerCommand(TextCommand):

    def run(self, edit):
        if is_header_in_view(self.view):
            self.disable(edit)
        else:
            self.enable(edit)

    def enable(self, edit):
        try:
            header = generate_header(self.view)
        except NoHeaderError:
            pass
        else:
            self.view.insert(edit, 0, header)

    def disable(self, edit):
        header = generate_header(self.view)
        header_region = Region(0, len(header))
        self.view.erase(edit, header_region)

class update_headerCommand(TextCommand):

    def run(self, edit):
        if not is_header_in_view(self.view):
            return

        header = generate_header(self.view)
        header_region = Region(0, len(header))
        self.view.replace(edit, header_region, header)

class eventListener(EventListener):

    def on_pre_save(self, view):
        view.window().run_command('update_header')
