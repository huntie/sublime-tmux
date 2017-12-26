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
            os_dirname_mock.return_value = '~/example-project/src'
            sublime.active_window().run_command('open_tmux')

        self.assertMatchSnapshot(self.subproc_popen_mock.call_args[0])

    def test_run_split_vertical(self):
        with mock.patch('os.path.dirname') as os_dirname_mock:
            os_dirname_mock.return_value = '~/example-project/src'
            sublime.active_window().run_command('open_tmux', { 'split': 'vertical' })

        self.assertMatchSnapshot(self.subproc_popen_mock.call_args[0])

    def test_run_split_horizontal(self):
        with mock.patch('os.path.dirname') as os_dirname_mock:
            os_dirname_mock.return_value = '~/example-project/src'
            sublime.active_window().run_command('open_tmux', { 'split': 'horizontal' })

        self.assertMatchSnapshot(self.subproc_popen_mock.call_args[0])
