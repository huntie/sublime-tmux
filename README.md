# Sublime tmux

Commands to open [tmux](https://github.com/tmux/tmux#readme) windows at the current file or root project folder in [Sublime Text](https://www.sublimetext.com/).

## Installation

Soon to be available on [Package Control](https://packagecontrol.io/). Until then, place this repository in your `Packages/` directory.

## Usage

For now, *sublime-tmux* requires a your local tmux server to be running. In practice this means it will only run actions whilst you have an open tmux session in your terminal emulator.

Once installed, a number of tmux-related commands are available in the Command Palette, activated with *ctrl*+*shift*+*p*:

<img src="./screenshots/command-palette.png" width="555" alt="tmux commands in the Command Palette">

If you wish to run these commands from your own keybinding, edit the config file under **Preferences: Key Bindings**, where they can be set along with any arguments.

### Commands

#### `open_tmux`

Open a new tmux window at the directory of the current file.

#### `open_tmux_project_folder`

Open a new tmux window at the current root project directory.

### Arguments

These properties may be set as part of the `args` object for any command.

#### `split` (str)

If set, a new pane in the current window will be opened. The direction of the split can be set to either `"horizontal"` or `"vertical"` (default).

## Contributing

If you discover a problem or have a feature request, please create an issue or feel free to fork this repository and make improvements.
