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

    def update_window_layout(self):
        args = ['tmux', 'select-layout']

        if get_setting('arrange_panes_on_split') == 'even':
            args.append('even-' + ('horizontal' if '-h' in self.command_args else 'vertical'))
        else:
            args.append('tiled')

        if '-t' in self.command_args:
            args.extend(['-t', self.command_args[self.command_args.index('-t') + 1]])

        subprocess.Popen(args)

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

    def run_tmux(self, parameters, split):
        try:
            if self.check_tmux_status():
                self.attached_sessions = list(filter(lambda x: int(x['attached']), self.get_active_tmux_sessions()))
                self.command_args = ['tmux', 'split-window' if split else 'new-window']
                self.command_args.extend(parameters)

                if split == 'horizontal':
                    self.command_args.append('-h')

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
            for path in self.paths:
                subprocess.Popen(self.command_args + ['-c', path])

            if 'split-window' in self.command_args and get_setting('arrange_panes_on_split'):
                self.update_window_layout()

        except Exception as exception:
            sublime.error_message('tmux: ' + str(exception))

class OpenTmuxCommand(sublime_plugin.WindowCommand, TmuxCommand):
    def run(self, paths=[], split=None):
        self.paths = [os.path.dirname(path) if not os.path.isdir(path) else path for path in paths]

        if not len(self.paths):
            self.paths.append(self.resolve_file_path())

        self.run_tmux([], split)

class OpenTmuxProjectFolderCommand(sublime_plugin.WindowCommand, TmuxCommand):
    def run(self, split=None):
        parameters=[]
        path = self.resolve_file_path()
        matched_dirs = [x for x in self.window.folders() if path.find(x) == 0]

        if len(matched_dirs):
            path = matched_dirs[0]

            if get_setting('set_project_window_name', True):
                parameters.extend(['-n', path.split(os.sep)[-1]])

        self.paths = [path]
        self.run_tmux(parameters, split)
