import sqlite3 as sql
import pandas as pd # Usaremos pandas para exibir os dados de forma mais clara
from typing import Union, Any # Importar Union e Any

# --- Configurações Globais ---
NOME_BD = 'conversas_completas.db'
NOME_TABELA = 'historico_conversas'

# Definindo as colunas para fácil acesso e validação
COLUNAS = [
    "numero_telefone",  # PRIMARY KEY
    "hist_mensagem_bot_principal",
    "hist_mensagem_juiz_1",
    "hist_mensagem_juiz_2",
    "hist_mensagem_juiz_3",
    "hist_mensagem_juiz_4",
    "hist_mensagem_juiz_5",
    "hist_mensagem_avaliador_1",
    "hist_mensagem_avaliador_2",
    "hist_mensagem_avaliador_3",
    "hist_mensagem_avaliador_4",
    "hist_mensagem_avaliador_5",
    "imagens_disponiveis_para_envio",
    "audio_disponivel_para_envio",
    "video_disponivel_para_envio",
    "user_bloqueado"
]

# --- Funções Principais do Banco de Dados ---

def criar_tabela_conversas():
    """Cria a tabela no banco de dados se ela não existir."""
    conexao = None
    try:
        conexao = sql.connect(NOME_BD)
        cursor = conexao.cursor()

        # A primeira coluna é a chave primária
        defs_colunas = [f"{COLUNAS[0]} TEXT PRIMARY KEY NOT NULL"]
        # As demais colunas
        for coluna in COLUNAS[1:]:
            # Definimos todas as novas colunas como TEXT, permitindo NULL por padrão
            defs_colunas.append(f"{coluna} TEXT")

        sql_create_table = f'''
            CREATE TABLE IF NOT EXISTS {NOME_TABELA} (
                {", ".join(defs_colunas)}
            );
        '''
        cursor.execute(sql_create_table)

        # --- Lógica para adicionar a nova coluna se a tabela já existir ---
        # Isso é útil se você estiver rodando o script em um banco de dados existente
        # que foi criado antes da adição da coluna 'user_bloqueado'.
        if "user_bloqueado" in COLUNAS: # Verificação redundante, mas explícita
            try:
                cursor.execute(f"ALTER TABLE {NOME_TABELA} ADD COLUMN user_bloqueado TEXT")
                print(f"Coluna 'user_bloqueado' adicionada à tabela '{NOME_TABELA}' (se não existia).")
            except sql.OperationalError as e:
                # sqlite3.OperationalError: duplicate column name: user_bloqueado
                # Isso é esperado se a coluna já existe, então podemos ignorar ou logar.
                if "duplicate column name" in str(e).lower():
                    # print(f"Coluna 'user_bloqueado' já existe na tabela '{NOME_TABELA}'.")
                    pass # Coluna já existe, tudo bem.
                else:
                    raise # Outro OperationalError, melhor levantar.
        # --------------------------------------------------------------------

        conexao.commit()
        print(f"Tabela '{NOME_TABELA}' verificada/criada/atualizada com sucesso em '{NOME_BD}'.")
    except sql.Error as e:
        print(f"Erro ao criar/atualizar tabela: {e}")
    finally:
        if conexao:
            conexao.close()

def adicionar_conversa_inicial(
    numero_telefone: str,
    hist_bot_principal: str = None,
    hist_juiz_1: str = None, hist_juiz_2: str = None, hist_juiz_3: str = None,
    hist_juiz_4: str = None, hist_juiz_5: str = None,
    hist_avaliador_1: str = None, hist_avaliador_2: str = None, hist_avaliador_3: str = None,
    hist_avaliador_4: str = None, hist_avaliador_5: str = None,
    imagens_envio: str = None, audio_envio: str = None, video_envio: str = None,
    user_bloqueado: str = None  # NOVO PARÂMETRO
) -> bool:
    """
    Adiciona um novo registro de conversa.
    O 'numero_telefone' é obrigatório. Outros campos são opcionais.
    Retorna True se bem-sucedido, False caso contrário.
    """
    if not numero_telefone:
        print("Erro: 'numero_telefone' é obrigatório para adicionar uma nova conversa.")
        return False

    conexao = None
    try:
        conexao = sql.connect(NOME_BD)
        cursor = conexao.cursor()

        placeholders = ", ".join(["?"] * len(COLUNAS)) # Isso se ajusta automaticamente
        colunas_str = ", ".join(COLUNAS) # Isso se ajusta automaticamente
        sql_insert = f"INSERT INTO {NOME_TABELA} ({colunas_str}) VALUES ({placeholders})"

        dados_para_inserir = (
            numero_telefone, hist_bot_principal,
            hist_juiz_1, hist_juiz_2, hist_juiz_3, hist_juiz_4, hist_juiz_5,
            hist_avaliador_1, hist_avaliador_2, hist_avaliador_3, hist_avaliador_4, hist_avaliador_5,
            imagens_envio, audio_envio, video_envio,
            user_bloqueado  # NOVO DADO
        )

        cursor.execute(sql_insert, dados_para_inserir)
        conexao.commit()
        print(f"Dados para '{numero_telefone}' adicionados com sucesso (user_bloqueado='{user_bloqueado}').")
        return True
    except sql.IntegrityError:
        print(f"Erro: Já existe um registro para o número de telefone '{numero_telefone}'. Use a função de alteração.")
        return False
    except sql.Error as e:
        print(f"Erro ao adicionar dados para '{numero_telefone}': {e}")
        return False
    finally:
        if conexao:
            conexao.close()

def requisitar_dados_conversa(numero_telefone: str) -> Union[tuple, None]:
    """
    Requisita (busca) todos os dados de uma conversa específica pelo número de telefone.
    Retorna uma tupla com os dados ou None se não encontrado.
    A tupla retornada agora incluirá o valor da coluna 'user_bloqueado'.
    """
    if not numero_telefone:
        print("Erro: 'numero_telefone' é obrigatório para requisitar dados.")
        return None
    conexao = None
    try:
        conexao = sql.connect(NOME_BD)
        cursor = conexao.cursor()
        # SELECT * já incluirá a nova coluna automaticamente
        cursor.execute(f"SELECT * FROM {NOME_TABELA} WHERE numero_telefone = ?", (numero_telefone,))
        dados = cursor.fetchone()
        if dados:
            return dados
        else:
            print(f"Nenhum dado encontrado para o número de telefone '{numero_telefone}'.")
            return None
    except sql.Error as e:
        print(f"Erro ao requisitar dados para '{numero_telefone}': {e}")
        return None
    finally:
        if conexao:
            conexao.close()

def requisitar_valor_especifico(numero_telefone: str, nome_coluna: str) -> Union[Any, None]:
    """
    Requisita (busca) o valor de uma coluna específica para um dado número de telefone.
    Retorna o valor da célula ou None se não encontrado/erro.
    Agora pode ser usado para buscar 'user_bloqueado'.
    """
    if not numero_telefone or not nome_coluna:
        print("Erro: 'numero_telefone' e 'nome_coluna' são obrigatórios.")
        return None
    if nome_coluna not in COLUNAS: # A lista COLUNAS já está atualizada
        print(f"Erro: Nome da coluna '{nome_coluna}' inválido. Colunas válidas: {COLUNAS}")
        return None

    conexao = None
    try:
        conexao = sql.connect(NOME_BD)
        cursor = conexao.cursor()
        cursor.execute(f"SELECT {nome_coluna} FROM {NOME_TABELA} WHERE numero_telefone = ?", (numero_telefone,))
        resultado = cursor.fetchone()
        if resultado:
            return resultado[0]
        else:
            return None
    except sql.Error as e:
        print(f"Erro ao requisitar valor específico para '{numero_telefone}', coluna '{nome_coluna}': {e}")
        return None
    finally:
        if conexao:
            conexao.close()

def alterar_dado_especifico(numero_telefone: str, nome_coluna: str, novo_valor: Any) -> bool:
    """
    Altera o valor de uma coluna específica para um dado número de telefone (ID).
    Retorna True se bem-sucedido, False caso contrário.
    Agora pode ser usado para alterar 'user_bloqueado'.
    """
    if not numero_telefone or not nome_coluna:
        print("Erro: 'numero_telefone' e 'nome_coluna' são obrigatórios para alteração.")
        return False
    if nome_coluna == "numero_telefone":
        print("Erro: A coluna 'numero_telefone' (ID) não pode ser alterada diretamente por esta função.")
        return False
    if nome_coluna not in COLUNAS: # A lista COLUNAS já está atualizada
        print(f"Erro: Nome da coluna '{nome_coluna}' inválido. Colunas válidas: {COLUNAS[1:]}")
        return False

    conexao = None
    try:
        conexao = sql.connect(NOME_BD)
        cursor = conexao.cursor()

        sql_update = f"UPDATE {NOME_TABELA} SET {nome_coluna} = ? WHERE numero_telefone = ?"
        cursor.execute(sql_update, (novo_valor, numero_telefone))

        if cursor.rowcount == 0:
            print(f"Nenhum registro encontrado para o número de telefone '{numero_telefone}'. Nada foi alterado.")
            return False
        else:
            conexao.commit()
            print(f"Dado da coluna '{nome_coluna}' para '{numero_telefone}' alterado para '{novo_valor}' com sucesso.")
            return True
    except sql.Error as e:
        print(f"Erro ao alterar dado para '{numero_telefone}', coluna '{nome_coluna}': {e}")
        if conexao:
            conexao.rollback()
        return False
    finally:
        if conexao:
            conexao.close()

def mostrar_todos_os_dados():
    """Mostra todos os dados da tabela usando Pandas para melhor visualização."""
    conexao = None
    try:
        conexao = sql.connect(NOME_BD)
        # SELECT * e Pandas já incluirão a nova coluna automaticamente
        df = pd.read_sql_query(f"SELECT * FROM {NOME_TABELA}", conexao)
        if df.empty:
            print(f"A tabela '{NOME_TABELA}' está vazia.")
        else:
            print(f"\n--- Dados da Tabela: {NOME_TABELA} ---")
            print(df.to_string()) # to_string() mostra todas as colunas
            print("--- Fim dos Dados ---")
    except sql.Error as e:
        print(f"Erro ao buscar todos os dados: {e}")
    except Exception as e_pd:
        print(f"Erro ao exibir dados com pandas: {e_pd}")
    finally:
        if conexao:
            conexao.close()

# --- Exemplo de Uso ---
if __name__ == "__main__":
    # 1. Criar/atualizar a tabela
    # A função criar_tabela_conversas agora também tenta adicionar a coluna se necessário.
    criar_tabela_conversas()

    # 2. Adicionar dados iniciais (Função de adição/envio de dados)
    print("\n--- ADICIONANDO DADOS ---")
    adicionar_conversa_inicial(
        numero_telefone="5511987654321",
        hist_bot_principal="Olá! Como vai?",
        hist_juiz_1="Processo 123: Análise inicial.",
        imagens_envio="imagem_selfie.jpg,imagem_paisagem.png",
        user_bloqueado="nao" # Fornecendo valor para a nova coluna
    )
    adicionar_conversa_inicial(
        numero_telefone="5521912345678", # Número corrigido para ser único
        hist_bot_principal="Oi, tudo bem por aí?",
        hist_avaliador_3="Avaliação do projeto X: Pendente.",
        hist_avaliador_1='não',
        user_bloqueado="sim"  # Este usuário está bloqueado
    )
    adicionar_conversa_inicial(
        numero_telefone="5531999990000",
        user_bloqueado=None # Pode ser None, resultará em NULL no banco
    )

    # 3. Requisitar dados de uma conversa específica (Função de requisição de dados)
    print("\n--- REQUISITANDO DADOS COMPLETOS ---")
    dados_cliente1 = requisitar_dados_conversa("5511987654321")
    if dados_cliente1:
        print("Dados recuperados para 5511987654321:")
        # zip agora funcionará corretamente com a lista COLUNAS atualizada
        for nome_coluna, valor in zip(COLUNAS, dados_cliente1):
            print(f"  {nome_coluna}: {valor}")

    # 4. Requisitar valor de uma coluna específica, incluindo a nova
    print("\n--- REQUISITANDO VALOR ESPECÍFICO ---")
    status_bloqueio_cliente1 = requisitar_valor_especifico("5511987654321", "user_bloqueado")
    if status_bloqueio_cliente1 is not None:
        print(f"Status de bloqueio para 5511987654321: {status_bloqueio_cliente1}")
    else:
        print(f"Status de bloqueio para 5511987654321 não definido ou é NULL.")

    status_bloqueio_cliente2 = requisitar_valor_especifico("5521912345678", "user_bloqueado")
    if status_bloqueio_cliente2 is not None:
        print(f"Status de bloqueio para 5521912345678: {status_bloqueio_cliente2}")


    # 5. Alterar dados (Função de alteração de dados), incluindo a nova coluna
    print("\n--- ALTERANDO DADOS ---")
    alterar_dado_especifico(
        numero_telefone="5511987654321",
        nome_coluna="user_bloqueado",
        novo_valor="sim" # Bloqueando o usuário
    )
    alterar_dado_especifico(
        numero_telefone="5531999990000",
        nome_coluna="user_bloqueado",
        novo_valor="nao"
    )

    # 6. Mostrar todos os dados da tabela para verificação final
    # A nova coluna 'user_bloqueado' aparecerá.
    mostrar_todos_os_dados()

    print("\n--- VERIFICANDO STATUS DE BLOQUEIO APÓS ALTERAÇÃO ---")
    status_bloqueio_cliente1_apos = requisitar_valor_especifico("5511987654321", "user_bloqueado")
    print(f"Novo status de bloqueio para 5511987654321: {status_bloqueio_cliente1_apos}")