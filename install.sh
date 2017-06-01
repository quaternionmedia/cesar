
# 	cd /home/$USER
#
# 	# dotfiles
# 	git clone https://github.com/mathiasbynens/dotfiles.git
# 	cd dotfiles
# 	source bootstrap.sh

PACKAGES="sudo rsync git vim htop tree nginx wireshark nmap python-tk python3-tk g++ build-essential checkinstall libreadline-gplv2-dev libncursesw5-dev libssl-dev libsqlite3-dev tk-dev libgdbm-dev libc6-dev libbz2-dev libncurses5-dev zlib1g-dev"
for PACKAGE in $PACKAGES
do
	apt install -y $PACKAGE
done

# python install

wget https://www.python.org/ftp/python/3.6.1/Python-3.6.1.tgz
tar xvzf Python-3.6.1.tgz
cd Python-3.6.1
./configure --enable-optimizations
make
make altinstall
cd ..

PIPS="hug jinja2 pillow"
for PIP in $PIPS
do
	pip3.6 install $PIP
done
