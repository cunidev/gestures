if [[ $EUID = 0 ]]; then
   echo "Warning: This script shouldn't be run as root!"
   echo
fi

rm -rf build
cd gestures
zip -r ../Gestures.zip *
cd ..
mkdir build
echo '#!/usr/bin/python3' | cat - Gestures.zip > build/gestures
rm Gestures.zip
chmod +x build/gestures
cp data/org.cunidev.gestures.desktop build/

