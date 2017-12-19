import sublime
import sublime_plugin
from datetime import datetime
import io
import os
import re
import subprocess
import sys

def get_setting(key, default=None):
    settings = sublime.load_settings('tmux.sublime-settings')
    os_specific_settings = {}

    if sys.platform == 'darwin':
        os_specific_settings = sublime.load_settings('tmux (OSX).sublime-settings')
    else:
        os_specific_settings = sublime.load_settings('tmux (Linux).sublime-settings')

    return os_specific_settings.get(key, settings.get(key, default))

class TmuxCommand():
    def resolve_file_path(self):
        if self.window.active_view().file_name():
            return os.path.dirname(self.window.active_view().file_name())
        elif len(self.window.folders()):
            return self.window.folders()[0]
        else:
            sublime.status_message('tmux: Could not resolve file path - opening at home directory')

            return '~/'

    def check_tmux_status(self):
        tmux_status = subprocess.Popen(['tmux', 'info'])
        tmux_status.wait()

        return tmux_status.returncode is 0

    def get_active_tmux_sessions(self):
        parts = ['name', 'windows', 'created', 'attached', 'width', 'height']
        list_sessions = subprocess.Popen([
            'tmux',
            'list-sessions',
            '-F',
            '#{session_' + '} #{session_'.join(parts) + '}'
        ], stdout=subprocess.PIPE)

        return [dict(zip(parts, line.strip().split(' '))) for line in io.TextIOWrapper(list_sessions.stdout)]

    def format_session_choices(self, sessions):
        return list(map(
            lambda session: [
                '{}: {} window{}'.format(session['name'], session['windows'], 's'[int(session['windows']) == 1:]),
                '{:%c}'.format(datetime.fromtimestamp(int(session['created']))),
                '{}x{}{}'.format(session['width'], session['height'], ' (attached)' if int(session['attached']) else '')
            ],
            sessions
        ))

    def on_session_selected(self, index):
        if index == -1:
            return

        self.command_args.extend(['-t', self.attached_sessions[index]['name'] + ':'])
        self.execute()

    def run_tmux(self, path, parameters, split):
        try:
            if self.check_tmux_status():
                self.attached_sessions = list(filter(lambda x: int(x['attached']), self.get_active_tmux_sessions()))
                self.command_args = ['tmux', 'split-window' if split else 'new-window']
                self.command_args.extend(parameters)

                if split == 'horizontal':
                    self.command_args.append('-h')

                if path:
                    self.command_args.extend(['-c', path])

                if len(self.attached_sessions) > 1:
                    return self.window.show_quick_panel(
                        self.format_session_choices(self.attached_sessions),
                        self.on_session_selected
                    )

                self.execute()
        except Exception as exception:
            sublime.error_message('tmux: ' + str(exception))

    def execute(self):
        try:
            subprocess.Popen(self.command_args)
        except Exception as exception:
            sublime.error_message('tmux: ' + str(exception))

class OpenTmuxCommand(sublime_plugin.WindowCommand, TmuxCommand):
    def run(self, path=None, split=None):
        if not path:
            path = self.resolve_file_path()

        self.run_tmux(path, [], split)

class OpenTmuxProjectFolderCommand(sublime_plugin.WindowCommand, TmuxCommand):
    def run(self, path=None, split=None):
        parameters=[]

        if not path:
            path = self.resolve_file_path()

        matched_folders = [x for x in self.window.folders() if path.find(x) == 0]

        if len(matched_folders):
            path = matched_folders[0]

            if get_setting('set_project_window_name', True):
                parameters.extend(['-n', path.split(os.sep)[-1]])

        self.run_tmux(path, parameters, split)
