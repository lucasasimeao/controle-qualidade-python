import sqlite3
from contextlib import contextmanager

DB_PATH = 'producao_industrial.db'
PECAS_POR_CAIXA = 10

# --- CAMADA DE DADOS (SQLite) ---
@contextmanager
def conectar():
    """Abre a conexão, faz commit (ou rollback em erro) e sempre fecha."""
    conn = sqlite3.connect(DB_PATH)
    try:
        with conn:
            yield conn
    finally:
        conn.close()

def iniciar_db():
    with conectar() as conn:
        conn.execute('''
            CREATE TABLE IF NOT EXISTS pecas (
                id TEXT PRIMARY KEY,
                peso REAL,
                cor TEXT,
                comprimento REAL,
                status TEXT,
                motivo TEXT
            )
        ''')

def salvar_peca(peca):
    """Salva a peça. Retorna False se já existir uma peça com o mesmo ID."""
    try:
        with conectar() as conn:
            conn.execute('INSERT INTO pecas VALUES (?, ?, ?, ?, ?, ?)',
                         (peca['id'], peca['peso'], peca['cor'], peca['comprimento'], peca['status'], peca.get('motivo', '')))
        return True
    except sqlite3.IntegrityError:
        return False

def excluir_peca(id_peca):
    """Remove a peça. Retorna True se alguma linha foi apagada."""
    with conectar() as conn:
        cursor = conn.execute('DELETE FROM pecas WHERE id = ?', (id_peca,))
        return cursor.rowcount > 0

def buscar_pecas():
    with conectar() as conn:
        return conn.execute('SELECT id, peso, cor, comprimento, status, motivo FROM pecas').fetchall()

def calcular_indicadores():
    with conectar() as conn:
        aprovadas = conn.execute("SELECT COUNT(*) FROM pecas WHERE status = 'Aprovada'").fetchone()[0]
        reprovadas = conn.execute("SELECT COUNT(*) FROM pecas WHERE status = 'Reprovada'").fetchone()[0]
        motivos = conn.execute("SELECT id, motivo FROM pecas WHERE status = 'Reprovada'").fetchall()

    total = aprovadas + reprovadas
    return {
        'aprovadas': aprovadas,
        'reprovadas': reprovadas,
        'taxa_aprovacao': (aprovadas / total * 100) if total else 0.0,
        'caixas_fechadas': aprovadas // PECAS_POR_CAIXA,
        'pecas_na_caixa_atual': aprovadas % PECAS_POR_CAIXA,
        'motivos': motivos,
    }

# --- LÓGICA DO SISTEMA ---

def validar_peca(peso, cor, comprimento):
    erros = []
    if not (95 <= peso <= 105):
        erros.append("Peso fora (95g-105g)")
    if cor.lower() not in ['azul', 'verde']:
        erros.append("Cor inválida (Azul/Verde)")
    if not (10 <= comprimento <= 20):
        erros.append("Comprimento fora (10cm-20cm)")
    return erros

def montar_peca(id_p, peso, cor, comprimento):
    lista_erros = validar_peca(peso, cor, comprimento)
    return {
        "id": id_p, "peso": peso, "cor": cor.lower(),
        "comprimento": comprimento,
        "status": "Aprovada" if not lista_erros else "Reprovada",
        "motivo": " | ".join(lista_erros),
    }

def cadastrar_peca():
    print("\n[ NOVO CADASTRO ]")
    id_p = input("ID da Peça: ").strip()
    if not id_p:
        print("⚠️ Erro: o ID não pode ficar vazio.")
        return

    try:
        peso = float(input("Peso (g): ").replace(',', '.'))
        cor = input("Cor (Azul/Verde): ").strip()
        comp = float(input("Comprimento (cm): ").replace(',', '.'))
    except ValueError:
        print("⚠️ Erro: Insira apenas números para peso e comprimento.")
        return

    peca = montar_peca(id_p, peso, cor, comp)

    if not salvar_peca(peca):
        print(f"⚠️ Já existe uma peça com o ID {id_p}. Use outro ID.")
    elif peca["status"] == "Aprovada":
        print(f"✅ Peça {id_p} cadastrada e APROVADA!")
    else:
        print(f"❌ Peça {id_p} REPROVADA: {peca['motivo']}")

def listar_pecas():
    dados = buscar_pecas()

    print("\n--- LISTA GERAL DE PEÇAS ---")
    if not dados:
        print("Nenhuma peça cadastrada.")
    for d in dados:
        print(f"ID: {d[0]} | Status: {d[4]} | Detalhe: {d[5]}")

def gerar_relatorio():
    ind = calcular_indicadores()

    print("\n" + "="*35)
    print("      RELATÓRIO CONSOLIDADO")
    print("="*35)
    print(f"Total de Peças Aprovadas:   {ind['aprovadas']}")
    print(f"Total de Peças Reprovadas:  {ind['reprovadas']}")
    print(f"Taxa de Aprovação:          {ind['taxa_aprovacao']:.1f}%")
    print(f"Caixas Fechadas (Full):     {ind['caixas_fechadas']}")
    print(f"Peças na Caixa Atual:       {ind['pecas_na_caixa_atual']}/{PECAS_POR_CAIXA}")

    if ind['motivos']:
        print("\nMotivos de Reprovação:")
        for id_peca, motivo in ind['motivos']:
            print(f"- Peça {id_peca}: {motivo}")
    print("="*35)

# --- INTERFACE DE USUÁRIO (MENU) ---

def menu():
    iniciar_db()
    while True:
        print("\n🏭 SISTEMA DE QUALIDADE INDUSTRIAL")
        print("1. Cadastrar nova peça")
        print("2. Listar peças cadastradas")
        print("3. Remover peça (ID)")
        print("4. Relatório final")
        print("0. Sair")

        opcao = input("\nEscolha uma opção: ")

        if opcao == '1':
            cadastrar_peca()
        elif opcao == '2':
            listar_pecas()
        elif opcao == '3':
            id_rem = input("Digite o ID da peça para remover: ").strip()
            if excluir_peca(id_rem):
                print(f"Peça {id_rem} removida.")
            else:
                print(f"Nenhuma peça encontrada com o ID {id_rem}.")
        elif opcao == '4':
            gerar_relatorio()
        elif opcao == '0':
            print("Encerrando sistema...")
            break
        else:
            print("Opção inválida!")

if __name__ == "__main__":
    menu()
