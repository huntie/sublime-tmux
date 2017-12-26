import sublime
import io
from unittest import mock
import snapshottest

def mock_process_call(attrs):
    process_mock = mock.Mock()
    process_mock.configure_mock(**attrs)

    return process_mock

def mock_tmux_subproc_calls():
    # `tmux info`
    yield mock_process_call({'returncode': 0})

    # `tmux list-sessions`
    yield mock_process_call({
        'returncode': 0,
        'stdout': io.BufferedReader(io.BytesIO(b'0 1 1513966319 1 150 34\n'))
    })

    # Later commands
    while True:
        yield mock_process_call({'returncode': 0})

class TestOpenTmuxCommand(snapshottest.TestCase):
    def setUp(self):
        self.subproc_popen_mock = mock.patch('subprocess.Popen').start()
        self.subproc_popen_mock.side_effect = mock_tmux_subproc_calls()

    def tearDown(self):
        mock.patch.stopall()

    def test_run_current_file(self):
        with mock.patch('os.path.dirname') as os_dirname_mock:
            os_dirname_mock.return_value = '/home/user/example-project/src'
            sublime.active_window().run_command('open_tmux')

        self.assertMatchSnapshot(self.subproc_popen_mock.call_args[0])

    def test_run_with_paths_argument(self):
        sublime.active_window().run_command('open_tmux', {'paths': ['/home/user/example-project/tests/snapshots']})

        self.assertMatchSnapshot(self.subproc_popen_mock.call_args[0])

    def test_run_with_paths_argument_multiple(self):
        with mock.patch('os.path.isdir') as os_isdir_mock:
            os_isdir_mock.side_effect = [True, False]
            sublime.active_window().run_command('open_tmux', {'paths': [
                '/home/user/example-project/docs',
                '/home/user/example-project/tests/test.py'
            ]})

        self.assertEqual(self.subproc_popen_mock.call_count, 4)
        self.assertMatchSnapshot([args[0] for args in self.subproc_popen_mock.call_args_list[-2:]])

    def test_run_unsaved_file_inside_project(self):
        view = sublime.active_window().new_file()

        with mock.patch('sublime.Window.folders') as window_folders_mock:
            window_folders_mock.return_value = [
                '/home/user/example-project',
                '/home/user/secondary-folder'
            ]
            sublime.active_window().run_command('open_tmux')

        self.assertMatchSnapshot(self.subproc_popen_mock.call_args[0])
        view.window().run_command("close_file")

    def test_run_unsaved_file_outside_project(self):
        view = sublime.active_window().new_file()

        with mock.patch('sublime.Window.folders') as window_folders_mock:
            window_folders_mock.return_value = []

            with mock.patch('os.path.expanduser') as home_dir_mock:
                home_dir_mock.return_value = '/home/user'
                sublime.active_window().run_command('open_tmux')

        self.assertMatchSnapshot(self.subproc_popen_mock.call_args[0])
        view.window().run_command("close_file")

    def test_run_split_vertical(self):
        with mock.patch('os.path.dirname') as os_dirname_mock:
            os_dirname_mock.return_value = '/home/user/example-project/src'
            sublime.active_window().run_command('open_tmux', { 'split': 'vertical' })

        self.assertMatchSnapshot(self.subproc_popen_mock.call_args[0])

    def test_run_split_horizontal(self):
        with mock.patch('os.path.dirname') as os_dirname_mock:
            os_dirname_mock.return_value = '/home/user/example-project/src'
            sublime.active_window().run_command('open_tmux', { 'split': 'horizontal' })

        self.assertMatchSnapshot(self.subproc_popen_mock.call_args[0])

    @mock.patch('sublime.load_settings')
    def test_run_split_vertical_even(self, mock_load_settings):
        mock_load_settings.return_value = {'arrange_panes_on_split': 'even'}

        with mock.patch('os.path.dirname') as os_dirname_mock:
            os_dirname_mock.return_value = '/home/user/example-project/src'
            sublime.active_window().run_command('open_tmux', { 'split': 'vertical' })

        self.assertMatchSnapshot([args[0] for args in self.subproc_popen_mock.call_args_list[-2:]])

    @mock.patch('sublime.load_settings')
    def test_run_split_horizontal_even(self, mock_load_settings):
        mock_load_settings.return_value = {'arrange_panes_on_split': 'even'}

        with mock.patch('os.path.dirname') as os_dirname_mock:
            os_dirname_mock.return_value = '/home/user/example-project/src'
            sublime.active_window().run_command('open_tmux', { 'split': 'horizontal' })

        self.assertMatchSnapshot([args[0] for args in self.subproc_popen_mock.call_args_list[-2:]])

    @mock.patch('sublime.load_settings')
    def test_run_split_arrange_tiled(self, mock_load_settings):
        mock_load_settings.return_value = {'arrange_panes_on_split': 'tiled'}

        with mock.patch('os.path.dirname') as os_dirname_mock:
            os_dirname_mock.return_value = '/home/user/example-project/src'
            sublime.active_window().run_command('open_tmux', { 'split': 'vertical' })

        self.assertMatchSnapshot([args[0] for args in self.subproc_popen_mock.call_args_list[-2:]])
