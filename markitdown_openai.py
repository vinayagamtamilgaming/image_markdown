from markitdown import MarkItDown
from openai import OpenAI

client = OpenAI()
md = MarkItDown(llm_client=client, 
                llm_model="gpt-5-mini", 
                llm_prompt="Em 3 parágrafos descreva a imagem detalhadamente em pt-br")

result = md.convert("sandeco.jpg")

#salve o resultado em "processo_revisão.md"
with open("sandeco.md", "w", encoding="utf-8") as f:
    f.write(result.text_content)
    