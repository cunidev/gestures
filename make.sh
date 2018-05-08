if [ $(id -u) = 0 ]; then
   echo "Warning: This script shouldn't be run as root!"
fi

rm -rf build
cd gestures
zip -r ../Gestures.zip *
cd ..
mkdir build
echo '#!/usr/bin/env python3' | cat - Gestures.zip > build/gestures
rm Gestures.zip
chmod +x build/gestures
cp data/org.cunidev.gestures.desktop build/

