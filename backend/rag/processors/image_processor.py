from PIL import Image

from transformers import (
    BlipProcessor,
    BlipForConditionalGeneration
)


processor = (
    BlipProcessor.from_pretrained(
        "Salesforce/blip-image-captioning-large"
    )
)

model = (
    BlipForConditionalGeneration.from_pretrained(
        "Salesforce/blip-image-captioning-large"
    )
)


def generate_caption(
    image_path
):

    image = Image.open(
        image_path
    ).convert("RGB")

    inputs = processor(
        image,
        return_tensors="pt"
    )

    output = model.generate(
        **inputs
    )

    caption = processor.decode(
        output[0],
        skip_special_tokens=True
    )

    return caption