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
        columns=10,
        dpi=300,
        background_color=(40, 40, 40),
        text_preview_color=(255, 255, 255),
        title_color=(150, 150, 150),
        grid_color=(70, 70, 70),
        padding=20,
        cell_width=700,
        cell_height=500,
        title_font_path=None,
        title_font_size=30,
        gap_between_title_and_preview=80,
        scale=5.0
):
    # Apply scaling to all dimensional parameters
    actual_font_size = int(font_size * scale)
    actual_title_font_size = int(title_font_size * scale) if title_font_size else None
    actual_cell_width = int(cell_width * scale)
    actual_cell_height = int(cell_height * scale)
    actual_padding = int(padding * scale)
    actual_gap = int(gap_between_title_and_preview * scale)
    actual_dpi = int(dpi * scale)
    # Fixed offsets for the font name inside the cell (originally 15, 10)
    name_offset_x = int(15 * scale)
    name_offset_y = int(10 * scale)

    print(f"🔍 Scale factor: {scale}")
    print(f"   Effective font size: {actual_font_size}")
    print(f"   Effective cell size: {actual_cell_width}x{actual_cell_height}")
    print(f"   Effective DPI: {actual_dpi}")

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

    # Load the unified title font (if provided) – used only for name rendering
    title_font = None
    if title_font_path and os.path.isfile(title_font_path):
        try:
            title_font = ImageFont.truetype(title_font_path, actual_title_font_size or 30)
        except Exception as e:
            print(f"⚠️  Could not load title font: {e}. Using default.")
            title_font = ImageFont.load_default()
    else:
        title_font = ImageFont.load_default()

    # Calculate grid dimensions using scaled values
    num_fonts = len(font_files)
    rows = math.ceil(num_fonts / columns)

    image_width = columns * actual_cell_width + actual_padding * 2
    image_height = rows * actual_cell_height + actual_padding * 2

    print(f"📐 Grid: {rows} rows × {columns} columns")
    print(f"🔤 Name font size: {actual_title_font_size}")
    print(f"📏 Gap between title and preview text: {actual_gap} pixels")
    print(f"📏 Final image dimensions: {image_width}×{image_height} pixels")

    image = Image.new("RGB", (image_width, image_height), background_color)
    draw = ImageDraw.Draw(image)

    # Render each font in its grid cell
    for idx, font_path in enumerate(font_files):
        row = idx // columns
        col = idx % columns
        x = actual_padding + col * actual_cell_width
        y = actual_padding + row * actual_cell_height
        font_name = os.path.basename(font_path)

        # Draw cell border
        draw.rectangle([x, y, x + actual_cell_width, y + actual_cell_height],
                       outline=grid_color, width=max(2, int(2 * scale)))

        try:
            font = ImageFont.truetype(font_path, actual_font_size)

            # Render the font name using the unified font (or fallback)
            try:
                if title_font_path and os.path.isfile(title_font_path):
                    name_font = ImageFont.truetype(title_font_path, actual_title_font_size or 30)
                else:
                    name_font = ImageFont.truetype(font_path, actual_title_font_size or 30)
            except:
                name_font = ImageFont.load_default()

            draw.text((x + name_offset_x, y + name_offset_y),
                      font_name, font=name_font, fill=title_color)

            # Render the sample text.
            # Position is controlled by actual_gap from the top of the cell.
            text_y = y + actual_gap
            draw.text((x + name_offset_x, text_y),
                      sample_text, font=font, fill=text_preview_color)

        except Exception as e:
            print(f"⚠️  Error loading font: {font_path} - {e}")
            default_font = ImageFont.load_default()
            draw.text((x + name_offset_x, y + name_offset_y),
                      f"Error: {font_name}", font=default_font, fill=(255, 0, 0))

    # Save the final image with scaled DPI
    try:
        image.save(output_file, dpi=(actual_dpi, actual_dpi), quality=100)
        print(f"🎉 Saved successfully to: {output_file}")
        print(f"📐 Dimensions: {image_width}×{image_height} pixels, {actual_dpi} DPI")
    except Exception as e:
        print(f"❌ Failed to save image: {e}")


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
    # CLI Arguments:
    # argv[1] = root_folder (required)
    # argv[2] = output_dir (optional)
    # argv[3] = title_font_path (optional)
    root_folder = None
    output_dir = None
    title_font_path = None

    if len(sys.argv) > 1:
        root_folder = sys.argv[1]
        print(f"ℹ️  Using root path from argument: {root_folder}")
        if len(sys.argv) > 2:
            output_dir = os.path.abspath(sys.argv[2])
            print(f"ℹ️  Output directory: {output_dir}")
        if len(sys.argv) > 3:
            title_font_path = sys.argv[3]
            print(f"ℹ️  Title font path: {title_font_path}")
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

        title_font = input("🖋️  (Optional) Full path to a font file for displaying font names only (press Enter to skip): ").strip()
        if title_font and os.path.isfile(title_font):
            title_font_path = title_font
        else:
            title_font_path = None

    if not os.path.isdir(root_folder):
        print(f"❌ Folder does not exist: {root_folder}")
    else:
        generate_previews_for_subfolders(
            root_folder=root_folder,
            output_dir=output_dir,
            title_font_path=title_font_path
        )
