import os
import sys
import glob
import math
from PIL import Image, ImageDraw, ImageFont

# ----------------------------------------------------------------------
# Check for RAQM (modern shaping) support
# ----------------------------------------------------------------------
RAQM_AVAILABLE = False
try:
    if hasattr(ImageFont, "LAYOUT_RAQM"):
        RAQM_AVAILABLE = True
except AttributeError:
    pass

# Optional BiDi fallback (used only if RAQM is not available)
try:
    from bidi.algorithm import get_display

    BIDI_AVAILABLE = True
except ImportError:
    BIDI_AVAILABLE = False
    print("⚠️  'python-bidi' not installed. Fallback will not work.")


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
        scale=4.0,
        title_vertical_offset=-80,
        preview_vertical_offset=-80,
        line_spacing=20,
        use_raqm=True
):
    """
    Generate a high-resolution grid preview of multiple fonts.

    - If use_raqm=True and RAQM is available, Arabic is shaped correctly.
    - Otherwise, it falls back to BiDi reordering (no reshaping) – no character loss,
      but Arabic letters will not be joined (isolated forms).
    """
    # Apply scaling
    actual_font_size = int(font_size * scale)
    actual_title_font_size = int(title_font_size * scale) if title_font_size else None
    actual_cell_width = int(cell_width * scale)
    actual_cell_height = int(cell_height * scale)
    actual_padding = int(padding * scale)
    actual_dpi = int(dpi * scale)
    actual_title_vertical_offset = int(title_vertical_offset * scale)
    actual_preview_vertical_offset = int(preview_vertical_offset * scale)
    actual_line_spacing = int((line_spacing if line_spacing is not None else 4) * scale)

    use_raqm_effective = RAQM_AVAILABLE and use_raqm
    print(f"🔍 Scale: {scale} | Font size: {actual_font_size}")
    print(f"   Cell: {actual_cell_width}x{actual_cell_height} | DPI: {actual_dpi}")
    print(f"   Using RAQM: {use_raqm_effective}")
    if not use_raqm_effective:
        print(f"   ⚠️  Fallback: BiDi reordering only (letters won't be joined)")

    # Collect fonts
    if font_files is None:
        if folder_path is None:
            raise ValueError("Provide either folder_path or font_files")
        font_files = []
        for ext in ["*.ttf", "*.otf"]:
            font_files.extend(glob.glob(os.path.join(folder_path, ext)))
            font_files.extend(glob.glob(os.path.join(folder_path, ext.upper())))
        font_files = sorted(set(font_files))

    if not font_files:
        print("❌ No fonts found.")
        return

    print(f"✅ Found {len(font_files)} fonts.")

    # Load title font
    title_font = None
    if title_font_path and os.path.isfile(title_font_path):
        try:
            title_font = ImageFont.truetype(title_font_path, actual_title_font_size or 30)
        except Exception:
            title_font = ImageFont.load_default()
    else:
        title_font = ImageFont.load_default()

    rows = math.ceil(len(font_files) / columns)
    image_width = columns * actual_cell_width + actual_padding * 2
    image_height = rows * actual_cell_height + actual_padding * 2
    print(f"📐 Grid: {rows}×{columns} | Image: {image_width}×{image_height}")

    image = Image.new("RGB", (image_width, image_height), background_color)
    draw = ImageDraw.Draw(image)

    sample_lines = sample_text.split('\n')

    # ---- Pre‑process for fallback (BiDi only, NO reshaping) ----
    if not use_raqm_effective and BIDI_AVAILABLE:
        fallback_lines = [get_display(line) for line in sample_lines]
    else:
        fallback_lines = sample_lines[:]  # fallback if no bidi

    for idx, font_path in enumerate(font_files):
        row = idx // columns
        col = idx % columns
        x = actual_padding + col * actual_cell_width
        y = actual_padding + row * actual_cell_height
        font_name = os.path.basename(font_path)

        # Cell border
        draw.rectangle([x, y, x + actual_cell_width, y + actual_cell_height],
                       outline=grid_color, width=max(2, int(2 * scale)))

        try:
            # Load font with or without RAQM
            if use_raqm_effective:
                font = ImageFont.truetype(font_path, actual_font_size,
                                          layout_engine=ImageFont.LAYOUT_RAQM)
            else:
                font = ImageFont.truetype(font_path, actual_font_size)

            # Name font
            try:
                if title_font_path and os.path.isfile(title_font_path):
                    name_font = ImageFont.truetype(title_font_path, actual_title_font_size or 30)
                else:
                    name_font = ImageFont.truetype(font_path, actual_title_font_size or 30)
            except:
                name_font = ImageFont.load_default()

            # Draw font name (centered)
            name_bbox = draw.textbbox((0, 0), font_name, font=name_font)
            name_cx = x + actual_cell_width / 2
            name_cy = y + actual_cell_height / 4 + actual_title_vertical_offset
            draw.text((name_cx, name_cy), font_name, font=name_font,
                      fill=title_color, anchor='mm')

            # Draw preview lines (centered)
            if sample_lines:
                # Choose the text to draw
                if use_raqm_effective:
                    texts = sample_lines
                else:
                    texts = fallback_lines

                line_heights = []
                for line in texts:
                    if use_raqm_effective:
                        bbox = draw.textbbox((0, 0), line, font=font, direction='rtl')
                    else:
                        bbox = draw.textbbox((0, 0), line, font=font)
                    line_heights.append(bbox[3] - bbox[1])

                total_height = sum(line_heights) + (len(texts) - 1) * actual_line_spacing
                target_center_y = y + 3 * actual_cell_height / 4 + actual_preview_vertical_offset
                y_start = target_center_y - total_height / 2

                current_y = y_start
                for i, line in enumerate(texts):
                    line_mid_y = current_y + line_heights[i] / 2
                    line_cx = x + actual_cell_width / 2

                    if use_raqm_effective:
                        draw.text((line_cx, line_mid_y), line, font=font,
                                  fill=text_preview_color, anchor='mm', direction='rtl')
                    else:
                        draw.text((line_cx, line_mid_y), line, font=font,
                                  fill=text_preview_color, anchor='mm')

                    current_y += line_heights[i] + actual_line_spacing

        except Exception as e:
            print(f"⚠️  Error with {font_path}: {e}")
            default_font = ImageFont.load_default()
            draw.text((x + 10, y + 10), f"Error: {font_name}",
                      font=default_font, fill=(255, 0, 0))

    # Save
    try:
        image.save(output_file, dpi=(actual_dpi, actual_dpi), quality=100)
        print(f"🎉 Saved: {output_file}")
    except Exception as e:
        print(f"❌ Save failed: {e}")


def generate_previews_for_subfolders(root_folder, output_dir=None, **kwargs):
    if output_dir is None:
        output_dir = root_folder
    os.makedirs(output_dir, exist_ok=True)

    for root, dirs, files in os.walk(root_folder):
        font_files = [os.path.join(root, f) for f in files if f.lower().endswith(('.ttf', '.otf'))]
        if font_files:
            folder_name = os.path.basename(root) or "root"
            output_file = os.path.join(output_dir, f"fonts_preview_{folder_name}.png")
            print(f"\n📁 Processing: {root} ({len(font_files)} fonts)")
            generate_high_resolution_font_preview(
                font_files=font_files,
                output_file=output_file,
                **kwargs
            )


if __name__ == "__main__":
    root_folder = None
    output_dir = None
    title_font_path = None

    if len(sys.argv) > 1:
        root_folder = sys.argv[1]
        if len(sys.argv) > 2:
            output_dir = os.path.abspath(sys.argv[2])
        if len(sys.argv) > 3:
            title_font_path = sys.argv[3]
    else:
        root_folder = input("📁 Enter fonts folder: ").strip()
        if not root_folder:
            import platform

            if platform.system() == "Windows":
                root_folder = "C:/Windows/Fonts"
            elif platform.system() == "Darwin":
                root_folder = "/Library/Fonts"
            else:
                root_folder = "/usr/share/fonts/truetype"
        out = input("📁 Output folder (Enter for same): ").strip()
        if out:
            output_dir = os.path.abspath(out)
        title_font = input("🖋️  Title font path (optional): ").strip()
        if title_font and os.path.isfile(title_font):
            title_font_path = title_font

    if not os.path.isdir(root_folder):
        print(f"❌ Folder not found: {root_folder}")
    else:
        generate_previews_for_subfolders(
            root_folder=root_folder,
            output_dir=output_dir,
            title_font_path=title_font_path,
            use_raqm=True
        )
