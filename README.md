# Gestures (moved to GitLab)
A minimal Gtk+ GUI app for libinput-gestures
New link: https://gitlab.com/cunidev/gestures

Use:
- `./make.sh; sudo ./install.sh` to install in /usr/local/bin. An alternative path for the binary can be specified as parameter to `install.sh`


## Video demo:

<a href="http://www.youtube.com/watch?feature=player_embedded&v=MrOIEoyijXM
" target="_blank"><img src="http://img.youtube.com/vi/MrOIEoyijXM/0.jpg" 
alt="(click to open video)" width="480" height="360" border="10" /></a>

## Dependencies:
- Python 3 with `gi` module
- xdotool
- libinput-gestures
- libinput-tools

On Debian/Ubuntu, type:
`sudo apt install python3 xdotool python3-gi libinput-tools python-gobject`

To install libinput-gestures, follow the instructions on its official page: https://github.com/bulletmark/libinput-gestures
