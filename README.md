# FontPreview

A Python tool for generating high-resolution font preview sheets from a folder of font files.

The program scans a folder or its subfolders, renders predefined Arabic and English preview texts using each font, and exports organized PNG images with every font displayed inside an equally sized frame.

Arabic text is rendered using Pillow's native complex-text layout support when available, with `libraqm` providing proper Arabic shaping and bidirectional text handling.

## Features

* Recursively scan a folder and its subfolders.
* Detect supported font files.
* Support `.ttf` and `.otf` font formats.
* Render Arabic text with proper Arabic shaping and text direction when RAQM is available.
* Render Arabic-Indic digits.
* Render English digits.
* Render English text.
* Display preview texts in a fixed order.
* Place every font inside an equally sized frame.
* Display the font name above each preview.
* Generate high-resolution PNG images.
* Configure the number of columns through the function API.
* Automatically adjust the effective number of columns when fewer fonts are available than requested.
* Configure frame width and height through the function API.
* Configure DPI through the function API.
* Configure padding and border width through the function API.
* Configure preview font sizes through the function API.
* Generate separate preview images for subfolders.
* Optionally generate a single preview image containing fonts from all subfolders.
* Preserve the folder-based organization of the generated previews.
* Support command-line folder input.
* Support an interactive terminal mode when no command-line arguments are provided.
* Support a custom font for displaying font names.
* Use Pillow for image generation and font rendering.
* Use `fontTools` for font inspection and font metadata.
* Use `libraqm` for native complex-text layout when available.
* Use `python-bidi` as fallback support for Arabic text rendering when native layout is unavailable.

## Requirements

* Python 3.11 or newer.
* Pillow.
* fontTools.
* python-bidi.
* Optional: `libraqm` for native complex-text layout and improved Arabic rendering.

## Recommended Environment

The recommended setup uses **Conda** to install Pillow together with `libraqm`.

```text
Python 3.14
├── pip 26.2.1
│   ├── Pillow 12.3.0
│   ├── fontTools 4.64.0
│   └── python-bidi 0.6.11
└── conda 26.7.1
    ├── libraqm 0.11.0
    └── Pillow 12.3.0
```

The versions above describe the recommended environment. Other compatible versions may also work.

## Installation

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
python -c "from PIL import features; print('Using RAQM:', features.check_feature('raqm'))"
```

Expected output:

```text
Using RAQM: True
```

If the output is `True`, Pillow can use `libraqm` for Arabic and other complex-text layout operations.

If the output is `False`, the program can still generate previews, but Arabic shaping and right-to-left layout may not work correctly.

## Usage

### Command-Line Mode

Run the program with a folder path:

```powershell
python FontPreview.py "C:\Users\user\Documents\Fonts"
```

The program recursively scans the specified folder and generates a separate preview image for each folder containing supported font files.

### Specify an Output Folder

The second argument specifies the output directory:

```powershell
python FontPreview.py "C:\Users\user\Documents\Fonts" "C:\Users\user\Documents\FontPreviews"
```

### Specify a Custom Title Font

The third argument specifies a font used to display the font names:

```powershell
python FontPreview.py "C:\Users\user\Documents\Fonts" "C:\Users\user\Documents\FontPreviews" "C:\Windows\Fonts\arial.ttf"
```

### Command-Line Arguments

```text
python FontPreview.py <root_folder> [output_dir] [title_font_path]
```

| Argument          | Description                                                                     |
|-------------------|---------------------------------------------------------------------------------|
| `root_folder`     | Source folder containing font files.                                            |
| `output_dir`      | Optional output directory. If omitted, previews are saved in the source folder. |
| `title_font_path` | Optional font used to display font names.                                       |

### Interactive Mode

If no command-line arguments are provided, the program prompts for the source folder, output folder, and optional title font:

```powershell
python FontPreview.py
```

If the source folder is left empty, the program uses a default system font directory:

* Windows: `C:/Windows/Fonts`
* macOS: `/Library/Fonts`
* Linux: `/usr/share/fonts/truetype`

## Preview Text

Each font is tested using the following texts in this exact order:

```text
اللغة العربية
٠١٢٣٤٥٦٧٨٩
0123456789
English Language
```

The Arabic text and Arabic-Indic digits are rendered using right-to-left layout when RAQM is available.

The English digits are included as a separate preview line, and the English text is rendered using left-to-right layout.

If native layout is unavailable, the program can use the additional Arabic shaping and bidirectional text libraries as fallback support.

## Output

The generated PNG files contain a structured preview sheet.

Each font is displayed in its own frame, with:

1. Font name.
2. Arabic text.
3. Arabic-Indic digits.
4. English digits.
5. English text.

Multiple fonts are arranged into equally sized columns and rows.

The program automatically adjusts the effective number of columns when the number of available fonts is smaller than the requested number of columns.

For example, if the requested number of columns is `10` but only `3` fonts are available, the preview uses `3` columns instead of `10`.

### Output Naming

Preview images are generated using the following naming format:

```text
fonts_preview_<folder_name>.png
```

For example:

```text
Fonts/
├── Arabic/
│   ├── Amiri.ttf
│   └── Cairo.ttf
└── English/
    ├── Arial.ttf
    └── Times New Roman.ttf
```

The generated previews will be:

```text
Fonts/
├── Arabic/
│   ├── Amiri.ttf
│   └── Cairo.ttf
├── English/
│   ├── Arial.ttf
│   └── Times New Roman.ttf
├── fonts_preview_Arabic.png
└── fonts_preview_English.png
```

The output directory can be changed using the second command-line argument.

## Combined Preview

The function API supports generating a single preview image containing all fonts from the source folder and its subfolders.

This mode is enabled by passing:

```python
combine_all = True
```

The combined preview is saved as:

```text
fonts_preview_all.png
```

This option is available through the Python function API.

## Configuration

The preview generation function supports the following parameters:

| Parameter                 | Description                          |
|---------------------------|--------------------------------------|
| `folder_path`             | Source folder containing font files. |
| `font_files`              | Optional list of font file paths.    |
| `output_file`             | Output PNG file path.                |
| `sample_text`             | Custom preview text list.            |
| `font_size`               | Preview font size.                   |
| `columns`                 | Requested number of columns.         |
| `dpi`                     | Output image DPI.                    |
| `background_color`        | Background color.                    |
| `text_preview_color`      | Preview text color.                  |
| `title_color`             | Font name color.                     |
| `grid_color`              | Frame border color.                  |
| `padding`                 | Outer image padding.                 |
| `cell_width`              | Width of each font frame.            |
| `cell_height`             | Height of each font frame.           |
| `title_font_path`         | Optional font used for font names.   |
| `title_font_size`         | Font name size.                      |
| `scale`                   | Resolution scaling factor.           |
| `title_vertical_offset`   | Vertical offset for font names.      |
| `preview_vertical_offset` | Vertical offset for preview text.    |
| `line_spacing`            | Spacing between preview lines.       |
| `use_raqm`                | Enable or disable RAQM layout.       |


## How It Works

1. Reads the source folder from the command line or interactive terminal.
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
14. Determines the effective number of columns based on the number of available fonts.
15. Creates an equally sized frame for each font.
16. Places the font name above the preview text.
17. Places the preview text inside the frame.
18. Arranges all font frames into rows and columns.
19. Generates the final high-resolution PNG image.
20. Saves the generated previews according to the folder structure.

## Notes

The quality of Arabic rendering depends on the capabilities of the installed Pillow build and its text-layout support.

When available, `libraqm` provides proper complex-text layout for Arabic and other scripts. Installing Pillow and `libraqm` together from `conda-forge` is the recommended setup for reliable Arabic rendering.

`python-bidi` is retained as fallback support for bidirectional text handling when native complex-text layout is unavailable.

The number of columns is automatically adjusted to match the number of available fonts when fewer fonts are found than requested.

The original font files are never modified by the preview generation process.

The current command-line interface does not provide interactive options for changing preview dimensions, colors, or other rendering settings. These settings can be configured through the Python function API.
