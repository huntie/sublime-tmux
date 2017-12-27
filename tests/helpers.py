import io
from unittest import mock

def mock_process_call(attrs):
    process_mock = mock.Mock()
    process_mock.configure_mock(**attrs)

    return process_mock

def mock_tmux_subproc_events():
    # `tmux info`
    yield mock_process_call({'returncode': 0})

    # `tmux list-sessions`
    yield mock_process_call({
        'returncode': 0,
        'stdout': io.BufferedReader(io.BytesIO(b'0 1 1513966319 1 150 34\n'))
    })

    while True:
        yield mock_process_call({'returncode': 0})
