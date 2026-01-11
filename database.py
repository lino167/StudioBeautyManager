import sqlite3
import os

class DatabaseManager:
    def __init__(self, db_name="studio_beauty.db"):
        self.db_name = db_name
        self.conn = None
        self.cursor = None
        self.connect()
        self.create_tables()
        self.seed_data()

    def connect(self):
        """Estabelece a conexão com o banco de dados"""
        try:
            self.conn = sqlite3.connect(self.db_name)
            self.cursor = self.conn.cursor()
            print(f"Conectado ao banco de dados: {self.db_name}")
        except sqlite3.Error as e:
            print(f"Erro ao conectar ao banco de dados: {e}")

    def create_tables(self):
        """Cria as tabelas necessárias se não existirem"""
        try:
            # Tabela de Profissionais
            self.cursor.execute("""
                CREATE TABLE IF NOT EXISTS profissionais (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    nome TEXT NOT NULL,
                    especialidade TEXT,
                    comissao REAL DEFAULT 0.0
                )
            """)

            # Tabela de Serviços
            self.cursor.execute("""
                CREATE TABLE IF NOT EXISTS servicos (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    nome TEXT NOT NULL,
                    preco REAL NOT NULL,
                    duracao INTEGER NOT NULL -- Duração em minutos
                )
            """)

            # Tabela de Agendamentos
            self.cursor.execute("""
                CREATE TABLE IF NOT EXISTS agendamentos (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    fk_profissional INTEGER NOT NULL,
                    fk_servico INTEGER NOT NULL,
                    data TEXT NOT NULL, -- Formato YYYY-MM-DD
                    hora_inicio TEXT NOT NULL, -- Formato HH:MM
                    hora_fim TEXT NOT NULL, -- Formato HH:MM
                    FOREIGN KEY (fk_profissional) REFERENCES profissionais (id),
                    FOREIGN KEY (fk_servico) REFERENCES servicos (id)
                )
            """)
            self.conn.commit()
            print("Tabelas verificadas/criadas com sucesso.")
        except sqlite3.Error as e:
            print(f"Erro ao criar tabelas: {e}")

    def seed_data(self):
        """Insere dados de teste se o banco estiver vazio"""
        try:
            # Verifica se já existem profissionais
            self.cursor.execute("SELECT COUNT(*) FROM profissionais")
            count = self.cursor.fetchone()[0]

            if count == 0:
                print("Banco vazio. Inserindo dados de teste...")

                # Inserindo Profissionais
                profissionais = [
                    ('Ana Silva', 'Cabelereira', 30.0),
                    ('Carlos Oliveira', 'Manicure', 40.0),
                    ('Mariana Souza', 'Esteticista', 35.0)
                ]
                self.cursor.executemany("""
                    INSERT INTO profissionais (nome, especialidade, comissao)
                    VALUES (?, ?, ?)
                """, profissionais)

                # Inserindo Serviços
                servicos = [
                    ('Corte Feminino', 80.00, 60),
                    ('Manicure Completa', 40.00, 45),
                    ('Limpeza de Pele', 120.00, 90),
                    ('Escova', 50.00, 40)
                ]
                self.cursor.executemany("""
                    INSERT INTO servicos (nome, preco, duracao)
                    VALUES (?, ?, ?)
                """, servicos)

                self.conn.commit()
                print("Dados de teste inseridos com sucesso!")
            else:
                print("Dados já existentes. Pulei a inserção de teste.")

        except sqlite3.Error as e:
            print(f"Erro ao inserir dados de teste: {e}")

    def close(self):
        """Fecha a conexão com o banco de dados"""
        if self.conn:
            self.conn.close()
            print("Conexão fechada.")

if __name__ == "__main__":
    db = DatabaseManager()
    db.close()
