<!DOCTYPE html>
<html lang="pt-br">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Documentação: Chatbot Inteligente com Acumulador de Mensagens</title>
    <style>
        body {
            font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, "Helvetica Neue", Arial, sans-serif;
            line-height: 1.7;
            color: #333;
            background-color: #f8f9fa;
            margin: 0;
            padding: 20px;
        }
        .container {
            max-width: 850px;
            margin: 20px auto;
            background-color: #ffffff;
            padding: 20px 40px;
            border-radius: 12px;
            box-shadow: 0 4px 15px rgba(0, 0, 0, 0.07);
        }
        h1, h2, h3 {
            font-weight: 700;
            color: #1d3557; /* Um azul escuro e forte */
            margin-top: 40px;
            margin-bottom: 20px;
            border-bottom: 2px solid #e9ecef;
            padding-bottom: 10px;
        }
        h1 {
            font-size: 2.5em;
            text-align: center;
            border-bottom: none;
            margin-top: 0;
        }
        h2 {
            font-size: 2em;
        }
        h3 {
            font-size: 1.5em;
        }
        a {
            color: #007bff;
            text-decoration: none;
            font-weight: 600;
        }
        a:hover {
            text-decoration: underline;
        }
        code {
            background-color: #e9ecef;
            padding: 3px 7px;
            border-radius: 5px;
            font-family: "SFMono-Regular", Consolas, "Liberation Mono", Menlo, Courier, monospace;
            font-size: 0.9em;
            color: #c7254e;
        }
        pre {
            background-color: #282c34;
            color: #abb2bf;
            padding: 20px;
            border-radius: 8px;
            overflow-x: auto;
            white-space: pre-wrap;
            word-wrap: break-word;
            font-family: "SFMono-Regular", Consolas, "Liberation Mono", Menlo, Courier, monospace;
        }
        pre code {
            background-color: transparent;
            padding: 0;
            color: inherit;
            font-size: 1em;
        }
        img {
            max-width: 100%;
            height: auto;
            display: block;
        }
        .center-div {
            text-align: center;
            margin-bottom: 20px;
        }
        ul, ol {
            padding-left: 25px;
        }
        li {
            margin-bottom: 12px;
        }
        hr {
            border: 0;
            height: 1px;
            background-color: #dee2e6;
            margin: 50px 0;
        }
        strong, b {
          color: #0056b3;
        }
        .badges p {
            margin: 10px 0;
            display: flex;
            gap: 10px;
            justify-content: center;
            flex-wrap: wrap;
        }
    </style>
</head>
<body>
    <div class="container">
        
        <div class="center-div">
            <a href="https://z-api.io/">
                <img src="https://z-api.io/wp-content/uploads/2023/04/Z-API.svg" alt="Z-API Logo" style="width: 200px; margin-bottom: 20px;"/>
            </a>
        </div>
        
        <h1>Chatbot Inteligente com Acumulador de Mensagens</h1>

        <p class="center-div">
            <strong>Um backend robusto para WhatsApp que agrupa mensagens de texto, áudio e imagem para gerar respostas de IA mais ricas e contextuais.</strong>
        </p>

        <div class="badges">
            <p>
                <img src="https://img.shields.io/badge/Python-3.8%2B-blue.svg" alt="Python Version">
                <img src="https://img.shields.io/badge/Framework-Flask-black.svg" alt="Flask Framework">
                <img src="https://img.shields.io/badge/Integração-Z--API-brightgreen.svg" alt="Z-API Integration">
                <img src="https://img.shields.io/badge/License-MIT-yellow.svg" alt="License">
            </p>
        </div>

        <hr>

        <h2>📋 Índice</h2>
        <ul>
            <li><a href="#visao-geral"><strong>Visão Geral</strong></a></li>
            <li><a href="#arquitetura"><strong>Arquitetura do Sistema</strong></a></li>
            <li><a href="#como-funciona"><strong>Como Funciona: O Fluxo de uma Conversa</strong></a></li>
            <li><a href="#instalacao"><strong>Guia de Instalação e Configuração</strong></a></li>
            <li><a href="#customizacao"><strong>Customização e Extensibilidade</strong></a></li>
            <li><a href="#melhorias"><strong>Melhorias Futuras</strong></a></li>
            <li><a href="#licenca"><strong>Licença</strong></a></li>
        </ul>

        <hr>

        <h2 id="visao-geral">🎯 Visão Geral</h2>
        <p>Este projeto implementa um serviço de backend para um chatbot de WhatsApp que se destaca por sua capacidade de <strong>acumular mensagens de forma inteligente</strong>. Em vez de responder reativamente a cada interação, o sistema aguarda uma pausa na conversa do usuário para consolidar múltiplas mensagens — incluindo texto, áudios transcritos e descrições de imagens — em um único prompt contextual.</p>
        <p>Este prompt unificado permite que modelos de linguagem (LLMs) como o GPT-4 gerem respostas muito mais coesas, precisas e humanizadas, transformando interações fragmentadas em um diálogo fluido.</p>
        
        <h3>🌟 Objetivo do Projeto</h3>
        <p>O principal objetivo é superar a limitação de chatbots tradicionais que processam cada mensagem isoladamente. Ao criar um "buffer de contexto", o bot pode entender a intenção completa do usuário, mesmo que ela seja expressa em várias partes, resultando em uma experiência de usuário drasticamente superior.</p>

        <h3>✨ Principais Funcionalidades</h3>
        <ul>
            <li><strong>Acumulador de Mensagens:</strong> Consolida mensagens enviadas em um curto intervalo de tempo.</li>
            <li><strong>Suporte Multimodal Completo:</strong>
                <ul>
                    <li>💬 <strong>Texto:</strong> Processa mensagens de texto padrão.</li>
                    <li>🎤 <strong>Áudio:</strong> Transcreve automaticamente mensagens de voz para texto usando <strong>OpenAI Whisper</strong>.</li>
                    <li>🖼️ <strong>Imagem:</strong> Gera descrições textuais de imagens enviadas usando <strong>GPT-4 Vision</strong>.</li>
                    <li>📹 <strong>Vídeo:</strong> Reconhece o recebimento de vídeos e captura suas legendas.</li>
                </ul>
            </li>
            <li><strong>Temporizador Dinâmico:</strong> Um temporizador reinicia a cada nova mensagem, acionando a resposta apenas quando o usuário faz uma pausa.</li>
            <li><strong>Arquitetura Flexível:</strong> Projetado para ser independente da API de envio, permitindo fácil adaptação a qualquer serviço de mensageria (Telegram, Messenger, etc.).</li>
            <li><strong>Segurança de Concorrência:</strong> Utiliza <code>threading.Lock</code> para garantir o processamento seguro e sem conflitos de mensagens de múltiplos usuários simultâneos.</li>
        </ul>

        <hr>

        <h2 id="arquitetura">🏗️ Arquitetura do Sistema</h2>
        <p>O sistema é construído sobre uma base de Python e Flask, com uma arquitetura simples, porém poderosa, focada em modularidade e performance.</p>

        <h3>🌊 Diagrama de Fluxo</h3>
        <pre><code>sequenceDiagram
    participant User as Usuário (WhatsApp)
    participant ZApi as Z-API
    participant Server as Servidor Flask
    participant AI as Lógica de IA (GPT)

    User->>ZApi: Envia Mensagem (Texto/Áudio/Imagem)
    ZApi->>Server: POST /webhook com dados da msg
    Server->>Server: Extrai conteúdo e identifica tipo
    Note right of Server: Se áudio, transcreve.<br>Se imagem, descreve.
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
    ZApi-->>User: Entrega a resposta do bot</code></pre>

        <h3>🧩 Componentes Chave</h3>
        <ul>
            <li><strong><code>app.py</code> (Servidor Flask):</strong> O núcleo da aplicação. Recebe webhooks, gerencia o estado da aplicação (mensagens e timers) e orquestra todo o fluxo.</li>
            <li><strong><code>funcoes_chatgpt.py</code>:</strong> Módulo responsável pela interação com as APIs da OpenAI (Whisper, GPT-4V, etc.).</li>
            <li><strong><code>funcao_envio.py</code>:</strong> Abstrai a comunicação com a API do Zapi para enviar mensagens.</li>
            <li><strong>Dicionários de Estado em Memória:</strong>
                <ul>
                    <li><code>accumulated_messages</code>: Armazena o contexto da conversa de cada usuário.</li>
                    <li><code>active_timers</code>: Mantém referência aos timers ativos para poder cancelá-los.</li>
                    <li><code>processing_lock</code>: Garante a integridade dos dados em operações concorrentes.</li>
                </ul>
            </li>
        </ul>

        <hr>

        <h2 id="como-funciona">🚀 Como Funciona: O Fluxo de uma Conversa</h2>
        <ol>
            <li><strong>Recepção:</strong> O endpoint <code>/webhook</code> recebe uma notificação da Z-API.</li>
            <li><strong>Processamento:</strong> O conteúdo é extraído. Se for uma mídia, é baixada e convertida para texto (transcrição ou descrição).</li>
            <li><strong>Acumulação Segura:</strong> Usando um <code>lock</code>, o sistema adiciona o novo texto ao buffer do usuário correspondente.</li>
            <li><strong>Gerenciamento do Timer:</strong> Qualquer timer anterior para aquele usuário é <strong>cancelado</strong> e um novo é <strong>iniciado</strong>. Este passo é crucial para garantir que o bot só responda após a última mensagem de uma sequência.</li>
            <li><strong>Expiração e Ação:</strong> Quando o usuário para de interagir, o timer expira. A função <code>on_timer_expire</code> é chamada.</li>
            <li><strong>Geração da Resposta:</strong> A mensagem consolidada é enviada para a função <code>responder_usuario</code>, onde a lógica de IA é aplicada.</li>
            <li><strong>Envio:</strong> A resposta final é enviada ao usuário através da API do Zapi.</li>
        </ol>

        <hr>

        <h2 id="instalacao">🛠️ Guia de Instalação e Configuração</h2>
        <p>Siga estes passos para colocar o chatbot em funcionamento.</p>

        <h3>✅ Pré-requisitos</h3>
        <ul>
            <li>Python 3.8 ou superior</li>
            <li>Conta na plataforma <strong>Z-API</strong> com credenciais de API.</li>
            <li>Chave de API da <strong>OpenAI</strong>.</li>
            <li><code>ngrok</code> (para exposição do webhook em ambiente de desenvolvimento).</li>
        </ul>

        <h3>⚙️ Passos de Instalação</h3>
        <ol>
            <li><strong>Clone o repositório:</strong>
                <pre><code>git clone <URL_DO_SEU_REPOSITORIO>
cd <NOME_DA_PASTA></code></pre>
            </li>
            <li><strong>Crie e ative um ambiente virtual:</strong>
                <pre><code>python3 -m venv venv
source venv/bin/activate  # No Windows: venv\Scripts\activate</code></pre>
            </li>
            <li><strong>Crie o arquivo <code>requirements.txt</code>:</strong>
                <pre><code>flask
requests
openai
openai-whisper
python-dotenv</code></pre>
            </li>
            <li><strong>Instale as dependências:</strong>
                <pre><code>pip install -r requirements.txt</code></pre>
            </li>
        </ol>

        <h3>🔑 Configurando o Ambiente</h3>
        <ol>
            <li><strong>Crie um arquivo <code>.env</code></strong> na raiz do projeto:
                <pre><code>touch .env</code></pre>
            </li>
            <li><strong>Adicione suas credenciais ao arquivo <code>.env</code>:</strong>
                <pre><code># Credenciais da OpenAI
OPENAI_API_KEY="sk-..."

# Credenciais da Z-API (Exemplo - adapte conforme sua necessidade)
ZAPI_API_URL="https://api.z-api.io/instances/..."
ZAPI_TOKEN="SeuTokenAqui"</code></pre>
            </li>
            <li><strong>Garanta que seu código carregue essas variáveis.</strong> No início do seu <code>app.py</code>, adicione:
                <pre><code class="language-python">from dotenv import load_dotenv
import os

load_dotenv() # Carrega as variáveis do arquivo .env

# Exemplo de como usar:
openai_key = os.getenv("OPENAI_API_KEY")</code></pre>
            </li>
        </ol>

        <h3>▶️ Executando o Servidor</h3>
        <ol>
            <li><strong>Inicie a aplicação Flask:</strong>
                <pre><code>python app.py</code></pre>
            </li>
            <li><strong>Exponha seu servidor local com o ngrok:</strong>
                <pre><code>ngrok http 5000</code></pre>
            </li>
            <li><strong>Configure o Webhook na Z-API:</strong> Use a URL pública fornecida pelo ngrok (ex: <code>https://<hash>.ngrok.io/webhook</code>) no seu painel da Z-API.</li>
        </ol>
        
        <hr>

        <h2 id="customizacao">🎨 Customização e Extensibilidade</h2>
        
        <h3>🧠 Implementando a Lógica da IA</h3>
        <p>O coração da sua inteligência está na função <code>responder_usuario</code>. É aqui que você define a "personalidade" e a capacidade do seu bot.</p>
        <pre><code class="language-python">def responder_usuario(mensagens_acumuladas_str, numero_telefone):
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
        )</code></pre>
        
        <h3>🔌 Adaptando para Outras Plataformas</h3>
        <p>A lógica de acumulação, timers e concorrência <strong>permanece 100% reutilizável</strong>. Para migrar para o Telegram, por exemplo, você só precisa alterar:</p>
        <ol>
            <li><strong>Recepção (<code>webhook_receiver</code>):</strong> Adaptar a extração de dados para o JSON do Telegram.</li>
            <li><strong>Envio (<code>responder_usuario</code>):</strong> Chamar uma função de envio específica para a API do Telegram.</li>
        </ol>

        <hr>

        <h2 id="melhorias">📈 Melhorias Futuras</h2>
        <ul>
            <li><strong>Persistência de Dados:</strong> Migrar os dicionários em memória para um banco de dados como <strong>Redis</strong> para persistir as conversas.</li>
            <li><strong>Gerenciamento de Histórico:</strong> Armazenar conversas passadas para fornecer um contexto ainda mais longo à IA.</li>
            <li><strong>Filas de Processamento:</strong> Para um alto volume, usar <strong>RabbitMQ</strong> ou <strong>Celery</strong> para processar as chamadas de IA de forma assíncrona.</li>
            <li><strong>Análise de Sentimentos:</strong> Analisar o tom do usuário para adaptar as respostas do bot.</li>
            <li><strong>Dashboard de Monitoramento:</strong> Criar uma interface web para visualizar conversas em tempo real.</li>
        </ul>

        <hr>

        <h2 id="licenca">📜 Licença</h2>
        <p>Este projeto está sob a licença MIT. Veja o arquivo <code>LICENSE</code> para mais detalhes.</p>
    </div>
</body>
</html>
