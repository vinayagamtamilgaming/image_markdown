import base64
import io
from PIL import Image
from google import genai


# Classes auxiliares para simular a resposta da OpenAI (sem alterações)
class _MockChoice:
    def __init__(self, content):
        self.message = type('obj', (object,), {'content': content})()

class _MockResponse:
    def __init__(self, content):
        self.choices = [_MockChoice(content)]

# A classe Adaptadora, agora responsável por criar seu próprio cliente
class GeminiClientAdapter:
    def __init__(self, api_key: str, model_name: str):
        """
        O construtor agora recebe a api_key e o model_name.
        Ele cria o cliente do genai internamente.
        """
        self.client = genai.Client(api_key=api_key)

        self.client_models = self.client.models
        self.model_name = model_name
        self.chat = self
        self.completions = self

    def create(self, model, messages, **kwargs):
        prompt = ""
        image_url = ""
        for part in messages[0]['content']:
            if part['type'] == 'text':
                prompt = part['text']
            elif part['type'] == 'image_url':
                image_url = part['image_url']['url']

        header, encoded = image_url.split(",", 1)
        image_data = base64.b64decode(encoded)
        image = Image.open(io.BytesIO(image_data))

        response = self.client_models.generate_content(
            model=f"models/{self.model_name}",
            contents=[prompt, image]
        )
        
        text_result = ""
        try:
            text_result = response.text
        except AttributeError:
            if response.candidates:
                text_result = response.candidates[0].content.parts[0].text

        return _MockResponse(content=text_result)

# --- FIM DO CÓDIGO DO ADAPTADOR ---
