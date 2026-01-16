import ast
from datetime import datetime
from PIL import Image, ImageDraw
from gradio_client import Client, handle_file

SHOWUI_HUGGINGFACE_SOURCE = "showlab/ShowUI"
SHOWUI_HUGGINGFACE_MODEL = "showlab/ShowUI-2B"
SHOWUI_HUGGINGFACE_API = "/on_submit"

class ShowUIProvider:
    """
    The ShowUI provider is used to make calls to ShowUI.
    """

    def __init__(self):
        # IMPORTANT: Avoid network calls at import-time so the app can start even if
        # the Hugging Face space is temporarily down. We'll initialize lazily.
        self._client = None

    def _get_client(self) -> Client:
        if self._client is not None:
            return self._client

        try:
            self._client = Client(SHOWUI_HUGGINGFACE_SOURCE)
            return self._client
        except Exception as e:
            raise RuntimeError(
                "Failed to initialize ShowUI (Hugging Face space). "
                "The space may be down or rate-limited. "
                "Try again later or switch `grounding_model` in `os_computer_use/config.py`."
            ) from e

    def extract_norm_point(self, response, image_url):
        if isinstance(image_url, str):
            image = Image.open(image_url)
        else:
            # Best-effort conversion without requiring numpy as a dependency.
            image = Image.fromarray(image_url)
        
        point = ast.literal_eval(response)
        if len(point) == 2:
            x, y = point[0] * image.width, point[1] * image.height
            return x, y
        else:
            return None

    def call(self, prompt, image_data):
        client = self._get_client()
        result = client.predict(
            image=handle_file(image_data),
            query=prompt,
            iterations=1,
            is_example_image="False",
            api_name=SHOWUI_HUGGINGFACE_API,
        )
        pred = result[1]
        img_url = result[0][0]['image']
        result = self.extract_norm_point(pred, img_url)
        return result

if __name__ == "__main__":
    showuiprovider = ShowUIProvider()
    img_url = "/home/qinghong/example/demo/chrome.png"
    query = "search box"
    result = showuiprovider.call(query, img_url)
    print(result)