import os
import glob
import math
from PIL import Image, ImageDraw, ImageFont


def generate_high_resolution_font_preview(
        folder_path,
        output_file="fonts_preview_hd.png",
        sample_text="مرحباً Hello World 123",
        font_size=72,
        columns=4,
        dpi=300,
        background_color=(40, 40, 40),
        text_preview_color=(255, 255, 255),
        title_color=(150, 150, 150),
        padding=50,
        cell_width=2000,
        cell_height=2000
):
    # 1. Collect all font files (.ttf and .otf) from the folder
    font_extensions = ["*.ttf", "*.otf"]
    font_files = []
    for extension in font_extensions:
        font_files.extend(glob.glob(os.path.join(folder_path, extension)))
        font_files.extend(glob.glob(os.path.join(folder_path, extension.upper())))

    font_files = sorted(list(set(font_files)))

    if not font_files:
        print(f"❌ No fonts (.ttf, .otf) found in folder: {folder_path}")
        return

    print(f"✅ Found {len(font_files)} font(s). Generating preview...")

    # 2. Calculate grid layout
    num_fonts = len(font_files)
    rows = math.ceil(num_fonts / columns)

    image_width = columns * cell_width + padding * 2
    image_height = rows * cell_height + padding * 2

    # 3. Create the blank canvas
    image = Image.new("RGB", (image_width, image_height), background_color)
    draw = ImageDraw.Draw(image)

    # 4. Render each font in its grid cell
    for idx, font_path in enumerate(font_files):
        row = idx // columns
        col = idx % columns

        # Calculate the top-left corner of the current cell
        x = padding + col * cell_width
        y = padding + row * cell_height

        # Get the font file name
        font_name = os.path.basename(font_path)

        try:
            # Load the main font
            font = ImageFont.truetype(font_path, font_size)

            # Load a smaller version for the filename label
            try:
                small_font = ImageFont.truetype(font_path, int(font_size * 0.5))
            except:
                small_font = ImageFont.load_default()

            # Draw the filename at the top of the cell
            draw.text((x + 10, y + 5), font_name, font=small_font, fill=title_color)

            # Draw the sample text in the middle of the cell
            text_y = y + int(cell_height * 0.35)
            draw.text((x + 10, text_y), sample_text, font=font, fill=text_preview_color)

        except Exception as e:
            print(f"⚠️  Error loading font: {font_path} - {e}")
            default_font = ImageFont.load_default()
            draw.text((x + 10, y + 10), f"Error: {font_name}", font=default_font, fill=(255, 0, 0))

    # 5. Save the image with high DPI
    try:
        image.save(output_file, dpi=(dpi, dpi), quality=100)
        print(f"🎉 High-resolution image saved successfully to: {output_file}")
        print(f"📐 Dimensions: {image_width}×{image_height} pixels, {dpi} DPI")
        image.show()  # Optional: display the image
    except Exception as e:
        print(f"❌ Failed to save image: {e}")


if __name__ == "__main__":
    folder = input("📁 Please enter the full path to the folder containing your fonts: ").strip()

    # If the user leaves it blank, use a system default font folder
    if not folder:
        import platform

        if platform.system() == "Windows":
            folder = "C:/Windows/Fonts"
        elif platform.system() == "Darwin":  # macOS
            folder = "/Library/Fonts"
        else:  # Linux
            folder = "/usr/share/fonts/truetype"
        print(f"ℹ️  Using default system path: {folder}")

    if not os.path.isdir(folder):
        print(f"❌ Folder does not exist: {folder}")
    else:
        generate_high_resolution_font_preview(
            folder_path=folder,
            output_file="my_hd_fonts_preview.png",
            sample_text="العربية English 123",
            font_size=80,
            columns=3,
            dpi=300,
            cell_width=1400,
            cell_height=200
        )
