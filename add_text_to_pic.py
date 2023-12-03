import csv

from PIL import Image, ImageDraw, ImageFont


def read_user_info_from_csv(csv_file):
    user_info_list = []
    with open(csv_file, newline="", encoding="utf-8") as csvfile:
        reader = csv.reader(csvfile)
        next(reader)  # Skip header if exists
        for row in reader:
            user_info_list.append(tuple(row))
    return user_info_list



def add_text_to_image(image_path, user_info):
    # Open the image
    image = Image.open(image_path)

    # Get the size of the image
    image_width, image_height = image.size
    print(f"Image size: {image_width} x {image_height}")

    # Initialize ImageDraw
    draw = ImageDraw.Draw(image)

    # Set font and size 
    font_path = "/System/Library/Fonts/Supplemental/Arial Unicode.ttf"
    font_size = 20
    font = ImageFont.truetype(font_path, font_size)

    # Unpack user_info tuple
    username, club_info, division_info, option_info, remark = user_info

    text_positions = [
        (1000, 400, username),  
        (1000, 450, club_info),  #
        (1000, 500, division_info),  
        (1000, 550, option_info),  
        (1000, 600, remark), 
        ]
    
    # Add text to image
    for x, y, text in text_positions:
        draw.text(
            (x, y), text, font=font, fill=(0, 0, 0)
            )  # You can adjust the fill color

    # Save or display the modified image for each row
    output_image_path = f"output_image_{username}.jpg"  # Using username for unique filenames
    image.save(output_image_path)
    image.show()


# Example usage:
csv_file_path = "user_info.csv"
user_info_list = read_user_info_from_csv(csv_file_path)

# Process all rows from the CSV file
for user_info_row in user_info_list:
    add_text_to_image("input_image.jpg", user_info_row)
    print(user_info_row)