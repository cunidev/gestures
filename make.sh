if [[ $EUID = 0 ]]; then
   echo "Warning: This script shouldn't be run as root!"
   echo
fi

rm -rf build
cd src
zip -r ../Gestures.zip *
cd ..
echo '#!/usr/bin/env python' | cat - Gestures.zip > gestures
rm Gestures.zip
chmod +x gestures
mkdir build
mv gestures build/
cp data/org.cunidev.gestures.desktop build/

