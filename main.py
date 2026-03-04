import os
from google import genai
from dotenv import load_dotenv

load_dotenv()

CHAVE_API_GOOGLE = os.getenv('GEMINI_API_KEY')
client = genai.Client(api_key=CHAVE_API_GOOGLE)
MODELO_ESCOLHIDO = 'gemini-2.0-flash'

prompt_sistema = 'Liste apenas os nomes dos produtos, e ofereça uma breve descrição.'

configuracao_modelo = {
    "temperature": 2.0,
    "top_p": 0.9,
    "top_k": 64,
    "max_output_tokens": 8192,
}

pergunta = 'Liste três produtos de moda sustentável para ir ao shopping.'

resposta = client.models.generate_content(
    model=MODELO_ESCOLHIDO,
    contents=f"{prompt_sistema}\n{pergunta}",
    config=configuracao_modelo
)

print(f'A resposta gerada para a pergunta é: {resposta.text}')
