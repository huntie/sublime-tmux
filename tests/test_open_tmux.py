import sublime
import io
from unittest import mock
import snapshottest

def mock_process_call(attrs):
    mock_process = mock.Mock()
    mock_process.configure_mock(**attrs)

    return mock_process

class TestOpenTmuxCommand(snapshottest.TestCase):
    @mock.patch('subprocess.Popen')
    def test_run_current_file(self, mock_subproc_popen):
        mock_subproc_popen.side_effect = [
            mock_process_call({'returncode': 0}),
            mock_process_call({'returncode': 0, 'stdout': io.BufferedReader(io.BytesIO(b'0 1 1513966319 1 206 51\n'))}),
            mock_process_call({'returncode': 0})
        ]

        with mock.patch('os.path.dirname') as mock_os_dirname:
            mock_os_dirname.return_value = '~/example-project/src'
            sublime.active_window().run_command('open_tmux')

        self.assertMatchSnapshot(mock_subproc_popen.call_args[0])

    @mock.patch('subprocess.Popen')
    def test_run_split_vertical(self, mock_subproc_popen):
        mock_subproc_popen.side_effect = [
            mock_process_call({'returncode': 0}),
            mock_process_call({'returncode': 0, 'stdout': io.BufferedReader(io.BytesIO(b'0 1 1513966319 1 206 51\n'))}),
            mock_process_call({'returncode': 0})
        ]

        with mock.patch('os.path.dirname') as mock_os_dirname:
            mock_os_dirname.return_value = '~/example-project/src'
            sublime.active_window().run_command('open_tmux', { 'split': 'vertical' })

        self.assertMatchSnapshot(mock_subproc_popen.call_args[0])

    @mock.patch('subprocess.Popen')
    def test_run_split_horizontal(self, mock_subproc_popen):
        mock_subproc_popen.side_effect = [
            mock_process_call({'returncode': 0}),
            mock_process_call({'returncode': 0, 'stdout': io.BufferedReader(io.BytesIO(b'0 1 1513966319 1 206 51\n'))}),
            mock_process_call({'returncode': 0})
        ]

        with mock.patch('os.path.dirname') as mock_os_dirname:
            mock_os_dirname.return_value = '~/example-project/src'
            sublime.active_window().run_command('open_tmux', { 'split': 'horizontal' })

        self.assertMatchSnapshot(mock_subproc_popen.call_args[0])
