if ! [ $(id -u) = 0 ]; then
   echo "This script must be run as root!"
   exit -1
fi

INSTALL="/usr/local/bin"

if [ -z "$1" ]
then
      echo "Notice: Using default install path ($INSTALL)"
else
      INSTALL=$1
fi

cp ./build/gestures $INSTALL/gestures
sed -e 's|/usr/bin|'$INSTALL'|g' -i ./build/org.cunidev.gestures.desktop 
cp ./build/org.cunidev.gestures.desktop /usr/share/applications/
cp ./data/org.cunidev.gestures.svg /usr/share/icons/hicolor/scalable/apps

echo "Installed to $INSTALL/gestures!"
