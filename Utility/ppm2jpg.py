import os
from PIL import Image

def convert_ppm_to_jpg(input_folder, output_folder):
    if not os.path.exists(output_folder):
        os.makedirs(output_folder)

    for filename in os.listdir(input_folder):
        if filename.endswith(".ppm"):
            ppm_path = os.path.join(input_folder, filename)
            with Image.open(ppm_path) as im:
                jpg_filename = os.path.splitext(filename)[0] + ".jpg"
                jpg_path = os.path.join(output_folder, jpg_filename)
                im.convert('RGB').save(jpg_path, "JPEG")
            print(f"Convertito {ppm_path} a {jpg_path}")

if __name__ == "__main__":
    input_folder = "dataset/input/directory"
    output_folder = "dataset/output/directory"
    convert_ppm_to_jpg(input_folder, output_folder)
