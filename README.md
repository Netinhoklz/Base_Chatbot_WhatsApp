<div align="center">
  <a href="https://z-api.io/">
    <img src="https://z-api.io/wp-content/uploads/2023/04/Z-API.svg" alt="Z-API Logo" width="200"/>
  </a>
</div>

<h1 align="center">Chatbot Inteligente com Acumulador de Mensagens</h1>

<p align="center">
  <strong>Um backend robusto para WhatsApp que agrupa mensagens de texto, áudio e imagem para gerar respostas de IA mais ricas e contextuais.</strong>
</p>

<p align="center">
  <img src="https://img.shields.io/badge/Python-3.8%2B-blue.svg" alt="Python Version">
  <img src="https://img.shields.io/badge/Framework-Flask-black.svg" alt="Flask Framework">
  <img src="https://img.shields.io/badge/Integração-Z--API-brightgreen.svg" alt="Z-API Integration">
  <img src="https://img.shields.io/badge/License-MIT-yellow.svg" alt="License">
</p>

---

## 📋 Índice

1.  [**Visão Geral**](#-visão-geral)
    *   [Objetivo do Projeto](#-objetivo-do-projeto)
    *   [Principais Funcionalidades](#-principais-funcionalidades)
2.  [**Arquitetura do Sistema**](#-arquitetura-do-sistema)
    *   [Diagrama de Fluxo](#-diagrama-de-fluxo)
    *   [Componentes Chave](#-componentes-chave)
3.  [**Como Funciona: O Fluxo de uma Conversa**](#-como-funciona-o-fluxo-de-uma-conversa)
4.  [**Guia de Instalação e Configuração**](#-guia-de-instalação-e-configuração)
    *   [Pré-requisitos](#-pré-requisitos)
    *   [Passos de Instalação](#-passos-de-instalação)
    *   [Configurando o Ambiente](#-configurando-o-ambiente)
    *   [Executando o Servidor](#-executando-o-servidor)
5.  [**Customização e Extensibilidade**](#-customização-e-extensibilidade)
    *   [Implementando a Lógica da IA](#-implementando-a-lógica-da-ia)
    *   [Adaptando para Outras Plataformas](#-adaptando-para-outras-plataformas)
6.  [**Melhorias Futuras**](#-melhorias-futuras)
7.  [**Licença**](#-licença)

---

## 🎯 Visão Geral

Este projeto implementa um serviço de backend para um chatbot de WhatsApp que se destaca por sua capacidade de **acumular mensagens de forma inteligente**. Em vez de responder reativamente a cada interação, o sistema aguarda uma pausa na conversa do usuário para consolidar múltiplas mensagens — incluindo texto, áudios transcritos e descrições de imagens — em um único prompt contextual.

Este prompt unificado permite que modelos de linguagem (LLMs) como o GPT-4 gerem respostas muito mais coesas, precisas e humanizadas, transformando interações fragmentadas em um diálogo fluido.

### 🌟 Objetivo do Projeto

O principal objetivo é superar a limitação de chatbots tradicionais que processam cada mensagem isoladamente. Ao criar um "buffer de contexto", o bot pode entender a intenção completa do usuário, mesmo que ela seja expressa em várias partes, resultando em uma experiência de usuário drasticamente superior.

### ✨ Principais Funcionalidades

*   **Acumulador de Mensagens:** Consolida mensagens enviadas em um curto intervalo de tempo.
*   **Suporte Multimodal Completo:**
    *   💬 **Texto:** Processa mensagens de texto padrão.
    *   🎤 **Áudio:** Transcreve automaticamente mensagens de voz para texto usando **OpenAI Whisper**.
    *   🖼️ **Imagem:** Gera descrições textuais de imagens enviadas usando **GPT-4 Vision**.
    *   📹 **Vídeo:** Reconhece o recebimento de vídeos e captura suas legendas.
*   **Temporizador Dinâmico:** Um temporizador reinicia a cada nova mensagem, acionando a resposta apenas quando o usuário faz uma pausa.
*   **Arquitetura Flexível:** Projetado para ser independente da API de envio, permitindo fácil adaptação a qualquer serviço de mensageria (Telegram, Messenger, etc.).
*   **Segurança de Concorrência:** Utiliza `threading.Lock` para garantir o processamento seguro e sem conflitos de mensagens de múltiplos usuários simultâneos.

---

## 🏗️ Arquitetura do Sistema

O sistema é construído sobre uma base de Python e Flask, com uma arquitetura simples, porém poderosa, focada em modularidade e performance.

### 🌊 Diagrama de Fluxo

```mermaid
sequenceDiagram
    participant User as Usuário (WhatsApp)
    participant ZApi as Z-API
    participant Server as Servidor Flask
    participant AI as Lógica de IA (GPT)

    User->>ZApi: Envia Mensagem (Texto/Áudio/Imagem)
    ZApi->>Server: POST /webhook com dados da msg
    Server->>Server: Extrai conteúdo e identifica tipo
    Note right of Server: Se áudio, transcreve.<br/>Se imagem, descreve.
    Server->>Server: Acumula texto no buffer do usuário
    Server->>Server: Reinicia o timer de 30s
    User->>ZApi: Envia outra mensagem (dentro de 30s)
    ZApi->>Server: POST /webhook ...
    Server->>Server: Repete processo de acumulação e reinicia o timer
    
    loop Timer Expira
        Note over Server: Usuário parou de enviar mensagens.
        Server->>Server: Timer de 30s expira.
    end
    
    Server->>AI: Envia prompt consolidado
    AI-->>Server: Retorna resposta completa
    Server->>ZApi: Envia resposta para o usuário via API
    ZApi-->>User: Entrega a resposta do bot
Use code with caution.
🧩 Componentes Chave
app.py (Servidor Flask): O núcleo da aplicação. Recebe webhooks, gerencia o estado da aplicação (mensagens e timers) e orquestra todo o fluxo.
funcoes_chatgpt.py: Módulo responsável pela interação com as APIs da OpenAI (Whisper para transcrição, GPT-4V para visão, e o LLM para geração de respostas).
funcao_envio.py: Abstrai a comunicação com a API do Zapi para enviar mensagens de volta ao usuário.
Dicionários de Estado em Memória:
accumulated_messages: Armazena o contexto da conversa de cada usuário.
active_timers: Mantém referência aos timers ativos para poder cancelá-los.
processing_lock: Garante a integridade dos dados em operações concorrentes.
🚀 Como Funciona: O Fluxo de uma Conversa
Recepção: O endpoint /webhook recebe uma notificação da Z-API.
Processamento: O conteúdo é extraído. Se for uma mídia, é baixada e convertida para texto (transcrição ou descrição).
Acumulação Segura: Usando um lock, o sistema adiciona o novo texto ao buffer do usuário correspondente.
Gerenciamento do Timer: Qualquer timer anterior para aquele usuário é cancelado e um novo é iniciado. Este passo é crucial para garantir que o bot só responda após a última mensagem de uma sequência.
Expiração e Ação: Quando o usuário para de interagir, o timer expira. A função on_timer_expire é chamada.
Geração da Resposta: A mensagem consolidada é enviada para a função responder_usuario, onde a lógica de IA é aplicada para gerar uma resposta inteligente e contextual.
Envio: A resposta final é enviada ao usuário através da API do Zapi.
🛠️ Guia de Instalação e Configuração
Siga estes passos para colocar o chatbot em funcionamento.
✅ Pré-requisitos
Python 3.8 ou superior
Conta na plataforma Z-API com credenciais de API.
Chave de API da OpenAI.
ngrok (para exposição do webhook em ambiente de desenvolvimento).
⚙️ Passos de Instalação
Clone o repositório:
git clone <URL_DO_SEU_REPOSITORIO>
cd <NOME_DA_PASTA>
Use code with caution.
Bash
Crie e ative um ambiente virtual:
python3 -m venv venv
source venv/bin/activate  # No Windows: venv\Scripts\activate
Use code with caution.
Bash
Crie o arquivo requirements.txt:
flask
requests
openai
openai-whisper
python-dotenv
Use code with caution.
Txt
Instale as dependências:
pip install -r requirements.txt
Use code with caution.
Bash
🔑 Configurando o Ambiente
Por segurança e boas práticas, as credenciais devem ser gerenciadas através de variáveis de ambiente.
Crie um arquivo .env na raiz do projeto:
touch .env
Use code with caution.
Bash
Adicione suas credenciais ao arquivo .env:
# Credenciais da OpenAI
OPENAI_API_KEY="sk-..."

# Credenciais da Z-API (Exemplo - adapte conforme sua necessidade)
ZAPI_API_URL="https://api.z-api.io/instances/..."
ZAPI_TOKEN="SeuTokenAqui"
Use code with caution.
Env
Garanta que seu código carregue essas variáveis. No início do seu app.py, adicione:
from dotenv import load_dotenv
import os

load_dotenv() # Carrega as variáveis do arquivo .env

# Exemplo de como usar:
openai_key = os.getenv("OPENAI_API_KEY")
Use code with caution.
Python
▶️ Executando o Servidor
Inicie a aplicação Flask:
flask run --host=0.0.0.0 --port=5000
Use code with caution.
Bash
Ou, se estiver usando a estrutura if __name__ == '__main__':, execute:
python app.py
Use code with caution.
Bash
Exponha seu servidor local com o ngrok:
ngrok http 5000
Use code with caution.
Bash
O ngrok fornecerá uma URL pública no formato https://<hash-aleatorio>.ngrok.io.
Configure o Webhook na Z-API:
Vá ao painel da Z-API.
Na seção de webhooks, configure a URL de recebimento de mensagens para: https://<hash-aleatorio>.ngrok.io/webhook.
Seu chatbot agora está vivo e pronto para receber mensagens!
🎨 Customização e Extensibilidade
A verdadeira força deste projeto está em sua capacidade de adaptação.
🧠 Implementando a Lógica da IA
O coração da sua inteligência está na função responder_usuario. É aqui que você define a "personalidade" e a capacidade do seu bot.
Exemplo de implementação robusta:
def responder_usuario(mensagens_acumuladas_str, numero_telefone):
    """Gera e envia uma resposta baseada no contexto acumulado."""
    try:
        prompt = [
            {"role": "system", "content": "Você é o assistente virtual da nossa empresa. Seja amigável, profissional e ajude o cliente com suas dúvidas."},
            {"role": "user", "content": mensagens_acumuladas_str}
        ]
        
        # Chama a função que consulta a API da OpenAI
        resposta_ia = gerar_resposta_chatgpt(prompt)

        if resposta_ia:
            enviar_mensagem_zapi_com_delaytyping(
                telefone=numero_telefone,
                mensagem=resposta_ia,
                tempo_digitando_segundos=3
            )
    except Exception as e:
        print(f"ERRO CRÍTICO ao processar IA para {numero_telefone}: {e}")
        # Enviar mensagem de fallback para o usuário
        enviar_mensagem_zapi_com_delaytyping(
            telefone=numero_telefone,
            mensagem="Desculpe, nosso sistema está enfrentando uma instabilidade. Por favor, tente novamente em alguns instantes."
        )
Use code with caution.
Python
🔌 Adaptando para Outras Plataformas
Para migrar para o Telegram, por exemplo, você precisaria de apenas duas mudanças:
Recepção (webhook_receiver): Modificar a extração de dados para se adequar ao JSON do Telegram (ex: message['chat']['id'] em vez de phone).
Envio (responder_usuario): Chamar uma nova função enviar_mensagem_telegram() em vez da função do Zapi.
A lógica de acumulação, timers e concorrência permanece 100% reutilizável.
📈 Melhorias Futuras
Este projeto é uma base sólida. Aqui estão algumas ideias para evoluí-lo:
Persistência de Dados: Migrar os dicionários em memória para um banco de dados como Redis para persistir as conversas entre reinicializações do servidor.
Gerenciamento de Histórico: Armazenar conversas passadas em um banco de dados para fornecer um contexto ainda mais longo à IA.
Filas de Processamento: Para um alto volume de mensagens, implementar uma fila (como RabbitMQ ou Celery) para processar as chamadas de IA de forma assíncrona.
Análise de Sentimentos: Analisar o tom do usuário para adaptar as respostas do bot.
Dashboard de Monitoramento: Criar uma interface web simples para visualizar conversas em tempo real e monitorar a saúde do sistema.
📜 Licença
Este projeto está sob a licença MIT. Veja o arquivo LICENSE para mais detalhes.
