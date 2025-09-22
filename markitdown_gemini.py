import os
from markitdown import MarkItDown
from dotenv import load_dotenv
from genai_adapter import GeminiClientAdapter

load_dotenv()

model_name = "gemini-2.5-flash" 
KEY = os.environ.get("GEMINI_API_KEY")

gemini_adapter_client = GeminiClientAdapter(api_key=KEY, model_name=model_name)

md = MarkItDown(llm_client=gemini_adapter_client, 
                llm_model=model_name,
                llm_prompt="Em 3 parágrafos descreva a imagem detalhadamente em pt-br")

result = md.convert("https://ars.els-cdn.com/content/image/1-s2.0-S2590005625001389-gr1.jpg")


#salve o resultado em "processo_revisão.md"
with open("processo_revisão.md", "w", encoding="utf-8") as f:
    f.write(result.text_content)
    