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
2.  [**Gerenciamento de Conversas: A Base de Dados de Brinde**](#-gerenciamento-de-conversas-a-base-de-dados-de-brinde)
3.  [**Arquitetura do Sistema**](#-arquitetura-do-sistema)
4.  [**Guia de Instalação e Configuração**](#-guia-de-instalação-e-configuração)
5.  [**Customização e Extensibilidade**](#-customização-e-extensibilidade)

---

## 🎯 Visão Geral

Este projeto implementa um serviço de backend para um chatbot de WhatsApp que se destaca por sua capacidade de **acumular mensagens de forma inteligente**. Em vez de responder reativamente a cada interação, o sistema aguarda uma pausa na conversa do usuário para consolidar múltiplas mensagens em um único prompt contextual.

O resultado é um chatbot que compreende o contexto completo da solicitação do usuário, permitindo que a IA gere respostas muito mais coesas, precisas e humanizadas.

---

## 🗄️ Gerenciamento de Conversas: A Base de Dados de Brinde

Para tornar o chatbot ainda mais poderoso, este projeto inclui um script bônus, **`gerar_base_dados.py`**, que implementa uma base de dados local simples. Ele foi projetado como um "brinde" para oferecer persistência de conversas sem a complexidade de um banco de dados externo.

### Como Funciona?

*   **Armazenamento Local:** O script utiliza um arquivo (geralmente JSON) para salvar o histórico de mensagens de cada usuário.
*   **Memória de Longo Prazo:** Com ele, o bot pode "lembrar" de interações passadas, não apenas das mensagens da sessão atual.
*   **Contexto Aprimorado:** Ao carregar o histórico antes de chamar a IA, as respostas se tornam drasticamente mais ricas e personalizadas.
*   **Fácil Implementação:** Não requer configuração de um banco de dados como MySQL ou Redis. Basta usar as funções de leitura e escrita do script na sua lógica principal.

---

## 🏗️ Arquitetura do Sistema

O sistema é construído sobre Python e Flask, com uma arquitetura focada em modularidade. Os componentes principais são:

*   **`app.py`:** O servidor Flask que recebe os webhooks e orquestra o fluxo.
*   **`funcoes_chatgpt.py`:** Módulo que interage com as APIs da OpenAI.
*   **`funcao_envio.py`:** Módulo que abstrai o envio de mensagens pela Z-API.
*   **`gerar_base_dados.py`:** Gerencia o histórico de conversas em um arquivo local.

---

## 🛠️ Guia de Instalação e Configuração

Siga estes passos para colocar o chatbot em funcionamento de forma rápida e correta.

### ✅ Pré-requisitos

*   Python 3.8 ou superior
*   Conta na plataforma **Z-API**
*   Chave de API da **OpenAI**

### ⚙️ Passos de Configuração

1.  **Instalar Dependências:** O projeto já vem com um arquivo `requirements.txt`. Para instalar tudo o que é necessário, basta executar no seu terminal:
    ```bash
    pip install -r requirements.txt
    ```

2.  **Configurar Chave do ChatGPT (OpenAI):**
    Crie um arquivo chamado `.env` na raiz do projeto. Dentro dele, coloque sua chave da API da OpenAI da seguinte forma:
    ```env
    OPENAI_API_KEY="sk-..."
    ```
    Isso mantém sua chave segura e fora do código-fonte.

3.  **Configurar Credenciais da Z-API:**
    As credenciais da Z-API (Token, Instance ID, etc.) devem ser inseridas **diretamente no arquivo `funcao_envio.py`**. Abra este arquivo e preencha as variáveis correspondentes no topo do script.

4.  **Executar o Servidor:**
    Inicie o servidor com `python app.py` e use uma ferramenta como o `ngrok` para criar uma URL pública (`ngrok http 5000`). Use essa URL no painel da Z-API.

---

## 🎨 Customização e Extensibilidade

A lógica central do seu bot reside na função `responder_usuario`. É aqui que você deve chamar as funções de `gerar_base_dados.py` para carregar o histórico e, em seguida, chamar a IA com o contexto completo. A arquitetura modular permite trocar facilmente qualquer componente.
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
