import csv
import logging
from pathlib import Path

from PIL import Image, ImageDraw, ImageFont


logging.basicConfig(filename='log.txt', level=logging.INFO)


def generate_images(csv_file):
    user_info_list = read_user_info_from_csv(csv_file)
    for user_info in user_info_list:
        add_text_to_image(user_info)


def read_user_info_from_csv(csv_file):
    user_info_list = []
    with open(csv_file, newline="", encoding="utf-8") as csvfile:
        reader = csv.reader(csvfile)
        next(reader)  # Skip header if exists
        for row in reader:
            user_info_list.append(tuple(row))
    return user_info_list


def add_text_to_image(user_info, output_folder="badge"):
    username, club_info, division_info, option_info, remark, option = user_info

    option_A = 'one day ticket without meal'
    option_B = 'one day ticket with meal'
    option_C = 'two day ticket with meal'
    option = option.strip().replace("'", "")
    print(f"Option value: {option}, type: {type(option)}")

    if not option:
        logging.info(f"Skipping row for user {username} due to empty option")
        return

    if option == option_A:
        image_path = 'optionA.jpg'
    elif option == option_B:
        image_path = 'optionB.jpg'
    elif option == option_C:
        image_path = 'optionC.jpg'
    else:
        raise ValueError(f"Invalid option: {option}")

    image = Image.open(image_path)

    image_width, image_height = image.size
    print(f"Image size: {image_width} x {image_height}")

    draw = ImageDraw.Draw(image)

    font_path = "/System/Library/Fonts/Supplemental/Arial Unicode.ttf"
    font_size = 20
    font = ImageFont.truetype(font_path, font_size)

    text_positions = [
        (420, username),
        (450, club_info),
        (500, division_info),
        (550, option_info),
        (600, remark),
        (100, '100'),
        (200, '200'),
        (300, '300'),
        (400, '400'),
        (500, '500'),
        (600, '600'),
        (700, '700'),
        (800, '800'),
        (900, '900'),
        (1000, '1000'),
        (1100, '1100'),
        (1174, '1174')
    ]

    # # Add text to image
    for y, text in text_positions:
        text_width, text_height = [1, 1]
        x = (image_width - text_width) / 2
        draw.text((x, y - text_height / 2), text, font=font, fill=(0, 0, 0), anchor="mm")
        output_folder_path = Path(output_folder)

    output_folder_path.mkdir(parents=True, exist_ok=True)

    output_image_path = output_folder_path / f"{username}.jpg"
    image.save(output_image_path)
    image.show()


# Example usage:
csv_file_path = "user_info.csv"
user_info_list = read_user_info_from_csv(csv_file_path)

generate_images(csv_file_path)