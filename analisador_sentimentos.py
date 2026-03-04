import os
from google import genai
from google.api_core.exceptions import NotFound
from dotenv import load_dotenv

load_dotenv()

CHAVE_API_GOOGLE = os.getenv("GEMINI_API_KEY")
client = genai.Client(api_key=CHAVE_API_GOOGLE)

MODELO_ESCOLHIDO = "gemini-2.0-flash"


def carrega(nome_do_arquivo):
    try:
        with open(nome_do_arquivo, "r", encoding="utf-8") as arquivo:
            return arquivo.read()
    except IOError as e:
        print(f"Erro ao ler arquivo: {e}")
        return ""


def salva(nome_do_arquivo, conteudo):
    try:
        with open(nome_do_arquivo, "w", encoding="utf-8") as arquivo:
            arquivo.write(conteudo)
    except IOError as e:
        print(f"Erro ao salvar arquivo: {e}")


def analisador_sentimentos(nome_produto):
    prompt_sistema = """
Você é um analisador de sentimentos de avaliações de produtos.
Escreva um parágrafo com até 50 palavras resumindo as avaliações e
depois atribua qual o sentimento geral para o produto.
Identifique também 3 pontos fortes e 3 pontos fracos identificados a partir das avaliações.

# Formato de Saída

Nome do Produto:
Resumo das Avaliações:
Sentimento Geral: [utilize aqui apenas Positivo, Negativo ou Neutro]
Pontos fortes:
- ...
- ...
- ...
Pontos fracos:
- ...
- ...
- ...
"""

    arquivo_entrada = f"dados/avaliacoes-{nome_produto}.txt"
    arquivo_saida = f"dados/resposta-{nome_produto}.txt"

    prompt_usuario = carrega(arquivo_entrada)

    print(f"Iniciando a análise de sentimentos do produto: {nome_produto}")

    try:
        resposta = client.models.generate_content(
            model=MODELO_ESCOLHIDO,
            contents=f"{prompt_sistema}\n{prompt_usuario}"
        )

        texto_resposta = resposta.text
        salva(arquivo_saida, texto_resposta)

    except NotFound as e:
        print(f"Modelo não encontrado ({MODELO_ESCOLHIDO}). Tentando modelo alternativo...")

        modelo_alternativo = "gemini-1.5-flash"

        resposta = client.models.generate_content(
            model=modelo_alternativo,
            contents=f"{prompt_sistema}\n{prompt_usuario}"
        )

        texto_resposta = resposta.text
        salva(arquivo_saida, texto_resposta)


def main():
    lista_de_produtos = [
        "Camisetas de algodão orgânico",
        "Jeans feitos com materiais reciclados",
        "Maquiagem mineral"
    ]

    for um_produto in lista_de_produtos:
        analisador_sentimentos(um_produto)


if __name__ == "__main__":
    main()