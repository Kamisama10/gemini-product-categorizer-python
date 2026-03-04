import os
from google import genai
from dotenv import load_dotenv

load_dotenv()

CHAVE_API_GOOGLE = os.getenv('GEMINI_API_KEY')
client = genai.Client(api_key=CHAVE_API_GOOGLE)

MODELO_ESCOLHIDO = 'gemini-2.0-flash'


def categorizar_produto(nome_produto, lista_categorias_possiveis):
    prompt_sistema = f"""
Você é um categorizador de produtos.

Você deve usar APENAS as categorias abaixo:
{lista_categorias_possiveis}

Formato da saída:
Produto: <nome do produto>
Categoria: <uma das categorias da lista>

Exemplo:
Produto: Escova elétrica com recarga solar
Categoria: Eletrônicos verdes
"""

    resposta = client.models.generate_content(
        model=MODELO_ESCOLHIDO,
        contents=f"{prompt_sistema}\nProduto: {nome_produto}"
    )

    return resposta.text.strip()


def main():
    lista_categorias_possiveis = 'Eletrônicos verdes, moda sustentável, produtos de limpeza ecológicos, alimentos orgânicos'

    produto = input('Informe o produto que você deseja classificar: ')

    while produto != "":
        print(f'Resposta: {categorizar_produto(produto, lista_categorias_possiveis)}')
        produto = input('Informe o produto que você deseja classificar: ')


if __name__ == '__main__':
    main()



