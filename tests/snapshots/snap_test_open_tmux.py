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
        '~/example-project/src'
    ]
)

snapshots['TestOpenTmuxCommand::test_run_split_horizontal 1'] = (
    [
        'tmux',
        'split-window',
        '-h',
        '-c',
        '~/example-project/src'
    ]
)

snapshots['TestOpenTmuxCommand::test_run_split_vertical 1'] = (
    [
        'tmux',
        'split-window',
        '-c',
        '~/example-project/src'
    ]
)

snapshots['TestOpenTmuxCommand::test_run_with_paths_argument 1'] = (
    [
        'tmux',
        'new-window',
        '-c',
        '~/example-project/tests'
    ]
)

snapshots['TestOpenTmuxCommand::test_run_with_paths_argument_multiple 1'] = [
    (
        [
            'tmux',
            'new-window',
            '-c',
            '~/example-project/docs'
        ]
    ),
    (
        [
            'tmux',
            'new-window',
            '-c',
            '~/example-project/tests'
        ]
    )
]
