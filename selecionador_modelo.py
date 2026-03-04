import os
from google import genai
from dotenv import load_dotenv

load_dotenv()

CHAVE_API_GOOGLE = os.getenv("GEMINI_API_KEY")
client = genai.Client(api_key=CHAVE_API_GOOGLE)

MODELO_FLASH = "gemini-2.0-flash"
MODELO_PRO = "gemini-2.0-pro"
LIMITE_TOKENS = 3000


def carrega(nome_do_arquivo):
    try:
        with open(nome_do_arquivo, "r", encoding="utf-8") as arquivo:
            return arquivo.read()
    except IOError as e:
        print(f"Erro ao ler arquivo: {e}")
        return ""


prompt_sistema = """
Identifique o perfil de compra para cada cliente a seguir.

O formato de saída deve ser:

cliente - descreva o perfil do cliente em 3 palavras
"""

prompt_usuario = carrega("dados/lista_de_compras_100_clientes.csv")


contagem = client.models.count_tokens(
    model=MODELO_FLASH,
    contents=prompt_usuario
)

qtd_tokens = contagem.total_tokens

modelo_escolhido = MODELO_FLASH

if qtd_tokens >= LIMITE_TOKENS:
    modelo_escolhido = MODELO_PRO

print(f"O modelo selecionado foi: {modelo_escolhido}")
print(f"Quantidade de tokens: {qtd_tokens}")


resposta = client.models.generate_content(
    model=modelo_escolhido,
    contents=f"{prompt_sistema}\n{prompt_usuario}"
)

print("Resposta:")
print(resposta.text)