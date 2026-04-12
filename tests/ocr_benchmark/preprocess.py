from pathlib import Path

from PIL import Image

def preprocess_image(image_path: str, output_path: str, scale_factor: int = 4) -> str:
    image = Image.open(image_path)

    image = image.resize(
        (image.width * scale_factor, image.height * scale_factor),
        Image.Resampling.NEAREST,
    )

    image = image.convert("L") # set Grayscale


    threshold = 160
    def threshold_pixel(value: int) -> int:
        return 255 if value > threshold else 0
    image = image.point(threshold_pixel)

    Path(output_path).parent.mkdir(parents=True, exist_ok=True)
    image.save(output_path)

    return output_path
