zip -r Gestures.zip src/*
echo '#!/usr/bin/env python' | cat - Gestures.zip > Gestures_0.1
chmod +x Gestures_0.1

