import sublime
import sublime_plugin
import io
import os
import re
import subprocess
import sys

def get_setting(key, default=None):
    settings = sublime.load_settings('SublimeTmux.sublime-settings')
    os_specific_settings = {}

    if sys.platform == 'darwin':
        os_specific_settings = sublime.load_settings('SublimeTmux (OSX).sublime-settings')
    else:
        os_specific_settings = sublime.load_settings('SublimeTmux (Linux).sublime-settings')

    return os_specific_settings.get(key, settings.get(key, default))

class TmuxCommand():
    def resolve_file_path(self, path):
        if path:
            return path
        elif self.window.active_view().file_name():
            return re.sub(
                re.compile('{0}[^{0}]+$'.format(os.sep)),
                os.sep,
                self.window.active_view().file_name()
            )
        elif self.window.folders():
            return self.window.folders()[0]
        else:
            return None

    def check_tmux_status(self):
        tmux_status = subprocess.Popen(['tmux', 'info'])
        tmux_status.wait()

        return tmux_status.returncode is 0

    def get_active_tmux_sessions(self):
        sessions = subprocess.Popen(['tmux', 'list-sessions'], stdout=subprocess.PIPE)
        active_sessions = {}

        for line in io.TextIOWrapper(sessions.stdout, encoding='utf-8'):
            if line.endswith('(attached)' + os.linesep):
                active_sessions[line.split(':')[0]] = line.split(' (')[0]

        return active_sessions

    def run_tmux(self, path, parameters, split):
        try:
            if self.check_tmux_status():
                args = ['tmux', 'split-window' if split else 'new-window']

                if split == 'horizontal':
                    args.append('-h')

                if path:
                    args.extend(['-c', path])

                args.extend(parameters)
                subprocess.Popen(args)
        except (Exception) as exception:
            sublime.error_message('tmux: ' + str(exception))

class OpenTmuxCommand(sublime_plugin.WindowCommand, TmuxCommand):
    def run(self, path=None, split=None):
        path = self.resolve_file_path(path)

        self.run_tmux(path, [], split)

class OpenTmuxProjectFolderCommand(sublime_plugin.WindowCommand, TmuxCommand):
    def run(self, path=None, split=None):
        path = self.resolve_file_path(path)
        folders = [x for x in self.window.folders() if path.find(x + os.sep) == 0][0:1]
        path = folders[0]
        parameters=[]

        if get_setting('set_project_window_name', True):
            parameters.extend(['-n', path.split(os.sep)[-1]])

        self.run_tmux(path, parameters, split)
