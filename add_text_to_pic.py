import logging
from pathlib import Path


from PIL import Image, ImageDraw, ImageFont


logging.basicConfig(
    filename='skipped_name_list.txt',
    format='%(asctime)s: %(levelname)s: %(message)s',
    datefmt='%Y-%m-%d %H:%M:%S %z',
    level=logging.INFO,
)


def generate_images(username, club, division, option_info, remark, ticket_type, output_folder=None):
    """
    Generate badge images for users.

    :param username: Username of the user.
    :param club: Information about the club.
    :param division: Information about the division.
    :param option_info: Information about the option.
    :param remark: Any remark for the user.
    :param ticket_type: Type of the ticket chosen by the user.
    :param output_folder: Output folder for saving badge images.
    """
    output_folder_path = Path(output_folder) if output_folder else Path(__file__).parent / "generated_images"
    # output_folder_path = Path(output_folder) if output_folder else Path(__file__).parent
    add_text_to_image(username, club, division, option_info, remark, ticket_type, output_folder_path, username)


def add_text_to_image(username, club, division, option_info, remark, ticket_type, output_folder_path, output_filename):
    """
    Add text to badge image.

    :param username: Username of the user.
    :param club: Information about the club.
    :param division: Information about the division.
    :param option_info: Information about the option.
    :param remark: Any remark for the user.
    :param ticket_type: Type of the ticket chosen by the user.
    :param output_folder_path: Path to the output folder.
    :param output_filename: Name of the output file.
    """
    output_image_path = output_folder_path / f"{output_filename}.jpg"

    ticket_option_mapping = {
        'one day ticket without meal': 'ticket_type/optionA.jpg',
        'one day ticket with meal': 'ticket_type/optionB.jpg',
        'two day ticket with meal': 'ticket_type/optionC.jpg'
    }

    ticket_type = ticket_type.strip()
    image_path = ticket_option_mapping.get(ticket_type)
    if not image_path:
        logging.error(f"Invalid ticket type for user {username}: {ticket_type}")
        return

    with Image.open(image_path) as image:
        image = image.convert("RGB")

        draw = ImageDraw.Draw(image)
        font_path = "/System/Library/Fonts/Supplemental/Arial Unicode.ttf"
        font = ImageFont.truetype(font_path, 20)

        text_positions = [
            (420, username),
            (450, club),
            (500, division),
            (550, option_info),
            (600, remark),
        ]

        for y, text in text_positions:
            x = (image.width - 1) / 2
            draw.text((x, y - 1 / 2), text, font=font, fill=(0, 0, 0), anchor="mm")

        image.save(output_image_path)

#Example usage
#generate_images("John Doe", "Awesome Club", "Division A", "Option info", "Remark", "one day ticket with meal")
