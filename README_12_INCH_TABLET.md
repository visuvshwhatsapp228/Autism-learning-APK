# Autism Student Learning – 12-inch Android Tablet Edition

Configured for a 12-inch Android tablet in landscape orientation. The interface uses scalable Kivy density-independent sizing (dp/sp), large touch controls and a wide central learning area. The layout also adapts to other landscape tablet resolutions.

## Layout
- Left: Play, Pass, Numbers, Capital A-Z, Small a-z, Symbols and Tamil.
- Centre: slow circular character orbit; tap a character to select it.
- Right: Animation On/Off, Voice On/Off, Teacher Settings and Export Report.
- A selected character remains visible until another character is tapped or Play/Pass is pressed.
- Optional Android text-to-speech via Plyer.
- Hardware keyboard support where available.
- CSV learning history saved in app-private storage.

## Build APK (Linux / Ubuntu / Windows WSL2)
Buildozer is best supported on Linux. On Windows, use WSL2 with Ubuntu.

1. Install WSL2 and Ubuntu.
2. Install dependencies:

```bash
sudo apt update
sudo apt install -y python3-pip python3-venv git zip unzip openjdk-17-jdk \
  build-essential autoconf libtool pkg-config zlib1g-dev libncurses-dev \
  cmake libffi-dev libssl-dev
```

3. In this project folder:

```bash
python3 -m venv .venv
source .venv/bin/activate
pip install --upgrade pip setuptools wheel
pip install buildozer cython
```

4. Compile:

```bash
buildozer android debug
```

5. The APK will be created in `bin/`. Transfer it to the tablet and install it. Android may require permission to install apps from the file manager.

## Tamil display and voice
Tamil glyph display depends on a Tamil-capable font. If glyphs appear as boxes, bundle a Tamil Unicode `.ttf` font and configure Kivy to use it. Tamil speech requires a Tamil voice/language pack installed in Android Text-to-Speech settings. Plyer uses the installed Android TTS service; it does not install missing voices.

## Notes
This is a source project, not a compiled APK. The report is saved in app-private storage in this starter version; a system Share/Save As picker can be added later. Begin with slow motion and voice off, and adjust sensory settings with the student's teacher or caregiver.
