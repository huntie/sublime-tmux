import sublime
from unittest import mock
import snapshottest

from helpers import mock_tmux_subproc_events

class TestOpenTmuxProjectFolderCommand(snapshottest.TestCase):
    def setUp(self):
        self.subproc_popen_mock = mock.patch('subprocess.Popen').start()
        self.subproc_popen_mock.side_effect = mock_tmux_subproc_events()

        self.window_folders_mock = mock.patch('sublime.Window.folders').start()
        self.window_folders_mock.return_value = [
            '/home/user/example-project',
            '/home/user/secondary-folder'
        ]

    def tearDown(self):
        mock.patch.stopall()

    def test_run_current_file(self):
        with mock.patch('sublime.View.file_name') as file_name_mock:
            file_name_mock.return_value = '/home/user/example-project/README.md'
            sublime.active_window().run_command('open_tmux_project_folder')

        self.assertMatchSnapshot(self.subproc_popen_mock.call_args[0])

    def test_run_secondary_folder(self):
        with mock.patch('sublime.View.file_name') as file_name_mock:
            file_name_mock.return_value = '/home/user/secondary-folder/src/main.py'
            sublime.active_window().run_command('open_tmux_project_folder')

        self.assertMatchSnapshot(self.subproc_popen_mock.call_args[0])

    def test_run_unsaved_file(self):
        view = sublime.active_window().new_file()
        sublime.active_window().run_command('open_tmux_project_folder')
        view.window().run_command('close_file')

        self.assertMatchSnapshot(self.subproc_popen_mock.call_args[0])

    @mock.patch('sublime.load_settings')
    def test_run_window_name_unset(self, mock_load_settings):
        mock_load_settings.return_value = {'set_project_window_name': False}
        self.test_run_current_file()
