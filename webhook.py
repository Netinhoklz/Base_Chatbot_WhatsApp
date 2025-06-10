import random
from flask import Flask, request, jsonify
import json
import threading  # Para timers e locks
from funcao_envio import *
from funcoes_chatgpt import *
from gerar_base_dados import *
import requests
import tempfile

app = Flask(__name__)

# --- Configurações e Estado Global ---
DELAY_SECONDS = 30  # Tempo de espera em segundos para acumular mensagens
accumulated_messages = {}  # Dicionário para guardar mensagens: { "phone_number": "msg1 msg2 msg3" }
active_timers = {}  # Dicionário para guardar timers ativos: { "phone_number": TimerObject }
processing_lock = threading.Lock()  # Lock para proteger o acesso aos dicionários acima


# --- Sua Função de Resposta ---
def responder_usuario(mensagens_acumuladas_str, numero_telefone):
    """
    Função chamada quando o timer expira, com as mensagens acumuladas.
    """
    # Conversa inicial
    prompt = 'Seja amigavel e divertido'
    # CRIE AQUI DENTRO O SEU CHATBOT PARA GERAR UMA RESPOSTA E ENVIAR PARA O CLIENTE
    # ATUALMENTE ELE ESTA RETORNANDO A MENSAGEM ACUMULADA
    resposta_chatgpt = conversa_com_chatgpt_sem_lembranca(texto_user=mensagens_acumuladas_str,prompt_comand=prompt)
    enviar_mensagem_zapi_com_delaytyping(telefone=numero_telefone, mensagem=resposta_chatgpt,tempo_digitando_segundos=5)


# --- Função de Transcrição (Simulada) ---
def transcrever_audio(audio_url: str, phone_sender_for_context: str = "") -> str:
    print(f"\nIniciando transcrição REAL para o áudio em: {audio_url}")

    # Tenta extrair um nome de arquivo da URL para fins de logging/contexto
    try:
        display_filename = os.path.basename(audio_url.split('?')[0])
    except:
        display_filename = "audio_desconhecido.ogg"  # Nome padrão

    temp_audio_file = None  # Para garantir que podemos tentar excluí-lo no finally

    try:
        # 1. Baixar o áudio da URL
        print(f"Baixando áudio de: {audio_url}...")
        response = requests.get(audio_url, stream=True, timeout=30)  # Timeout de 30s
        response.raise_for_status()  # Levanta um erro para códigos de status ruins (4xx ou 5xx)

        # Determinar a extensão do arquivo (se possível) para o arquivo temporário
        # Isso pode ajudar o Whisper se o formato for incomum, embora ele seja robusto.
        _, ext = os.path.splitext(display_filename)
        if not ext:  # Se não houver extensão na URL, use um padrão comum
            ext = ".ogg"  # Whisper lida bem com .ogg, .mp3, .wav, .m4a etc.

        # Criar um arquivo temporário para salvar o áudio
        # delete=False é importante para que possamos passar o nome do arquivo para outra função
        # e depois excluir manualmente.
        with tempfile.NamedTemporaryFile(delete=False, suffix=ext, mode='wb') as tmp_file:
            for chunk in response.iter_content(chunk_size=8192):  # Escreve em pedaços
                tmp_file.write(chunk)
            temp_audio_path = tmp_file.name

        print(f"Áudio baixado e salvo temporariamente em: {temp_audio_path}")

        # 2. Chamar sua função de transcrição com Whisper
        # (Assumindo que transcrever_audio_whisper está definida e importada)
        print(f"Enviando '{temp_audio_path}' para transcrição com Whisper...")
        texto_transcrito_puro = transcrever_audio_whisper(caminho_audio=temp_audio_path)

        # Montar a string de retorno final com o contexto
        if phone_sender_for_context:
            final_text = f"{texto_transcrito_puro}"
        else:
            final_text = f"{texto_transcrito_puro}"

        print(f"Transcrição concluída: '{final_text}'")
        return final_text

    except requests.exceptions.RequestException as e:
        print(f"Erro ao baixar o áudio de {audio_url}: {e}")
        return f"[ERRO DE DOWNLOAD ao tentar transcrever {display_filename} para {phone_sender_for_context}: {e}]"
    except Exception as e:
        # Captura outros erros, incluindo potenciais erros da função transcrever_audio_whisper
        print(f"Erro durante o processo de transcrição para {audio_url}: {e}")
        return f"[ERRO DE TRANSCRIÇÃO para {display_filename} (contexto: {phone_sender_for_context}): {e}]"
    finally:
        # 3. Limpeza: Excluir o arquivo de áudio temporário
        if temp_audio_path and os.path.exists(temp_audio_path):
            try:
                os.remove(temp_audio_path)
                print(f"Arquivo temporário '{temp_audio_path}' removido.")
            except Exception as e:
                print(f"Erro ao remover arquivo temporário '{temp_audio_path}': {e}")


# --- Função de Descrição de Imagem (Simulada) ---
def descrever_imagem(image_url: str, phone_sender_for_context: str = "") -> str:
    print(f"\nIniciando descrição REAL para a imagem em: {image_url}")

    # Tenta extrair um nome de arquivo da URL para fins de logging/contexto
    try:
        display_filename = os.path.basename(image_url.split('?')[0])
    except:
        display_filename = "imagem_desconhecida.jpg"  # Nome padrão

    temp_image_path = None  # Para garantir que podemos tentar excluí-lo no finally

    try:
        # 1. Baixar a imagem da URL
        print(f"  Baixando imagem de: {image_url}...")
        response = requests.get(image_url, stream=True, timeout=30)  # Timeout de 30s
        response.raise_for_status()  # Levanta um erro para códigos de status ruins (4xx ou 5xx)

        # Determinar a extensão do arquivo (se possível) para o arquivo temporário
        _, ext = os.path.splitext(display_filename)
        if not ext:  # Se não houver extensão na URL, tente obter do cabeçalho Content-Type ou use um padrão
            content_type = response.headers.get('content-type')
            if content_type and 'image/' in content_type:
                ext = "." + content_type.split('image/')[1].split(';')[0]  # ex: .jpeg, .png
            else:
                ext = ".jpg"  # Padrão se não conseguir determinar

        # Criar um arquivo temporário para salvar a imagem
        with tempfile.NamedTemporaryFile(delete=False, suffix=ext, mode='wb') as tmp_file:
            for chunk in response.iter_content(chunk_size=8192):  # Escreve em pedaços
                tmp_file.write(chunk)
            temp_image_path = tmp_file.name

        print(f"  Imagem baixada e salva temporariamente em: {temp_image_path}")

        # 2. Chamar sua função de descrição de imagem com o caminho do arquivo local
        print(f"  Enviando '{temp_image_path}' para descrição via GPT...")

        # AQUI você chama a SUA função que aceita image_path:
        # Substitua 'sua_funcao_gpt_descricao_imagem' pelo nome real da sua função.
        descricao_pura = descrever_imagem_gpt(image_path=temp_image_path)

        if descricao_pura is None:
            print(f"  Falha ao obter descrição da IA para {display_filename}.")
            return f"[ERRO NA DESCRIÇÃO DA IA para {display_filename} (contexto: {phone_sender_for_context})]"

        # Montar a string de retorno final com o contexto
        if phone_sender_for_context:
            final_text = f"Descrição da imagem: {descricao_pura}."
        else:
            final_text = f"Descrição da imagem: {descricao_pura}."
        print(f"  Descrição concluída: '{final_text}'")
        return final_text

    except requests.exceptions.RequestException as e:
        print(f"  Erro ao baixar a imagem de {image_url}: {e}")
        return f"[ERRO DE DOWNLOAD ao tentar descrever {display_filename} para {phone_sender_for_context}: {e}]"
    except Exception as e:
        # Captura outros erros, incluindo potenciais erros da sua função de descrição
        print(f"  Erro durante o processo de descrição para {image_url}: {e}")
        # Adicionar mais detalhes do erro se possível
        import traceback
        traceback.print_exc()
        return f"[ERRO GERAL NO PROCESSO DE DESCRIÇÃO para {display_filename} (contexto: {phone_sender_for_context}): {e}]"
    finally:
        # 3. Limpeza: Excluir o arquivo de imagem temporário
        if temp_image_path and os.path.exists(temp_image_path):
            try:
                os.remove(temp_image_path)
                print(f"  Arquivo temporário '{temp_image_path}' removido.")
            except Exception as e:
                print(f"  Erro ao remover arquivo temporário '{temp_image_path}': {e}")


# --- Função de Callback do Timer ---
def on_timer_expire(phone_number_key):
    with processing_lock:
        final_message_str = accumulated_messages.pop(phone_number_key, "").strip()
        active_timers.pop(phone_number_key, None)

        if final_message_str:
            print(f"\nTimer expirou para {phone_number_key}. Mensagem final a ser enviada: '{final_message_str}'")
            responder_usuario(final_message_str, phone_number_key)
        else:
            print(f"\nTimer expirou para {phone_number_key}, mas não havia mensagens acumuladas para enviar.")


@app.route('/webhook', methods=['POST'])
def webhook_receiver():
    print("\n=====================================================")
    print("NOVO WEBHOOK RECEBIDO!")
    print("=====================================================")

    content_type = request.headers.get('Content-Type', '').lower()
    if 'application/json' not in content_type:
        print(f"Conteúdo não é JSON (Content-Type: {content_type}). Ignorando.")
        return jsonify(success=False, error="Request must be JSON"), 415

    try:
        data = request.get_json()
        print("Dados JSON recebidos:")
        print(json.dumps(data, indent=2, ensure_ascii=False))

        message_type = data.get("type")
        if message_type != "ReceivedCallback":
            print(f"Tipo de evento não é 'ReceivedCallback' ({message_type}). Ignorando para acumulação.")
            return jsonify(success=True, message="Event type not processed for accumulation"), 200

        phone_sender = data.get("phone")
        if not phone_sender:
            print("Não foi possível identificar o 'phone' do remetente no payload. Ignorando.")
            return jsonify(success=False, error="Sender phone not found in payload"), 400

        message_parts_to_accumulate = []

        # 1. Verificar se é mensagem de texto
        text_object = data.get("text")
        if text_object and isinstance(text_object, dict):
            message_text = text_object.get("message")
            if message_text and isinstance(message_text, str) and message_text.strip():
                message_parts_to_accumulate.append(message_text.strip())
                print(f"Mensagem de texto recebida de {phone_sender}: '{message_text.strip()}'")

        # 2. Verificar se é mensagem de áudio
        audio_object = data.get("audio")
        if audio_object and isinstance(audio_object, dict):
            audio_url = audio_object.get("audioUrl")
            if audio_url:
                print(f"Mensagem de áudio recebida de {phone_sender}. URL: {audio_url}")
                transcribed_audio_text = transcrever_audio(audio_url, phone_sender)
                message_parts_to_accumulate.append(transcribed_audio_text)
            else:
                print(f"Objeto de áudio recebido de {phone_sender}, mas sem 'audioUrl'.")

        # 3. Verificar se é mensagem de imagem
        image_object = data.get("image")
        if image_object and isinstance(image_object, dict):
            image_url = image_object.get("imageUrl")
            caption = image_object.get("caption", "")

            if image_url:
                print(f"Mensagem de imagem recebida de {phone_sender}. URL: {image_url}")
                if caption and caption.strip():
                    message_parts_to_accumulate.append(f"Legenda da imagem: '{caption.strip()}'")
                    print(f"Legenda da imagem: '{caption.strip()}'")

                described_image_text = descrever_imagem(image_url, phone_sender)
                message_parts_to_accumulate.append(described_image_text)
            else:
                print(f"Objeto de imagem recebido de {phone_sender}, mas sem 'imageUrl'.")

        # 4. Verificar se é mensagem de vídeo
        video_object = data.get("video")
        if video_object and isinstance(video_object, dict):
            video_url = video_object.get("videoUrl")  # Apenas para confirmar que é um vídeo válido
            caption = video_object.get("caption", "")

            if video_url:  # Se tem videoUrl, consideramos que é uma mensagem de vídeo
                print(f"Mensagem de vídeo recebida de {phone_sender}.")
                video_notification_parts = []
                if caption and caption.strip():
                    video_notification_parts.append(f"Legenda do vídeo: '{caption.strip()}'")
                    print(f"Legenda do vídeo: '{caption.strip()}'")
                video_notification_parts.append("Você recebeu um vídeo.")
                message_parts_to_accumulate.append(" ".join(video_notification_parts))
            else:
                print(f"Objeto de vídeo recebido de {phone_sender}, mas sem 'videoUrl'.")

        if not message_parts_to_accumulate:
            print(f"Nenhum conteúdo para acumular de {phone_sender} nesta mensagem.")
            return jsonify(success=True, message="No content to accumulate"), 200

        text_to_accumulate_this_message = " ".join(message_parts_to_accumulate)

        with processing_lock:
            if phone_sender in active_timers:
                print(f"Cancelando timer existente para {phone_sender}.")
                active_timers[phone_sender].cancel()

            current_text_for_sender = accumulated_messages.get(phone_sender, "")
            accumulated_messages[phone_sender] = (
                        current_text_for_sender + " " + text_to_accumulate_this_message + " ").strip()

            print(f"Texto acumulado para {phone_sender}: '{accumulated_messages[phone_sender]}'")

            new_timer = threading.Timer(DELAY_SECONDS, on_timer_expire, args=[phone_sender])
            active_timers[phone_sender] = new_timer
            new_timer.start()
            print(f"Timer de {DELAY_SECONDS}s iniciado/reiniciado para {phone_sender}.")

        return jsonify(success=True, message="Message processed and accumulation timer updated."), 200

    except Exception as e:
        print(f"Erro ao processar JSON ou lógica do webhook: {e}")
        # import traceback
        # print(traceback.format_exc())
        return jsonify(success=False, error=f"Internal server error: {str(e)}"), 500


if __name__ == '__main__':
    print(f"Webhook rodando em http://0.0.0.0:5000/webhook")
    print(f"Delay para acumulação de mensagens: {DELAY_SECONDS} segundos.")
    app.run(host='0.0.0.0', port=5000, debug=False)
