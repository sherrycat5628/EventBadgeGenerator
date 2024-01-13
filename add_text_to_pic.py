import csv
import logging
from pathlib import Path

from PIL import Image, ImageDraw, ImageFont


logging.basicConfig(filename='log.txt', level=logging.INFO)


def generate_images(csv_file, output_folder="badge"):
    user_info_list = read_user_info_from_csv(csv_file)
    output_folder_path = Path(output_folder)
    output_folder_path.mkdir(parents=True, exist_ok=True)

    for user_info in user_info_list:
        add_text_to_image(user_info, output_folder_path)


def read_user_info_from_csv(csv_file):
    with open(csv_file, newline="", encoding="utf-8") as csvfile:
        reader = csv.reader(csvfile)
        next(reader)  # Skip header
        return [tuple(row) for row in reader]


def add_text_to_image(user_info, output_folder_path):
    username, club_info, division_info, option_info, remark, option = user_info

    option_A = 'one day ticket without meal'
    option_B = 'one day ticket with meal'
    option_C = 'two day ticket with meal'
    option = option.strip().replace("'", "")

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

    with Image.open(image_path) as image:
        draw = ImageDraw.Draw(image)
        font_path = "/System/Library/Fonts/Supplemental/Arial Unicode.ttf"
        font = ImageFont.truetype(font_path, 20)

        text_positions = [
            (420, username),
            (450, club_info),
            (500, division_info),
            (550, option_info),
            (600, remark),
        ]

        for y, text in text_positions:
            x = (image.width - 1) / 2
            draw.text((x, y - 1 / 2), text, font=font, fill=(0, 0, 0), anchor="mm")

        output_image_path = output_folder_path / f"{username}.jpg"
        image.save(output_image_path)


csv_file_path = "user_info.csv"
generate_images(csv_file_path)