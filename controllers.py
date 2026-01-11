from database import DatabaseManager
from datetime import datetime, timedelta

class StudioController:
    def __init__(self):
        self.db = DatabaseManager()

    def listar_profissionais(self):
        """Retorna uma lista de todos os profissionais cadastrados."""
        self.db.cursor.execute("SELECT id, nome, especialidade, comissao FROM profissionais")
        return self.db.cursor.fetchall()

    def listar_servicos(self):
        """Retorna uma lista de todos os serviços cadastrados."""
        self.db.cursor.execute("SELECT id, nome, preco, duracao FROM servicos")
        return self.db.cursor.fetchall()

    def calcular_fim_servico(self, inicio_str, id_servico):
        """
        Calcula o horário de término com base no início e duração do serviço.
        :param inicio_str: Horário de início no formato 'HH:MM'
        :param id_servico: ID do serviço para buscar a duração
        :return: String do horário de término 'HH:MM' ou None se erro
        """
        try:
            self.db.cursor.execute("SELECT duracao FROM servicos WHERE id = ?", (id_servico,))
            resultado = self.db.cursor.fetchone()

            if not resultado:
                return None

            duracao_minutos = resultado[0]

            # Converte string para objeto datetime para somar minutos
            formato = "%H:%M"
            inicio_dt = datetime.strptime(inicio_str, formato)
            fim_dt = inicio_dt + timedelta(minutos=duracao_minutos)

            return fim_dt.strftime(formato)
        except Exception as e:
            print(f"Erro ao calcular fim do serviço: {e}")
            return None

    def validar_agendamento(self, id_prof, data, inicio, fim):
        """
        Verifica se existe conflito de horário para o profissional na data especificada.
        :return: False se houver conflito (inválido), True se livre (válido).
        """
        try:
            # Query para buscar conflitos
            # Um conflito ocorre se o novo agendamento começar antes de um existente terminar
            # E terminar depois de um existente começar.
            # (StartA < EndB) and (EndA > StartB)
            query = """
                SELECT id FROM agendamentos
                WHERE fk_profissional = ?
                AND data = ?
                AND (hora_inicio < ? AND hora_fim > ?)
            """
            self.db.cursor.execute(query, (id_prof, data, fim, inicio))
            conflitos = self.db.cursor.fetchall()

            if conflitos:
                return False # Com conflito
            return True # Sem conflito
        except Exception as e:
            print(f"Erro na validação: {e}")
            return False

    def salvar_novo_agendamento(self, id_prof, id_servico, data, inicio):
        """
        Tenta salvar um novo agendamento após validar.
        :return: (Sucesso: bool, Mensagem: str)
        """
        fim = self.calcular_fim_servico(inicio, id_servico)
        if not fim:
            return False, "Erro ao calcular duração do serviço."

        if not self.validar_agendamento(id_prof, data, inicio, fim):
            return False, "Horário indisponível para este profissional."

        try:
            self.db.cursor.execute("""
                INSERT INTO agendamentos (fk_profissional, fk_servico, data, hora_inicio, hora_fim)
                VALUES (?, ?, ?, ?, ?)
            """, (id_prof, id_servico, data, inicio, fim))
            self.db.conn.commit()
            return True, "Agendamento realizado com sucesso!"
        except Exception as e:
            return False, f"Erro ao salvar no banco: {e}"

    def close(self):
        self.db.close()
