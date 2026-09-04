# FontPreview

A Python tool for generating high-resolution font preview sheets from a folder of font files.

The program recursively scans a folder and its subfolders, renders predefined Arabic and English preview texts using each font, and exports organized PNG images with every font displayed inside an equally sized frame.

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
* Use `arabic-reshaper` and `python-bidi` as fallback support for Arabic text rendering.

## Current Requirements

* Python 3.14
* Pillow
* fontTools
* arabic-reshaper
* python-bidi

## Usage

Run the program with a folder path:

```bash
python FontPreview.py "C:\Users\user\Documents\Fonts" "C:\Users\user\Documents\Fonts\Previews" "C:\Windows\Fonts\Arial.ttf"
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

### Preview Text

Each font is tested using the following texts in this exact order:

```text
اللغة العربية
٠١٢٣٤٥٦٧٨٩
0123456789
English Language
```

The Arabic text is rendered with Arabic shaping and bidirectional text handling to ensure that connected Arabic letters are displayed correctly.

### Output

The generated PNG files contain a structured preview sheet.

Each font is displayed in its own frame, with:

1. Arabic text.
2. Arabic-Indic digits.
3. English digits.
4. English text.
5. Font name.

Multiple fonts are arranged into equally sized columns and rows.

## How It Works

1. Reads the source folder from the command line or graphical interface.
2. Validates the selected directory.
3. Recursively searches for supported font files.
4. Detects and loads each font.
5. Reads font metadata when available.
6. Prepares the Arabic preview text.
7. Applies Arabic shaping when required.
8. Applies bidirectional text processing when required.
9. Renders the Arabic-Indic digits.
10. Renders the English digits.
11. Renders the English preview text.
12. Calculates the required dimensions for each font preview.
13. Creates an equally sized frame for each font.
14. Places the preview text inside the frame.
15. Displays the font name below the frame.
16. Arranges all font frames into rows and columns.
17. Generates the final high-resolution PNG image.
18. Saves the generated previews according to the folder structure.

## Notes

The quality of Arabic rendering depends on the capabilities of the installed Pillow build and its text-layout support.

When available, `libraqm` provides proper complex-text layout for Arabic and other scripts. The additional Arabic shaping libraries provide fallback handling when native complex-text layout is unavailable.

The original font files are never modified by the preview generation process.