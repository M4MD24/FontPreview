import os
import sys
import glob
import math
from PIL import Image, ImageDraw, ImageFont


def generate_high_resolution_font_preview(
        folder_path=None,
        font_files=None,
        output_file="font_preview.png",
        sample_text="العربية\n٠١٢٣٤٥٦٧٨٩\n0123456789\nEnglish",
        font_size=60,
        columns=3,
        dpi=300,
        background_color=(40, 40, 40),
        text_preview_color=(255, 255, 255),
        title_color=(150, 150, 150),
        grid_color=(70, 70, 70),
        padding=10,
        cell_width=600,
        cell_height=800
):
    # Collect fonts from folder if not provided directly
    if font_files is None:
        if folder_path is None:
            raise ValueError("You must provide either folder_path or font_files")
        font_extensions = ["*.ttf", "*.otf"]
        font_files = []
        for ext in font_extensions:
            font_files.extend(glob.glob(os.path.join(folder_path, ext)))
            font_files.extend(glob.glob(os.path.join(folder_path, ext.upper())))
        font_files = sorted(list(set(font_files)))

    if not font_files:
        print(f"❌ No fonts (.ttf, .otf) found in the specified path.")
        return

    print(f"✅ Found {len(font_files)} font(s). Generating preview...")

    # Calculate grid dimensions
    num_fonts = len(font_files)
    rows = math.ceil(num_fonts / columns)

    image_width = columns * cell_width + padding * 2
    image_height = rows * cell_height + padding * 2

    print(f"📐 Grid: {rows} rows × {columns} columns")

    image = Image.new("RGB", (image_width, image_height), background_color)
    draw = ImageDraw.Draw(image)

    # Render each font in its grid cell
    for idx, font_path in enumerate(font_files):
        row = idx // columns
        col = idx % columns
        x = padding + col * cell_width
        y = padding + row * cell_height
        font_name = os.path.basename(font_path)

        draw.rectangle([x, y, x + cell_width, y + cell_height], outline=grid_color, width=2)

        try:
            font = ImageFont.truetype(font_path, font_size)
            try:
                small_font = ImageFont.truetype(font_path, int(font_size * 0.4))
            except:
                small_font = ImageFont.load_default()

            draw.text((x + 15, y + 10), font_name, font=small_font, fill=title_color)
            text_y = y + int(cell_height * 0.45)
            draw.text((x + 15, text_y), sample_text, font=font, fill=text_preview_color)

        except Exception as e:
            print(f"⚠️  Error loading font: {font_path} - {e}")
            default_font = ImageFont.load_default()
            draw.text((x + 15, y + 15), f"Error: {font_name}", font=default_font, fill=(255, 0, 0))

    # Save the final image with high DPI
    try:
        image.save(output_file, dpi=(dpi, dpi), quality=100)
        print(f"🎉 Saved successfully to: {output_file}")
        print(f"📐 Dimensions: {image_width}×{image_height} pixels, {dpi} DPI")
    except Exception as e:
        print(f"❌ Failed to save image: {e}")


# Walk through subfolders and generate a preview image for each folder containing fonts
def generate_previews_for_subfolders(root_folder, output_dir=None, **kwargs):
    if output_dir is None:
        output_dir = root_folder
    os.makedirs(output_dir, exist_ok=True)

    for root, dirs, files in os.walk(root_folder):
        font_files = [os.path.join(root, f) for f in files if f.lower().endswith(('.ttf', '.otf'))]
        if font_files:
            folder_name = os.path.basename(root) or "root"
            output_file = os.path.join(output_dir, f"fonts_preview_{folder_name}.png")
            print(f"\n📁 Processing folder: {root} ({len(font_files)} fonts found)")
            generate_high_resolution_font_preview(
                font_files=font_files,
                output_file=output_file,
                **kwargs
            )


if __name__ == "__main__":
    # Parse CLI args: arg1 = root path, arg2 = optional output dir
    root_folder = None
    output_dir = None

    if len(sys.argv) > 1:
        root_folder = sys.argv[1]
        print(f"ℹ️  Using root path from argument: {root_folder}")
        if len(sys.argv) > 2:
            output_dir = os.path.abspath(sys.argv[2])
            print(f"ℹ️  Output directory: {output_dir}")
        else:
            print("ℹ️  No output directory specified. Images will be saved inside the root folder.")
    else:
        # Interactive mode with fallback to system default font directories
        root_folder = input("📁 Enter the full path to the root folder containing your font subfolders: ").strip()
        if not root_folder:
            import platform

            if platform.system() == "Windows":
                root_folder = "C:/Windows/Fonts"
            elif platform.system() == "Darwin":  # macOS
                root_folder = "/Library/Fonts"
            else:  # Linux
                root_folder = "/usr/share/fonts/truetype"
            print(f"ℹ️  Using default system path: {root_folder}")

        out = input("📁 (Optional) Folder to save output images (press Enter to use the root folder): ").strip()
        if out:
            output_dir = os.path.abspath(out)

    if not os.path.isdir(root_folder):
        print(f"❌ Folder does not exist: {root_folder}")
    else:
        generate_previews_for_subfolders(
            root_folder=root_folder,
            output_dir=output_dir
        )
