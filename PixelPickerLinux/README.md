# PixelPicker
PixelPicker is an image viewing application that retrieves pixel co-ordinates and RGB values.
These values can be used in automation for robots that make decisions based on pixel patterns.
This was built to assist those efforts.

The following packages are essential for the program to run:
python3-tk - Tkinter - Writing Tk applications with Python 3.x
python3-pil - Python Imaging Library (Python3)
python3-pil.imagetk - Python Imaging Library - ImageTk Module (Python3)

To create application shortcut icon for hotbar on linux:
sudo cp PixelPicker.destop /usr/share/applications/

To bind keystrokes to a shortcut:
1. Open Settings: Click on the Activities overview and type "Settings", then press Enter.

2. Navigate to Keyboard Shortcuts:
   - In the Settings menu, go to the Keyboard section.
   - Scroll down to find Custom Shortcuts (or Keyboard Shortcuts in some versions).

3. Add a New Shortcut:
   - Click on the + button (usually at the bottom).
   - In the Name field, enter a name for your shortcut (e.g., "Launch My Application").
   - In the Command field, enter the command to run your application, 
   which is the `Exec` field from your `.desktop` file (e.g., `/path/to/myapp`).

4. Assign the Shortcut:
   - After clicking Add, a box will appear asking you to press the keys you want 
   to use for the shortcut (e.g., Ctrl + Alt + P).
   - Press your desired key combination, and it will be bound to the command.

