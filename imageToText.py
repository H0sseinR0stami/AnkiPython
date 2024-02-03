from PIL import Image
import pytesseract

# Set the path to tesseract.exe
# For example, if you've installed Tesseract in the default directory, it might look like this on Windows:
pytesseract.pytesseract.tesseract_cmd = r'C:\Program Files\Tesseract-OCR\tesseract.exe'

def image_to_text(image_path, output_file):
    # Open the image file
    img = Image.open(image_path)

    # Use pytesseract to do OCR on the image
    text = pytesseract.image_to_string(img, lang='eng')

    # Write the text to a file
    with open(output_file, 'w') as file:
        file.write(text)

    print(f"Text has been saved to {output_file}")


# Replace 'path_to_image.jpg' with the path to your image file
# Replace 'output.txt' with your desired output file name
image_path = './inputImage/image.jpg'
output_file = './outTextFromImage/out.txt'
image_to_text(image_path, output_file)
