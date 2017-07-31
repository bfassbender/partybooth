install_all_the_things() 
{
cores=$(nproc)

sudo apt-get update -q
sudo apt-get remove -y gphoto2 libgphoto2*
sudo apt-get purge gphoto2 -y
sudo apt-get install libpopt-dev -y
sudo apt-get install libltdl-dev -y
sudo apt-get install libusb-dev -y
sudo apt-get install libusb-1.0-0-dev -y

wget http://downloads.sourceforge.net/project/gphoto/libgphoto/2.5.3.1/libgphoto2-2.5.3.1.tar.gz
tar xzvf libgphoto2-2.5.3.1.tar.gz
cd libgphoto2-2.5.3.1
./configure
make -j "$cores"
sudo make install
cd ..
rm -rf libgphoto2-2.5.3.1*

wget http://downloads.sourceforge.net/project/gphoto/gphoto/2.5.3/gphoto2-2.5.3.tar.gz
tar xzvf gphoto2-2.5.3.tar.gz
cd gphoto2-2.5.3
./configure
make -j "$cores"
sudo make install
cd ..
rm -rf gphoto2-2.5.3*
}

install_all_the_things
