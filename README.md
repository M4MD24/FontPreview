# FontPreview

A Python tool for generating high-resolution font preview sheets from a folder of font files.

The program recursively scans a folder and its subfolders, renders predefined Arabic and English preview texts using each font, and exports organized PNG images with every font displayed inside an equally sized frame.

Arabic text is rendered using Pillow's native complex-text layout support when available, with `libraqm` providing proper Arabic shaping and bidirectional text handling.

## Features

* Recursively scan a folder and all subfolders.
* Detect supported font files.
* Support `.ttf` and `.otf` font formats.
* Render Arabic text with proper Arabic shaping and text direction.
* Render Arabic-Indic digits.
* Render English digits.
* Render English text.
* Display preview texts in a fixed order.
* Place every font inside an equally sized frame.
* Display the font name below each preview frame.
* Generate high-resolution PNG images.
* Configure the number of columns.
* Configure frame width and height.
* Configure DPI.
* Configure padding and border width.
* Configure preview font sizes.
* Generate separate preview images for subfolders.
* Preserve the folder-based organization of the generated previews.
* Provide a graphical interface for selecting folders and configuring export settings.
* Support command-line folder input.
* Use Pillow for image generation and font rendering.
* Use `fontTools` for font inspection.
* Use `libraqm` for native complex-text layout when available.
* Use `python-bidi` as fallback support for Arabic text rendering when native layout is unavailable.

## Requirements

The recommended setup uses **Conda** to install Pillow together with `libraqm`.

### Recommended Environment

* Python 3.11
* Conda
* Pillow
* `libraqm`
* `fontTools`
* `python-bidi`

### Install Miniconda

Download and install **Miniconda for Windows 64-bit**.

After installation, open a new PowerShell window and verify that Conda is available:

```powershell
conda --version
```

### Create the Conda Environment

Create a dedicated environment for FontPreview:

```powershell
conda create -n fontpreview python=3.11 -c conda-forge
```

Activate the environment:

```powershell
conda activate fontpreview
```

### Install Pillow with libraqm

Install Pillow and `libraqm` together from `conda-forge`:

```powershell
conda install -c conda-forge pillow libraqm -y
```

This provides a Pillow installation with native complex-text layout support through `libraqm`.

### Install the Remaining Dependencies

Install the remaining Python packages:

```powershell
pip install fontTools python-bidi
```

### Verify Arabic Text Layout Support

Run the following command inside the activated Conda environment:

```powershell
python -c "from PIL import features; print('Using RAQM:', features.check('raqm'))"
```

The expected output is:

```text
Using RAQM: True
```

If the output is `True`, Pillow can use `libraqm` for Arabic and other complex-text layout operations.

## Usage

Run the program with a folder path:

```powershell
python FontPreview.py "C:\Users\user\Documents\Fonts"
```

The program recursively scans the specified folder and processes supported font files found inside it.

### Graphical Interface

The program can also be used through its graphical interface to select:

* Source folder
* Number of columns
* Frame width
* Frame height
* DPI
* Padding
* Border width
* Preview font sizes
* Output location

## Preview Text

Each font is tested using the following texts in this exact order:

```text
اللغة العربية الفصحى
٠١٢٣٤٥٦٧٨٩
0123456789
United States English
```

The Arabic text is rendered using native complex-text layout when available. This allows Arabic letters to connect correctly and appear in their proper positions.

If native layout is unavailable, the program can use the additional Arabic shaping and bidirectional text libraries as fallback support.

## Output

The generated PNG files contain a structured preview sheet.

Each font is displayed in its own frame, with:

1. Arabic text.
2. Arabic-Indic digits.
3. English digits.
4. English text.
5. Font name.

Multiple fonts are arranged into equally sized columns and rows.

Preview images are generated according to the selected folder structure, allowing fonts from different subfolders to be organized separately.

## How It Works

1. Reads the source folder from the command line or graphical interface.
2. Validates the selected directory.
3. Recursively searches for supported font files.
4. Detects and loads each font.
5. Reads font metadata when available.
6. Checks whether Pillow supports native complex-text layout.
7. Prepares the Arabic preview text.
8. Renders Arabic text using native layout when available.
9. Uses fallback Arabic shaping and bidirectional text processing when required.
10. Renders the Arabic-Indic digits.
11. Renders the English digits.
12. Renders the English preview text.
13. Calculates the required dimensions for each font preview.
14. Creates an equally sized frame for each font.
15. Places the preview text inside the frame.
16. Displays the font name below the frame.
17. Arranges all font frames into rows and columns.
18. Generates the final high-resolution PNG image.
19. Saves the generated previews according to the folder structure.

## Notes

The quality of Arabic rendering depends on the capabilities of the installed Pillow build and its text-layout support.

When available, `libraqm` provides proper complex-text layout for Arabic and other scripts. Installing Pillow and `libraqm` together from `conda-forge` is the recommended setup for reliable Arabic rendering.

`python-bidi` is retained as fallback support for bidirectional text handling when native complex-text layout is unavailable.

The original font files are never modified by the preview generation process.
