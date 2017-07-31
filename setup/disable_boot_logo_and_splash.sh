sudo sed -i 's/rootwait/rootwait logo.nologo/g' /boot/cmdline.txt 
sudo sed -i 's/console\=tty1/console\=tty3/g' /boot/cmdline.txt
sudo cp ~/partybooth/splash.png /usr/share/plymouth/themes/pix/splash.png
sudo reboot
