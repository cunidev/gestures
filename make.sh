rm -rf build
cd src
zip -r ../Gestures.zip *
cd ..
echo '#!/usr/bin/env python' | cat - Gestures.zip > Gestures_0.1
rm Gestures.zip
chmod +x Gestures_0.1
mkdir build
mv Gestures_0.1 build/
cp gestures.desktop build/
