cd
mkdir Code
cd Code

# install foundation stuff
sudo apt-get update
sudo apt-get upgrade
sudo apt-get install python-pip
sudo pip install --upgrade pip
sudo apt-get install python-setuptools python-dev build-essential automake autoconf libtool git

# install scipy stack
sudo apt-get install python-tk
sudo pip install --user numpy scipy matplotlib ipython jupyter pandas sympy nose

# install pyteomics and pymzml
sudo pip install lxml image pyteomics
sudo pip install pymzml==0.7.8

# install RDkit
sudo apt-get install python-rdkit librdkit1 rdkit-data

# install libspatialindex rtree
git clone https://github.com/libspatialindex/libspatialindex.git
cd libspatialindex/
./autogen.sh
./configure; make; make install
sudo apt-get install libspatialindex-dev
ldconfig
sudo pip install rtree
cd ..

# install qt4
sudo apt-get install  libglew-dev libcheese7 libcheese-gtk23 libclutter-gst-2.0-0 libcogl15 libclutter-gtk-1.0-0 libclutter-1.0-0

# install pyqt4
sudo apt-get install python-qt4 qt4-dev-tools python-qt4-dev pyqt4-dev-tools

# Install R + RStudio
sudo apt-key adv –keyserver keyserver.ubuntu.com –recv-keys E084DAB9

# Ubuntu 16.04: xenial
sudo add-apt-repository 'deb https://ftp.ussg.iu.edu/CRAN/bin/linux/ubuntu xenial/'
sudo apt-get update
sudo apt-get install r-base
sudo apt-get install r-base-dev

# Download and Install RStudio
sudo apt-get install gdebi-core
wget https://download1.rstudio.org/rstudio-1.0.44-amd64.deb
sudo gdebi rstudio-1.0.44-amd64.deb
rm rstudio-1.0.44-amd64.deb



