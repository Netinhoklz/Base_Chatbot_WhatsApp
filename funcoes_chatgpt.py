import json
import time
import base64
import openai
import numpy
from openai import OpenAI
import os
from dotenv import load_dotenv

# Carrega as variáveis do arquivo .env para o ambiente
load_dotenv()
apinumber = os.getenv("OPENAI_API_KEY")
client = OpenAI(api_key=apinumber)
# O CHATBOT ESTA CONFIGURADO PARA USAR LLMs DE PENSAMENTO
# PARA USAR OUTRO SEJA PRECISO AJUSTAR A O PARAMETRO max_completion_tokens
def conversa_com_chatgpt_sem_lembranca(texto_user: str,prompt_comand:str = "Você é um assistente", modelo: str = "o4-mini",maximo_tokens_usado:int=300) -> str:
    """
    Função que analisa um texto fornecido pelo usuário, utilizando a API da OpenAI.

    Args:
        texto (str): Texto a ser analisado.
        modelo (str): Modelo da OpenAI a ser utilizado (padrão: "gpt-4").

    Returns:
        str: Resultado da análise do texto.
    """
    resposta = client.chat.completions.create(
        model=modelo,
        messages=[
            {"role": "system", "content": prompt_comand},
            {"role": "user", "content": texto_user}
        ],
        max_completion_tokens=maximo_tokens_usado

    )

    return resposta.choices[0].message.content.strip()


def conversa_com_chatgpt_com_lembranca(historico_mensagem: list, modelo: str = "o4-mini",maximo_tokens_usado:int=300) -> str:
    """
    Função que analisa um texto fornecido pelo usuário, utilizando a API da OpenAI.

    Args:
        texto (str): Texto a ser analisado.
        modelo (str): Modelo da OpenAI a ser utilizado (padrão: "gpt-4").

    Returns:
        str: Resultado da análise do texto.
    """
    resposta = client.chat.completions.create(
        model=modelo,
        messages=historico_mensagem,
        max_completion_tokens=maximo_tokens_usado

    )

    return resposta.choices[0].message.content.strip()
# --- Função para codificar a imagem em Base64 ---
def encode_image_to_base64(image_path: str) -> str:
    """
    Codifica um arquivo de imagem em uma string Base64.

    Args:
        image_path: O caminho para o arquivo de imagem.

    Returns:
        A string Base64 codificada.
    """
    with open(image_path, "rb") as image_file:
        return base64.b64encode(image_file.read()).decode('utf-8')

# --- Função principal para descrever a imagem ---
def descrever_imagem_gpt(image_path: str) -> str | None:
    """
    Obtém uma descrição de uma imagem local usando a API de Chat Multimodal da OpenAI.

    Args:
        image_path: O caminho para o arquivo de imagem.

    Returns:
        A descrição da imagem como uma string, ou None em caso de erro.
    """
    if not client.api_key:
        print("Erro: Chave de API da OpenAI não configurada.")
        print("Por favor, defina a variável de ambiente OPENAI_API_KEY.")
        return None

    try:
        # 1. Codificar a imagem em Base64
        print(f"Codificando imagem: {image_path}...")
        base64_image = encode_image_to_base64(image_path)
        print("Imagem codificada com sucesso.")

        # 2. Definir o prompt
        prompt_texto = '''
        # Missão
        - Dar o contexto da imagem que você recebeu para uma outra IA que irá responder a pessoa.
        # Objetivo
        - Descrever com o máximo de detalhe a imagem.''' # Pedindo uma descrição detalhada

        # 3. Preparar as mensagens para a API (formato multimodal)
        messages_list = [
            {
                "role": "user",
                "content": [
                    {"type": "text", "text": prompt_texto},
                    {
                        "type": "image_url",
                        "image_url": {
                            # O prefixo data:image/jpeg;base64, é necessário
                            "url": f"data:image/jpeg;base64,{base64_image}"
                            # Opcional: especificar o nível de detalhe (auto, low, high)
                            # "detail": "auto"
                        }
                    }
                ]
            }
        ]

        # 4. Fazer a requisição à API de Chat
        print("Enviando requisição para a API da OpenAI...")
        response = client.chat.completions.create(
            model="gpt-4o-mini", # Modelo com capacidades de visão
            messages=messages_list,
            max_tokens=300,      # Limita o tamanho da resposta para evitar custos excessivos
            temperature=1     # Controla a criatividade (0.0 para determinístico, 1.0 para mais criativo)
        )
        print("Resposta recebida da API.")

        # 5. Extrair o texto da resposta
        description = response.choices[0].message.content

        # 6. Retornar a descrição
        return description

    except FileNotFoundError:
        print(f"Erro: Arquivo não encontrado em {image_path}. Verifique o caminho.")
        return None
    except Exception as e:
        # Captura outros possíveis erros (API, base64, etc.)
        print(f"Ocorreu um erro ao processar a imagem ou chamar a API: {e}")
        return None


def transcrever_audio_whisper(caminho_audio: str, modelo: str = "whisper-1") -> str:
    """
    Transcreve um arquivo de áudio para texto usando o modelo Whisper da OpenAI.

    Args:
        caminho_audio (str): O caminho completo ou relativo para o arquivo de áudio.
                             O arquivo será aberto em modo binário ('rb').
                             Formatos suportados pelo Whisper: mp3, mp4, mpeg, mpga, m4a, wav, webm.
                             Consulte a documentação da OpenAI para a lista mais atualizada.
        modelo (str): O modelo Whisper a ser utilizado (padrão: "whisper-1").

    Returns:
        str: O texto transcrito do áudio.

    Raises:
        FileNotFoundError: Se o arquivo de áudio especificado não for encontrado.
        openai.APIError: Se ocorrer um erro na chamada da API da OpenAI.
        Exception: Para outros erros inesperados durante a operação.
    """
    # Verificar se o arquivo existe antes de tentar abrir
    if not os.path.exists(caminho_audio):
        raise FileNotFoundError(f"Erro: Arquivo de áudio não encontrado em '{caminho_audio}'")

    try:
        # Abre o arquivo de áudio em modo binário para leitura
        with open(caminho_audio, "rb") as audio_file:
            # Chama a API de transcrição de áudio
            # O Whisper é acessado via client.audio.transcriptions.create
            transcricao = client.audio.transcriptions.create(
                model=modelo,  # Especifica o modelo Whisper (whisper-1 é o padrão e recomendado)
                file=audio_file, # Passa o objeto arquivo
                language="pt"  # Para especificar o idioma (útil para melhorar a precisão)
                # Você pode adicionar outros parâmetros aqui, como:
                # prompt="Algumas palavras específicas que podem aparecer no áudio." # Para guiar a transcrição
                # response_format="json" # Para obter mais detalhes, como timestamps (requer parsing adicional)
            )

        # A resposta da API para transcrições é um objeto com o texto transcrito
        # no atributo 'text'.
        return transcricao.text

    except openai.APIError as e:
        print(f"Erro da API da OpenAI durante a transcrição: {e}")
        # Re-lança a exceção para que o código chamador possa tratá-la, se necessário.
        raise

    except Exception as e:
        print(f"Ocorreu um erro inesperado durante a transcrição: {e}")
        # Re-lança a exceção
        raise

if __name__ == "__main__":
    # Exemplo de uso simples no console
    # print("Assistente iniciado. Digite 'sair' para encerrar.")

    prompt_teste = '''Seja amigavel e divertido'''
    while True:
        user_input = input("Você: ")
        if user_input.strip().lower() == "sair":
            print("Encerrando...")
            break

        resposta = conversa_com_chatgpt_sem_lembranca(texto_user=user_input,modelo='o4-mini',prompt_comand=prompt_teste,maximo_tokens_usado=1000)
        print("Assistente:", resposta)
