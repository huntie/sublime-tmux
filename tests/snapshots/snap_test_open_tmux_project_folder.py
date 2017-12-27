# -*- coding: utf-8 -*-
# snapshottest: v1 - https://goo.gl/zC4yUc
from __future__ import unicode_literals

from snapshottest import Snapshot


snapshots = Snapshot()

snapshots['TestOpenTmuxProjectFolderCommand::test_run_current_file 1'] = (
    [
        'tmux',
        'new-window',
        '-n',
        'example-project',
        '-c',
        '/home/user/example-project'
    ]
)

snapshots['TestOpenTmuxProjectFolderCommand::test_run_secondary_folder 1'] = (
    [
        'tmux',
        'new-window',
        '-n',
        'secondary-folder',
        '-c',
        '/home/user/secondary-folder'
    ]
)

snapshots['TestOpenTmuxProjectFolderCommand::test_run_unsaved_file 1'] = (
    [
        'tmux',
        'new-window',
        '-n',
        'example-project',
        '-c',
        '/home/user/example-project'
    ]
)

snapshots['TestOpenTmuxProjectFolderCommand::test_run_window_name_unset 1'] = (
    [
        'tmux',
        'new-window',
        '-c',
        '/home/user/example-project'
    ]
)
