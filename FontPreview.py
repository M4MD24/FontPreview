import os
import sys
import glob
import math
from PIL import Image, ImageDraw, ImageFont, features


def detect_raqm_support():
    try:
        return features.check_feature("raqm")
    except Exception:
        return False


RAQM_AVAILABLE = detect_raqm_support()


def generate_high_resolution_font_preview(
        folder_path=None,
        font_files=None,
        output_file="font_preview.png",
        sample_text=None,
        font_size=60,
        columns=10,
        dpi=300,
        background_color=(40, 40, 40),
        text_preview_color=(255, 255, 255),
        title_color=(150, 150, 150),
        grid_color=(70, 70, 70),
        padding=20,
        cell_width=1000,
        cell_height=500,
        title_font_path=None,
        title_font_size=30,
        scale=4.0,
        title_vertical_offset=-80,
        preview_vertical_offset=-80,
        line_spacing=20,
        use_raqm=True
):
    if columns <= 0:
        raise ValueError("columns must be a positive integer")

    if sample_text is None:
        sample_text = [
            {
                "text": "اللغة العربية",
                "is_rtl": True
            },
            {
                "text": "٠١٢٣٤٥٦٧٨٩",
                "is_rtl": True
            },
            {
                "text": "0123456789",
                "is_rtl": True
            },
            {
                "text": "English Language",
                "is_rtl": False
            }
        ]

    for item in sample_text:
        if not isinstance(item, dict):
            raise TypeError(
                "Each sample_text item must be a dictionary with "
                "'text' and 'is_rtl' keys."
            )

        if "text" not in item:
            raise ValueError("Each sample_text item must contain 'text'.")

        if "is_rtl" not in item:
            raise ValueError("Each sample_text item must contain 'is_rtl'.")

        if not isinstance(item["text"], str):
            raise TypeError("'text' must be a string.")

        if not isinstance(item["is_rtl"], bool):
            raise TypeError("'is_rtl' must be a bool.")

    actual_font_size = int(font_size * scale)
    actual_title_font_size = (
        int(title_font_size * scale)
        if title_font_size
        else None
    )

    actual_cell_width = int(cell_width * scale)
    actual_cell_height = int(cell_height * scale)
    actual_padding = int(padding * scale)
    actual_dpi = int(dpi * scale)
    actual_title_vertical_offset = int(
        title_vertical_offset * scale
    )
    actual_preview_vertical_offset = int(
        preview_vertical_offset * scale
    )
    actual_line_spacing = int(
        (line_spacing if line_spacing is not None else 4) * scale
    )

    use_raqm_effective = bool(use_raqm and RAQM_AVAILABLE)

    print(f"Scale: {scale} | Font size: {actual_font_size}")
    print(
        f"Cell: {actual_cell_width}x{actual_cell_height} | "
        f"DPI: {actual_dpi}"
    )
    print(f"RAQM available: {RAQM_AVAILABLE}")
    print(f"Using RAQM: {use_raqm_effective}")

    if not use_raqm_effective:
        print(
            "Warning: RAQM is disabled or unavailable. "
            "Arabic shaping and RTL layout may not work correctly."
        )

    if font_files is None:
        if folder_path is None:
            raise ValueError(
                "Provide either folder_path or font_files."
            )

        font_files = []

        for ext in ("*.ttf", "*.otf"):
            font_files.extend(
                glob.glob(os.path.join(folder_path, ext))
            )
            font_files.extend(
                glob.glob(os.path.join(folder_path, ext.upper()))
            )

        seen = {}

        for font_file in font_files:
            key = os.path.normcase(
                os.path.abspath(font_file)
            )
            seen.setdefault(key, font_file)

        font_files = sorted(seen.values())

    if not font_files:
        print("No fonts found.")
        return

    print(f"Found {len(font_files)} fonts.")

    # Determine the effective number of columns:
    # if we have fewer fonts than the requested columns, use the exact count.
    effective_columns = min(columns, len(font_files))

    if title_font_path and os.path.isfile(title_font_path):
        try:
            title_font = ImageFont.truetype(
                title_font_path,
                actual_title_font_size or 30
            )
        except OSError as error:
            print(
                f"Warning: could not load title font "
                f"'{title_font_path}': {error}"
            )
            title_font = ImageFont.load_default()
    else:
        title_font = None

    rows = math.ceil(len(font_files) / effective_columns)

    image_width = (
            effective_columns * actual_cell_width
            + actual_padding * 2
    )

    image_height = (
            rows * actual_cell_height
            + actual_padding * 2
    )

    print(
        f"Grid: {rows}x{effective_columns} (requested columns: {columns}) | "
        f"Image: {image_width}x{image_height}"
    )

    image = Image.new(
        "RGB",
        (image_width, image_height),
        background_color
    )

    draw = ImageDraw.Draw(image)

    name_font_cache = {}

    for index, font_path in enumerate(font_files):
        row = index // effective_columns
        column = index % effective_columns

        x = (
                actual_padding
                + column * actual_cell_width
        )

        y = (
                actual_padding
                + row * actual_cell_height
        )

        font_name = os.path.basename(font_path)

        draw.rectangle(
            [
                x,
                y,
                x + actual_cell_width,
                y + actual_cell_height
            ],
            outline=grid_color,
            width=max(2, int(2 * scale))
        )

        try:
            if use_raqm_effective:
                font = ImageFont.truetype(
                    font_path,
                    actual_font_size,
                    layout_engine=ImageFont.Layout.RAQM
                )
            else:
                font = ImageFont.truetype(
                    font_path,
                    actual_font_size
                )

            if font_path in name_font_cache:
                name_font = name_font_cache[font_path]
            else:
                try:
                    if title_font_path and os.path.isfile(
                            title_font_path):
                        name_font = ImageFont.truetype(
                            title_font_path,
                            actual_title_font_size or 30
                        )
                    else:
                        name_font = ImageFont.truetype(
                            font_path,
                            actual_title_font_size or 30
                        )
                except OSError:
                    name_font = ImageFont.load_default()

                name_font_cache[font_path] = name_font

            name_center_x = (
                    x + actual_cell_width / 2
            )

            name_center_y = (
                    y
                    + actual_cell_height / 4
                    + actual_title_vertical_offset
            )

            draw.text(
                (
                    name_center_x,
                    name_center_y
                ),
                font_name,
                font=name_font,
                fill=title_color,
                anchor="mm"
            )

            if sample_text:
                line_heights = []

                for item in sample_text:
                    text = item["text"]
                    is_rtl = item["is_rtl"]

                    if use_raqm_effective:
                        direction = "rtl" if is_rtl else "ltr"

                        bbox = draw.textbbox(
                            (0, 0),
                            text,
                            font=font,
                            direction=direction
                        )
                    else:
                        bbox = draw.textbbox(
                            (0, 0),
                            text,
                            font=font
                        )

                    line_height = bbox[3] - bbox[1]
                    line_heights.append(line_height)

                total_height = (
                        sum(line_heights)
                        + (
                                len(sample_text) - 1
                        ) * actual_line_spacing
                )

                target_center_y = (
                        y
                        + 3 * actual_cell_height / 4
                        + actual_preview_vertical_offset
                )

                current_y = (
                        target_center_y
                        - total_height / 2
                )

                for idx, item in enumerate(sample_text):
                    text = item["text"]
                    is_rtl = item["is_rtl"]

                    line_height = line_heights[idx]

                    line_center_y = (
                            current_y
                            + line_height / 2
                    )

                    line_center_x = (
                            x
                            + actual_cell_width / 2
                    )

                    if use_raqm_effective:
                        direction = (
                            "rtl"
                            if is_rtl
                            else "ltr"
                        )

                        draw.text(
                            (
                                line_center_x,
                                line_center_y
                            ),
                            text,
                            font=font,
                            fill=text_preview_color,
                            anchor="mm",
                            direction=direction
                        )
                    else:
                        draw.text(
                            (
                                line_center_x,
                                line_center_y
                            ),
                            text,
                            font=font,
                            fill=text_preview_color,
                            anchor="mm"
                        )

                    current_y += (
                            line_height
                            + actual_line_spacing
                    )

        except Exception as error:
            print(
                f"Error rendering {font_path}: {error}"
            )

            default_font = ImageFont.load_default()

            draw.text(
                (
                    x + 10,
                    y + 10
                ),
                f"Error: {font_name}",
                font=default_font,
                fill=(255, 0, 0)
            )

    try:
        output_parent = os.path.dirname(
            os.path.abspath(output_file)
        )

        os.makedirs(
            output_parent,
            exist_ok=True
        )

        image.save(
            output_file,
            dpi=(actual_dpi, actual_dpi)
        )

        print(f"Saved: {output_file}")

    except Exception as error:
        print(f"Save failed: {error}")


def generate_previews_for_subfolders(
        root_folder,
        output_dir=None,
        **kwargs
):
    if output_dir is None:
        output_dir = root_folder

    os.makedirs(
        output_dir,
        exist_ok=True
    )

    for root, dirs, files in os.walk(root_folder):
        font_files = [
            os.path.join(root, file_name)
            for file_name in files
            if file_name.lower().endswith(
                (".ttf", ".otf")
            )
        ]

        if not font_files:
            continue

        folder_name = (
                os.path.basename(root)
                or "root"
        )

        output_file = os.path.join(
            output_dir,
            f"fonts_preview_{folder_name}.png"
        )

        print(
            f"\nProcessing: {root} "
            f"({len(font_files)} fonts)"
        )

        generate_high_resolution_font_preview(
            font_files=font_files,
            output_file=output_file,
            **kwargs
        )


def main():
    root_folder = None
    output_dir = None
    title_font_path = None

    if len(sys.argv) > 1:
        root_folder = sys.argv[1]

        if len(sys.argv) > 2:
            output_dir = os.path.abspath(
                sys.argv[2]
            )

        if len(sys.argv) > 3:
            title_font_path = sys.argv[3]

    else:
        root_folder = input(
            "Enter fonts folder: "
        ).strip()

        if not root_folder:
            if sys.platform == "win32":
                root_folder = "C:/Windows/Fonts"
            elif sys.platform == "darwin":
                root_folder = "/Library/Fonts"
            else:
                root_folder = "/usr/share/fonts/truetype"

        output = input(
            "Output folder (Enter for same): "
        ).strip()

        if output:
            output_dir = os.path.abspath(
                output
            )

        title_font = input(
            "Title font path (optional): "
        ).strip()

        if (
                title_font
                and os.path.isfile(title_font)
        ):
            title_font_path = title_font

    if not os.path.isdir(root_folder):
        print(
            f"Folder not found: {root_folder}"
        )
        return

    generate_previews_for_subfolders(
        root_folder=root_folder,
        output_dir=output_dir,
        title_font_path=title_font_path
    )


if __name__ == "__main__":
    main()
