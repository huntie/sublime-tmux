# Sublime tmux

Commands to open [tmux](https://github.com/tmux/tmux#readme) windows at the current file or root project folder in [Sublime Text](https://www.sublimetext.com/).

## Installation

Available as [tmux](https://packagecontrol.io/packages/tmux) on [Package Control](https://packagecontrol.io/) – install using the *Package Control: Install Package* command from the Command Palette. Alternatively, place this repository in your `Packages/` directory.

## Usage

For now, *Sublime tmux* requires a local tmux server to be running. In practice this means it will only run actions whilst you have an open tmux session in your terminal emulator.

Once installed, a number of tmux-related commands are available in the Command Palette, activated with *Ctrl*+*Shift*+*P*:

<img src="./screenshots/command-palette.png" width="555" alt="tmux commands in the Command Palette">

If you wish to run these commands from your own keybinding, edit the config file under **Preferences: Key Bindings**, where they can be set along with any arguments.

### Commands

#### `open_tmux`

Open a new tmux window at the directory of the current file.

#### `open_tmux_project_folder`

Open a new tmux window at the current root project directory.

### Command arguments

These properties may be set as part of the `args` object for any command.

| Property | Type | Default | Description |
| --- | --- | --- | --- |
| **`split`** | `string`  | `null` | If set, a new pane in the current window will be opened. The direction of the split can be set to either `"horizontal"` or `"vertical"` (default). |

### Package settings

Default, user-level and OS-specific settings files can be accessed under **Preferences > Package Settings > tmux**.

| Property | Type | Default | Description |
| --- | --- | --- | --- |
| **`arrange_panes_on_split`** | `bool\|string` | `false` | Set how the active window layout should be updated each time after opening a split pane. A value of `"even"` will evenly distribute all panes in the direction opened. `"tiled"` or `true` will distribute all panes as evenly as possible in both rows and columns. Leave `false` to take no action. |
| **`set_project_window_name`** | `bool`  | `true` | Set whether new windows created with `open_tmux_project_folder` should be created with their name set to that of the directory opened. This is useful to identify multiple window tabs across projects. |

## Contributing

If you discover a problem or have a feature request, please create an issue or feel free to fork this repository and make improvements.
