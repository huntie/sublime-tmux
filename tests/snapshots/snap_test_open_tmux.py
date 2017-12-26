# -*- coding: utf-8 -*-
# snapshottest: v1 - https://goo.gl/zC4yUc
from __future__ import unicode_literals

from snapshottest import Snapshot


snapshots = Snapshot()

snapshots['TestOpenTmuxCommand::test_run_current_file 1'] = (
    [
        'tmux',
        'new-window',
        '-c',
        '/home/user/example-project/src'
    ]
)

snapshots['TestOpenTmuxCommand::test_run_split_arrange_tiled 1'] = [
    (
        [
            'tmux',
            'split-window',
            '-c',
            '/home/user/example-project/src'
        ]
    ),
    (
        [
            'tmux',
            'select-layout',
            'tiled'
        ]
    )
]

snapshots['TestOpenTmuxCommand::test_run_split_horizontal 1'] = (
    [
        'tmux',
        'split-window',
        '-h',
        '-c',
        '/home/user/example-project/src'
    ]
)

snapshots['TestOpenTmuxCommand::test_run_split_horizontal_even 1'] = [
    (
        [
            'tmux',
            'split-window',
            '-h',
            '-c',
            '/home/user/example-project/src'
        ]
    ),
    (
        [
            'tmux',
            'select-layout',
            'even-horizontal'
        ]
    )
]

snapshots['TestOpenTmuxCommand::test_run_split_vertical 1'] = (
    [
        'tmux',
        'split-window',
        '-c',
        '/home/user/example-project/src'
    ]
)

snapshots['TestOpenTmuxCommand::test_run_split_vertical_even 1'] = [
    (
        [
            'tmux',
            'split-window',
            '-c',
            '/home/user/example-project/src'
        ]
    ),
    (
        [
            'tmux',
            'select-layout',
            'even-vertical'
        ]
    )
]

snapshots['TestOpenTmuxCommand::test_run_unsaved_file_inside_project 1'] = (
    [
        'tmux',
        'new-window',
        '-c',
        '/home/user/example-project'
    ]
)

snapshots['TestOpenTmuxCommand::test_run_unsaved_file_outside_project 1'] = (
    [
        'tmux',
        'new-window',
        '-c',
        '/home/user'
    ]
)

snapshots['TestOpenTmuxCommand::test_run_with_paths_argument 1'] = (
    [
        'tmux',
        'new-window',
        '-c',
        '/home/user/example-project/tests'
    ]
)

snapshots['TestOpenTmuxCommand::test_run_with_paths_argument_multiple 1'] = [
    (
        [
            'tmux',
            'new-window',
            '-c',
            '/home/user/example-project/docs'
        ]
    ),
    (
        [
            'tmux',
            'new-window',
            '-c',
            '/home/user/example-project/tests'
        ]
    )
]
