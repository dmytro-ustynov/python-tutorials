# Packaging Tkinter Applications into Executables

## The Challenge

You've built a beautiful Tkinter GUI application. But when you send it to users, they need:
1. Python installed
2. All dependencies installed
3. To run it from command line: `python my_app.py`

This is impractical for non-technical users who expect a double-click executable!

## The Solution: Application Bundlers

Application bundlers package your Python code, the Python interpreter, and all dependencies into a single executable file (or folder) that runs without Python installed.

## Available Tools

| Tool | Platforms | Ease of Use | Notes |
|------|-----------|-------------|-------|
| **PyInstaller** | Windows, Mac, Linux | Easy | Most popular, best documentation |
| **cx_Freeze** | Windows, Mac, Linux | Medium | Cross-platform, older |
| **py2app** | Mac only | Medium | Mac-specific, creates .app bundles |
| **py2exe** | Windows only | Medium | Windows-specific, older |
| **Nuitka** | Windows, Mac, Linux | Hard | Compiles to C++, fastest |
| **briefcase** | Windows, Mac, Linux, Mobile | Medium | From BeeWare project |

**Recommendation**: Start with **PyInstaller** - it's the most popular and well-documented.

## PyInstaller: Complete Guide

### Installation

```bash
# Create virtual environment (recommended)
python -m venv venv
source venv/bin/activate  # Windows: venv\Scripts\activate

# Install PyInstaller
pip install pyinstaller
```

### Basic Example: Simple Tkinter App

Let's create a simple app to package:

```python
# hello_gui.py
import tkinter as tk
from tkinter import messagebox

def say_hello():
    name = entry.get()
    if name:
        messagebox.showinfo("Greeting", f"Hello, {name}!")
    else:
        messagebox.showwarning("Warning", "Please enter your name!")

# Create main window
root = tk.Tk()
root.title("Hello App")
root.geometry("300x150")

# Create widgets
label = tk.Label(root, text="Enter your name:", font=("Arial", 12))
label.pack(pady=10)

entry = tk.Entry(root, width=20, font=("Arial", 12))
entry.pack(pady=5)

button = tk.Button(root, text="Say Hello", command=say_hello, font=("Arial", 12))
button.pack(pady=10)

# Run
root.mainloop()
```

### Creating an Executable

```bash
pyinstaller hello_gui.py
```

This creates:
```
project/
├── hello_gui.py          # Your source
├── hello_gui.spec        # PyInstaller configuration
├── build/                # Build artifacts (can delete)
│   └── hello_gui/
└── dist/                 # Output directory
    └── hello_gui/        # Executable folder
        ├── hello_gui     # Linux/Mac
        ├── hello_gui.exe # Windows
        └── ... (many supporting files)
```

Run it:
```bash
./dist/hello_gui/hello_gui  # Linux/Mac
dist\hello_gui\hello_gui.exe  # Windows
```

### One-File Executable

Instead of a folder with many files, create a single executable:

```bash
pyinstaller --onefile hello_gui.py
```

Output:
```
dist/
└── hello_gui     # Single executable file!
```

**Trade-off**:
- One-file: Easier to distribute, but slower startup (unpacks to temp folder)
- One-folder: Faster startup, but many files to distribute

### Adding an Icon

```bash
# Windows
pyinstaller --onefile --icon=app_icon.ico hello_gui.py

# Mac
pyinstaller --onefile --icon=app_icon.icns hello_gui.py

# Linux
pyinstaller --onefile --icon=app_icon.png hello_gui.py
```

Icon requirements:
- **Windows**: .ico file (256x256 recommended)
- **Mac**: .icns file
- **Linux**: .png file

Create .ico from .png using online tools or:
```bash
pip install pillow
python -c "from PIL import Image; Image.open('icon.png').save('icon.ico')"
```

### Windowed Mode (No Console)

By default, a console window appears behind your GUI. Hide it:

```bash
pyinstaller --onefile --windowed hello_gui.py
# or shorthand:
pyinstaller --onefile -w hello_gui.py
```

**Important**: In windowed mode, `print()` statements won't show anywhere. Use logging instead:

```python
import logging

logging.basicConfig(
    filename='app.log',
    level=logging.INFO,
    format='%(asctime)s - %(message)s'
)

logging.info("Application started")
```

### Complete Packaging Command

```bash
pyinstaller --onefile --windowed --icon=icon.ico --name="My App" hello_gui.py
```

Options:
- `--onefile`: Single executable
- `--windowed` or `-w`: No console window
- `--icon=icon.ico`: Custom icon
- `--name="My App"`: Executable name (with spaces)

## Advanced Example: Multi-File Application

Real applications have multiple files, images, and data files.

Project structure:
```
my_app/
├── main.py               # Entry point
├── gui/
│   ├── __init__.py
│   └── dialogs.py
├── utils/
│   ├── __init__.py
│   └── helpers.py
├── assets/
│   ├── logo.png
│   ├── icon.ico
│   └── config.json
└── requirements.txt
```

### Including Data Files

PyInstaller doesn't automatically include non-.py files. You must specify them:

```bash
pyinstaller --onefile --windowed \
    --add-data="assets/logo.png:assets" \
    --add-data="assets/config.json:assets" \
    --icon=assets/icon.ico \
    main.py
```

**Syntax**: `--add-data="source:destination"`
- **Windows**: Use `;` instead of `:` → `--add-data="assets/logo.png;assets"`

### Accessing Data Files in Code

When packaged, files are in different locations. Use this helper:

```python
import sys
import os

def resource_path(relative_path):
    """Get absolute path to resource, works for dev and for PyInstaller"""
    try:
        # PyInstaller creates a temp folder and stores path in _MEIPASS
        base_path = sys._MEIPASS
    except Exception:
        base_path = os.path.abspath(".")

    return os.path.join(base_path, relative_path)

# Usage
logo_path = resource_path("assets/logo.png")
image = tk.PhotoImage(file=logo_path)
```

### Complete Example with Assets

```python
# main.py
import tkinter as tk
from tkinter import ttk
import sys
import os
import json

def resource_path(relative_path):
    """Get absolute path to resource, works for dev and for PyInstaller"""
    try:
        base_path = sys._MEIPASS
    except Exception:
        base_path = os.path.abspath(".")
    return os.path.join(base_path, relative_path)

class Application(tk.Tk):
    def __init__(self):
        super().__init__()

        self.title("Professional App")
        self.geometry("400x300")

        # Load configuration
        config_path = resource_path("assets/config.json")
        with open(config_path, 'r') as f:
            self.config = json.load(f)

        # Load logo
        logo_path = resource_path("assets/logo.png")
        self.logo = tk.PhotoImage(file=logo_path)

        # Create UI
        self.create_widgets()

    def create_widgets(self):
        # Logo
        logo_label = tk.Label(self, image=self.logo)
        logo_label.pack(pady=10)

        # Title from config
        title_label = tk.Label(
            self,
            text=self.config['app_title'],
            font=("Arial", 16, "bold")
        )
        title_label.pack(pady=10)

        # Button
        button = ttk.Button(self, text="Click Me", command=self.on_click)
        button.pack(pady=10)

    def on_click(self):
        print("Button clicked!")

if __name__ == "__main__":
    app = Application()
    app.mainloop()
```

assets/config.json:
```json
{
  "app_title": "My Professional Application",
  "version": "1.0.0"
}
```

Package it:
```bash
pyinstaller --onefile --windowed \
    --add-data="assets/logo.png:assets" \
    --add-data="assets/config.json:assets" \
    --icon=assets/icon.ico \
    --name="MyApp" \
    main.py
```

## Using a .spec File

For complex builds, edit the generated .spec file instead of using command-line options:

```bash
# Generate .spec file without building
pyinstaller --onefile --windowed main.py --name="MyApp"
```

Edit MyApp.spec:
```python
# -*- mode: python ; coding: utf-8 -*-

block_cipher = None

a = Analysis(
    ['main.py'],
    pathex=[],
    binaries=[],
    datas=[
        ('assets/logo.png', 'assets'),
        ('assets/config.json', 'assets'),
        ('assets/icons/*.png', 'assets/icons'),  # Wildcard supported
    ],
    hiddenimports=[],
    hookspath=[],
    hooksconfig={},
    runtime_hooks=[],
    excludes=[],
    win_no_prefer_redirects=False,
    win_private_assemblies=False,
    cipher=block_cipher,
    noarchive=False,
)

pyz = PYZ(a.pure, a.zipped_data, cipher=block_cipher)

exe = EXE(
    pyz,
    a.scripts,
    a.binaries,
    a.zipfiles,
    a.datas,
    [],
    name='MyApp',
    debug=False,
    bootloader_ignore_signals=False,
    strip=False,
    upx=True,
    upx_exclude=[],
    runtime_tmpdir=None,
    console=False,  # Windowed mode
    disable_windowed_traceback=False,
    argv_emulation=False,
    target_arch=None,
    codesign_identity=None,
    entitlements_file=None,
    icon='assets/icon.ico',
)
```

Build from .spec:
```bash
pyinstaller MyApp.spec
```

## Common Issues and Solutions

### Issue 1: ModuleNotFoundError

```
ModuleNotFoundError: No module named 'PIL'
```

**Cause**: PyInstaller didn't detect a module (often dynamic imports).

**Solution**: Add hidden imports:
```bash
pyinstaller --hidden-import=PIL --onefile main.py
```

Or in .spec file:
```python
hiddenimports=['PIL', 'PIL._tkinter_finder'],
```

### Issue 2: "Failed to execute script"

**Cause**: Usually a crash during startup. Hard to debug in --windowed mode.

**Solution 1**: Build without --windowed to see error:
```bash
pyinstaller --onefile main.py
./dist/main  # See actual error
```

**Solution 2**: Add error logging:
```python
import sys
import traceback

try:
    # Your app code
    app = Application()
    app.mainloop()
except Exception as e:
    with open('crash_log.txt', 'w') as f:
        f.write(traceback.format_exc())
    raise
```

### Issue 3: Large Executable Size

PyInstaller bundles entire Python + all dependencies.

Typical sizes:
- Simple Tkinter app: 10-15 MB
- App with NumPy/Pandas: 100-200 MB
- App with TensorFlow: 500+ MB

**Solutions**:

1. **Use virtual environment** (install only needed packages):
```bash
python -m venv venv
source venv/bin/activate
pip install -r requirements.txt
pyinstaller main.py
```

2. **Exclude unused modules**:
```bash
pyinstaller --exclude-module=pytest --exclude-module=setuptools main.py
```

3. **Use UPX compression** (already enabled by default):
```bash
# Install UPX
# Ubuntu: sudo apt install upx
# Mac: brew install upx
# Windows: Download from https://upx.github.io/

pyinstaller --onefile --upx-dir=/path/to/upx main.py
```

4. **Analyze what's included**:
```bash
pyinstaller --onefile main.py
# Check build/main/warn-main.txt for included files
```

### Issue 4: Antivirus False Positives

Many antivirus programs flag PyInstaller executables as malware.

**Reasons**:
- Packer behavior looks suspicious
- Self-extracting archive pattern
- No code signing certificate

**Solutions**:

1. **Code signing** (Windows):
```bash
# Buy a code signing certificate ($50-300/year)
# Sign your executable
signtool sign /f certificate.pfx /p password /t http://timestamp.digicert.com MyApp.exe
```

2. **Submit to antivirus vendors**: Most have false-positive submission forms

3. **Use alternative bundler**: Nuitka has fewer false positives

4. **Inform users**: Include note that it's a false positive

### Issue 5: File Not Found for Assets

**Problem**:
```python
# This works in development:
image = tk.PhotoImage(file="assets/logo.png")
# But fails in packaged app!
```

**Solution**: Always use `resource_path()` helper (shown earlier).

## Platform-Specific Considerations

### Windows

**Creating installer**:
Use Inno Setup or NSIS to create a proper installer:

1. Build executable with PyInstaller
2. Create installer script:

```iss
; InnoSetup script
[Setup]
AppName=My Application
AppVersion=1.0
DefaultDirName={pf}\MyApp
DefaultGroupName=My Application
OutputDir=installer
OutputBaseFilename=MyApp-Setup

[Files]
Source: "dist\MyApp.exe"; DestDir: "{app}"

[Icons]
Name: "{group}\My Application"; Filename: "{app}\MyApp.exe"
Name: "{commondesktop}\My Application"; Filename: "{app}\MyApp.exe"
```

3. Compile with Inno Setup Compiler

### macOS

**Creating .app bundle**:

PyInstaller on Mac creates a .app bundle automatically:
```bash
pyinstaller --onefile --windowed --icon=icon.icns main.py
```

Output: `dist/main.app` (can be double-clicked)

**Creating DMG installer**:
```bash
# Install create-dmg
brew install create-dmg

# Create DMG
create-dmg \
    --volname "MyApp" \
    --window-size 600 400 \
    --icon-size 100 \
    --icon "MyApp.app" 200 200 \
    --app-drop-link 400 200 \
    "MyApp-1.0.dmg" \
    "dist/"
```

**Code signing** (required for distribution):
```bash
# Sign the app
codesign --force --deep --sign "Developer ID Application: Your Name" dist/MyApp.app

# Verify
codesign --verify --deep --strict --verbose=2 dist/MyApp.app
```

### Linux

**Creating .desktop file**:

MyApp.desktop:
```ini
[Desktop Entry]
Version=1.0
Type=Application
Name=My Application
Comment=Description of my app
Exec=/opt/myapp/MyApp
Icon=/opt/myapp/icon.png
Terminal=false
Categories=Utility;
```

Install:
```bash
sudo cp MyApp.desktop /usr/share/applications/
sudo chmod +x /usr/share/applications/MyApp.desktop
```

**Creating DEB package**:
```
myapp_1.0/
├── DEBIAN/
│   └── control
└── opt/
    └── myapp/
        ├── MyApp
        └── icon.png
```

DEBIAN/control:
```
Package: myapp
Version: 1.0
Section: utils
Priority: optional
Architecture: amd64
Maintainer: Your Name <email@example.com>
Description: My Application
 A simple Tkinter application
```

Build:
```bash
dpkg-deb --build myapp_1.0
```

## Best Practices

### 1. Test on Target Platform

Always build and test on the same OS where users will run it:
- Build Windows .exe on Windows
- Build Mac .app on macOS
- Build Linux binary on Linux

Cross-compilation rarely works reliably.

### 2. Use Virtual Environment

```bash
# Clean environment
python -m venv build_env
source build_env/bin/activate
pip install -r requirements.txt
pip install pyinstaller
pyinstaller main.py
```

This ensures only necessary dependencies are included.

### 3. Version Your Builds

In your code:
```python
__version__ = "1.0.0"
```

In executable name:
```bash
pyinstaller --name="MyApp-v1.0.0" main.py
```

### 4. Include Error Handling

```python
import sys
import traceback
from tkinter import messagebox

def handle_exception(exc_type, exc_value, exc_traceback):
    """Global exception handler"""
    if issubclass(exc_type, KeyboardInterrupt):
        sys.__excepthook__(exc_type, exc_value, exc_traceback)
        return

    error_msg = "".join(traceback.format_exception(exc_type, exc_value, exc_traceback))

    # Log to file
    with open("error_log.txt", "a") as f:
        f.write(f"\n{'='*50}\n")
        f.write(error_msg)

    # Show to user
    messagebox.showerror(
        "Application Error",
        "An error occurred. Check error_log.txt for details."
    )

# Set global exception handler
sys.excepthook = handle_exception
```

### 5. Automated Build Script

build.py:
```python
import os
import shutil
import PyInstaller.__main__

# Clean previous build
if os.path.exists('build'):
    shutil.rmtree('build')
if os.path.exists('dist'):
    shutil.rmtree('dist')

# Build
PyInstaller.__main__.run([
    'main.py',
    '--onefile',
    '--windowed',
    '--icon=assets/icon.ico',
    '--name=MyApp',
    '--add-data=assets/logo.png:assets',
    '--add-data=assets/config.json:assets',
])

print("Build complete! Executable: dist/MyApp")
```

Run:
```bash
python build.py
```

### 6. Include README

In dist folder:
```
dist/
├── MyApp.exe
├── README.txt
└── LICENSE.txt
```

README.txt:
```
My Application v1.0.0

To run: Double-click MyApp.exe

System Requirements:
- Windows 10 or later
- No Python installation needed!

For support: email@example.com
```

## Alternative: Nuitka

For better performance and smaller size:

```bash
pip install nuitka

# Basic build
python -m nuitka --onefile --windows-disable-console main.py

# With icon
python -m nuitka --onefile --windows-disable-console --windows-icon-from-ico=icon.ico main.py

# Full optimization
python -m nuitka --onefile --standalone --windows-disable-console \
    --enable-plugin=tk-inter \
    --windows-icon-from-ico=icon.ico \
    main.py
```

Pros:
- Faster execution (compiled to C)
- Smaller executable
- Fewer antivirus false positives

Cons:
- Longer build time
- More complex setup
- Less documentation than PyInstaller

## Conclusion

Packaging Tkinter applications:

1. **Use PyInstaller** for simplicity
2. **Always test** on target platform
3. **Use `resource_path()` helper** for assets
4. **Build in clean virtual environment**
5. **Handle errors gracefully**
6. **Consider code signing** for professional distribution

**Complete workflow**:
```bash
# 1. Create virtual environment
python -m venv build_env
source build_env/bin/activate

# 2. Install dependencies
pip install -r requirements.txt
pip install pyinstaller

# 3. Build
pyinstaller --onefile --windowed --icon=icon.ico \
    --add-data="assets:assets" \
    --name="MyApp" \
    main.py

# 4. Test
./dist/MyApp

# 5. Distribute
zip -r MyApp-v1.0-windows.zip dist/MyApp.exe README.txt LICENSE.txt
```

Your users can now run your Python application without installing Python!