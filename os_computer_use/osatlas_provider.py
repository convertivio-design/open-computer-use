from gradio_client import Client, handle_file
from os_computer_use.logging import logger
from os_computer_use.grounding import extract_bbox_midpoint

import os


OSATLAS_HUGGINGFACE_SOURCE = "maxiw/OS-ATLAS"
OSATLAS_HUGGINGFACE_MODEL = "OS-Copilot/OS-Atlas-Base-7B"
OSATLAS_HUGGINGFACE_API = "/run_example"

HF_TOKEN = os.getenv("HF_TOKEN")


class OSAtlasProvider:
    """
    The OS-Atlas provider is used to make calls to OS-Atlas.
    """

    def __init__(self):
        # IMPORTANT: Avoid network calls at import-time so the app can start even if
        # the Hugging Face space is temporarily down. We'll initialize lazily.
        self._client = None

    def _get_client(self) -> Client:
        if self._client is not None:
            return self._client

        try:
            self._client = Client(OSATLAS_HUGGINGFACE_SOURCE, hf_token=HF_TOKEN)
            return self._client
        except Exception as e:
            raise RuntimeError(
                "Failed to initialize OS-Atlas (Hugging Face space). "
                "The space may be down or rate-limited. "
                "Try again later, set HF_TOKEN, or switch `grounding_model` in `os_computer_use/config.py`."
            ) from e

    def call(self, prompt, image_data):
        client = self._get_client()
        result = client.predict(
            image=handle_file(image_data),
            text_input=prompt + "\nReturn the response in the form of a bbox",
            model_id=OSATLAS_HUGGINGFACE_MODEL,
            api_name=OSATLAS_HUGGINGFACE_API,
        )
        position = extract_bbox_midpoint(result[1])
        image_url = result[2]
        logger.log(f"bbox {image_url}", "gray")
        return position
