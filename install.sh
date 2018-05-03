./make.sh

mkdir /opt/gestures
cp ./build/gestures /opt/gestures/
sed -e 's/\/usr\/bin/\/opt\/gestures/g' -i ./build/org.cunidev.gestures.desktop 
cp ./build/org.cunidev.gestures.desktop /usr/share/applications/
cp ./data/org.cunidev.gestures.svg /usr/share/icons/hicolor/scalable/apps
