
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
```

### 🧩 Componentes Chave

*   **`app.py` (Servidor Flask):** O núcleo da aplicação. Recebe webhooks, gerencia o estado da aplicação (mensagens e timers) e orquestra todo o fluxo.
*   **`funcoes_chatgpt.py`:** Módulo responsável pela interação com as APIs da OpenAI (Whisper para transcrição, GPT-4V para visão, e o LLM para geração de respostas).
*   **`funcao_envio.py`:** Abstrai a comunicação com a API do Zapi para enviar mensagens de volta ao usuário.
*   **Dicionários de Estado em Memória:**
    *   `accumulated_messages`: Armazena o contexto da conversa de cada usuário.
    *   `active_timers`: Mantém referência aos timers ativos para poder cancelá-los.
    *   `processing_lock`: Garante a integridade dos dados em operações concorrentes.

---

## 🚀 Como Funciona: O Fluxo de uma Conversa

1.  **Recepção:** O endpoint `/webhook` recebe uma notificação da Z-API.
2.  **Processamento:** O conteúdo é extraído. Se for uma mídia, é baixada e convertida para texto (transcrição ou descrição).
3.  **Acumulação Segura:** Usando um `lock`, o sistema adiciona o novo texto ao buffer do usuário correspondente.
4.  **Gerenciamento do Timer:** Qualquer timer anterior para aquele usuário é **cancelado** e um novo é **iniciado**. Este passo é crucial para garantir que o bot só responda após a última mensagem de uma sequência.
5.  **Expiração e Ação:** Quando o usuário para de interagir, o timer expira e executa a função de callback `on_timer_expire`.
6.  **Chamada da Lógica Principal:** A função `on_timer_expire` consolida todas as mensagens acumuladas em uma única string e a passa para a função `responder_usuario`.
7.  **Geração e Envio da Resposta:** `responder_usuario` utiliza a string completa para interagir com a IA, gerar uma resposta coesa e, finalmente, chama a função `enviar_mensagem_zapi_com_delaytyping` para entregar a resposta ao usuário.

---

## 🛠️ Guia de Instalação e Configuração

### ✅ Pré-requisitos

*   Python 3.8+
*   Conta na plataforma Z-API com as credenciais.
*   Chave de API da OpenAI.

### ⚙️ Passos de Instalação

1.  **Clone o repositório.**
2.  **Crie e ative um ambiente virtual.**
3.  **Crie um arquivo `requirements.txt`:**
    ```txt
    flask
    requests
    openai
    openai-whisper
    python-dotenv
    ```
4.  **Instale as dependências:**
    ```bash
    pip install -r requirements.txt
    ```

### 🔑 Configurando o Ambiente

1.  **Crie um arquivo `.env`** com suas credenciais:
    ```env
    # Credenciais da OpenAI
    OPENAI_API_KEY="sk-..."

    # Credenciais da Z-API
    ZAPI_API_URL="https://api.z-api.io/instances/..."
    ZAPI_TOKEN="SeuTokenAqui"
    ```

---

## 🎨 Customização e Extensibilidade

A lógica central do seu bot está na função `responder_usuario`. Adapte-a para definir a personalidade e as capacidades de resposta. A arquitetura modular permite trocar a API de envio (Z-API) por qualquer outra (Telegram, etc.) com alterações mínimas.

---

## 📈 Melhorias Futuras

*   **Persistência de Dados:** Usar **Redis** para salvar o estado da conversa.
*   **Gerenciamento de Histórico:** Salvar conversas em um banco de dados para contextos mais longos.
*   **Filas de Processamento:** Usar **RabbitMQ** ou **Celery** para escalar o processamento de IA.
*   **Dashboard de Monitoramento:** Criar uma interface para visualizar logs e conversas.

---

## 📜 Licença

Este projeto está sob a licença MIT.
</code></pre>
        </div>
    </div>
    <script>
        document.querySelector('.copy-button').addEventListener('click', function() {
            const codeToCopy = document.getElementById('markdown-code').innerText;
            navigator.clipboard.writeText(codeToCopy).then(() => {
                this.innerText = 'Copiado!';
                this.style.backgroundColor = '#28a745'; // Green color for success
                setTimeout(() => {
                    this.innerText = 'Copiar Código';
                    this.style.backgroundColor = '#007bff'; // Revert to original color
                }, 2000);
            }).catch(err => {
                console.error('Falha ao copiar o texto: ', err);
                this.innerText = 'Erro!';
                this.style.backgroundColor = '#dc3545'; // Red color for error
                 setTimeout(() => {
                    this.innerText = 'Copiar Código';
                    this.style.backgroundColor = '#007bff';
                }, 2000);
            });
        });
    </script>
</body>
</html>
