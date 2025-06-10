import requests
def enviar_mensagem_zapi_com_delaytyping(telefone, mensagem, tempo_digitando_segundos=None):
    """
    Envia uma mensagem de texto via Z-API com simulação de "digitando"
    controlada pelo parâmetro 'delayTyping' da API, que é adicionado
    ao payload do endpoint de envio de mensagem.

    Args:
        telefone (str): O número de telefone do destinatário (ex: "5585991604837").
        mensagem (str): A mensagem a ser enviada.
        tempo_digitando_segundos (int, optional):
            Segundos para que o status "Digitando..." seja exibido antes do envio da mensagem.
            Deve estar no range de 1 a 15 segundos, conforme a documentação.
            Se None, o 'delayTyping' não será incluído (API usará seu default, que é 0).
            Se 0, 'delayTyping' será 0 (sem "digitando").

    Returns:
        requests.Response: O objeto de resposta da requisição.
                           Retorna None em caso de erro.
    """
    instance_id = "COLOQUE AQUI A INSTACIA DO Z-API"
    api_token = "COLOQUE AQUI O TOKEN DO Z-API"
    client_token_header = "COLOQUE AQUI O TOKEN DE CLIENTE DO Z-API" # Mantenha seu Client-Token

    base_url = f"https://api.z-api.io/instances/{instance_id}/token/{api_token}"
    # Assumindo que 'send-text' é o endpoint que aceita o parâmetro 'delayTyping'
    url_send_text = f"{base_url}/send-text"

    headers = {
        "Client-Token": client_token_header,
        "Content-Type": "application/json"
    }

    payload_send_text = {
        "phone": telefone,
        "message": mensagem
    }

    # Adicionar 'delayTyping' ao payload se fornecido e válido
    if tempo_digitando_segundos is not None:
        if 1 <= tempo_digitando_segundos <= 15:
            payload_send_text["delayTyping"] = tempo_digitando_segundos
            print(f"INFO: 'delayTyping' configurado para {tempo_digitando_segundos} segundos.")
        elif tempo_digitando_segundos == 0:
            payload_send_text["delayTyping"] = 0
            print("INFO: 'delayTyping' configurado para 0 segundos (sem 'digitando' explícito).")
        else:
            # Fora do range recomendado pela Z-API (1-15), mas o usuário especificou.
            # Você pode optar por não enviar, ou enviar e deixar a API validar.
            # Por ora, vamos enviar e alertar.
            print(f"AVISO: 'tempo_digitando_segundos' ({tempo_digitando_segundos}) está fora do range recomendado pela Z-API (1-15s ou 0s). "
                  "O comportamento pode ser o default da API.")
            payload_send_text["delayTyping"] = tempo_digitando_segundos
    else:
        # Se tempo_digitando_segundos for None, não adicionamos 'delayTyping' ao payload.
        # A API usará seu comportamento default (0 segundos de 'digitando', conforme a documentação).
        print("INFO: 'delayTyping' não especificado, usando default da API (provavelmente 0s de 'digitando').")


    response_message = None
    try:
        print(f"\nINFO: Enviando mensagem para {telefone}.")
        print(f"DEBUG: URL de Envio: {url_send_text}")
        print(f"DEBUG: Payload de Envio: {str(payload_send_text)}")
        print(f"DEBUG: Headers de Envio: {str(headers)}")

        response_message = requests.post(url_send_text, json=payload_send_text, headers=headers)

        print(f"DEBUG: Resposta da API - Status HTTP: {response_message.status_code}")
        print(f"DEBUG: Resposta da API - Conteúdo: {response_message.text}")
        response_message.raise_for_status() # Levanta um erro para respostas HTTP 4xx/5xx
        print("INFO: Mensagem parece ter sido enviada com sucesso pela API.")
        return response_message
    except requests.exceptions.HTTPError as http_err:
        print(f"ERRO HTTP ao enviar mensagem: {http_err}")
        if response_message is not None: # Se houver uma resposta, mesmo com erro HTTP
            print(f"ERRO HTTP Conteúdo da resposta: {response_message.text}")
        return None
    except requests.exceptions.RequestException as e: # Erros de conexão, timeout, etc.
        print(f"ERRO DE REQUISIÇÃO ao enviar mensagem: {e}")
        return None
    except Exception as ex: # Outros erros inesperados
        print(f"ERRO INESPERADO ao enviar mensagem: {ex}")
        return None

# Exemplo de uso da função:
if __name__ == "__main__":
    numero_destino = "5511999999999"  # Substitua pelo número desejado

    print("\n--- Teste 1: Com 'delayTyping' de 5 segundos ---")
    mensagem_teste_1 = "Esta mensagem deve aparecer após 5s de 'digitando' (controlado pela API)."
    resposta1 = enviar_mensagem_zapi_com_delaytyping(numero_destino, mensagem_teste_1, tempo_digitando_segundos=5)
