#FunBox Photobooth

## Requirements
- [Python 2.7+](https://www.python.org/)
- [gphoto2](http://www.gphoto.org/)
- a [gphoto2 compatible camera](http://www.gphoto.org/proj/libgphoto2/support.php)
- [Pillow](https://python-pillow.org/) Python Image Library
- [Imagemagick](https://www.imagemagick.org)


## Setup
### Mac OS
- Install Homebrew
- brew install gphoto2
- brew install imagemagick
- brew install python
- brew install python-imaging


### Raspberry Pi
- sudo apt-get update && sudo apt-get upgrade
- sudo apt-get install gphoto2
- sudo apt-get install imagemagick
- sudo apt-get install python-imaging

## Tweaking Raspberry Pi Pixel
### Disable Tooltips
nano ~/.themes/PiX/gtk-2.0/gtkrc
add
gtk-enable-tooltips = 0


### Disable Screensaver & Mouse Pointer over Start Menu
```bash
nano .config/lxsession/LXDE-pi/autostart
```   
Comment out:

```bash
# @xscreensaver -no-splash
# @point-rpi
```
### Autostart PartyBooth
```bash
nano .config/lxsession/LXDE-pi/autostart
```   
add
```bash
@python <path_to_PartyBooth>/PartyBooth.py
```


### Disable Screen Blanking & Mouse Pointer
```bash
sudo nano /etc/lightdm/lightdm.conf
```
edit / add the following line in section [SeatDefaults]
```bash
[SeatDefaults]
xserver-command=X -s 0 -dpms -nocursor
```
