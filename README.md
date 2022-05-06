# libmutter-fix

`libmutter-fix` is a script to download, modify, and recompile libmutter in order to apply a 'bandaid' for a bug where the XkbNewKeyboardNotify event causes the system to freeze for several milliseconds when writing input to /dev/uinput.

This happens when using multiple input devices, or in my case, when simulating input with a program *(eg. macros)*.

This bug is not existant in Wayland nor non-GNOME-based desktop managers (from what I hear).

This script is derived completely from a post **[here](https://gitlab.gnome.org/GNOME/gnome-shell/-/issues/1858#note_818548)** by **Osvald Lindholm** - so shoutouts to them for the initial steps.

Additional threads found during my research on this bug:

- <https://bugs.launchpad.net/ubuntu/+source/gnome-shell/+bug/1777708>
- <https://gitlab.gnome.org/GNOME/mutter/-/merge_requests/833>
- <https://gitlab.gnome.org/GNOME/mutter/-/issues/398>

*NOTE: The original fix was reverted because it apparently causes issues on some non-QWERTY keyboards. I cannot confirm or deny this, as it doesn't affect me.*

**WARNING: Use this at your own risk. I created it for my own purposes so I can keep an up-to-date version of libmutter. If the script fails or you wish to fix this issue yourself, just follow the steps listed in the initial link above.**

## Usage

Must be on a Debian-based distro using x11.

Run `python libmutter-fix.py`, let it run, then reboot.

## How do I know if it worked?

You can use `xdotool key q` as a quick way to see if you suffer from the lag. Your system should lock up for a noticable amount before posting the key.

Run this command again after applying the fix and rebooting, and there should be no more system freeze.

## Tested On
- Pop!_OS 21.xx
- Pop!_OS 22.04
