import tkinter as tk
from tkinter import ttk, messagebox
from controllers import StudioController
import re

class StudioBeautyApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Studio Beauty Manager")
        self.root.geometry("800x600")

        # Inicializa o Controller
        self.controller = StudioController()

        # Configuração do Notebook (Abas)
        self.notebook = ttk.Notebook(root)
        self.notebook.pack(expand=True, fill='both', padx=10, pady=10)

        # Criando abas
        self.tab_agendar = ttk.Frame(self.notebook)
        self.tab_visualizar = ttk.Frame(self.notebook)

        self.notebook.add(self.tab_agendar, text='Agendar')
        self.notebook.add(self.tab_visualizar, text='Visualizar')

        # Inicializando conteúdo das abas
        self.setup_tab_agendar()
        self.setup_tab_visualizar()

        # Carregar dados iniciais
        self.carregar_combos()
        self.carregar_agendamentos()

        # Bind para atualizar lista ao mudar de aba
        self.notebook.bind("<<NotebookTabChanged>>", lambda e: self.carregar_agendamentos())

    def setup_tab_agendar(self):
        # Frame Principal de Agendamento
        frame = ttk.LabelFrame(self.tab_agendar, text="Novo Agendamento", padding=20)
        frame.pack(padx=20, pady=20, fill="both", expand=True)

        # Grid Configuration
        frame.columnconfigure(1, weight=1)

        # Campos
        ttk.Label(frame, text="Cliente (Nome):").grid(row=0, column=0, sticky="w", pady=5)
        self.entry_cliente = ttk.Entry(frame)
        self.entry_cliente.grid(row=0, column=1, sticky="ew", pady=5) # Placeholder sem funcionalidade real de cliente por enquanto

        ttk.Label(frame, text="Profissional:").grid(row=1, column=0, sticky="w", pady=5)
        self.combo_profissional = ttk.Combobox(frame, state="readonly")
        self.combo_profissional.grid(row=1, column=1, sticky="ew", pady=5)

        ttk.Label(frame, text="Serviço:").grid(row=2, column=0, sticky="w", pady=5)
        self.combo_servico = ttk.Combobox(frame, state="readonly")
        self.combo_servico.grid(row=2, column=1, sticky="ew", pady=5)

        ttk.Label(frame, text="Data (YYYY-MM-DD):").grid(row=3, column=0, sticky="w", pady=5)
        self.entry_data = ttk.Entry(frame)
        self.entry_data.grid(row=3, column=1, sticky="ew", pady=5)

        ttk.Label(frame, text="Hora Início (HH:MM):").grid(row=4, column=0, sticky="w", pady=5)
        self.entry_hora = ttk.Entry(frame)
        self.entry_hora.grid(row=4, column=1, sticky="ew", pady=5)

        ttk.Button(frame, text="Salvar Agendamento", command=self.salvar_agendamento).grid(row=5, column=0, columnspan=2, pady=20)

        # Dicts para mapear Nomes -> IDs
        self.map_profissionais = {}
        self.map_servicos = {}

    def setup_tab_visualizar(self):
        # Frame de Visualização
        frame = ttk.Frame(self.tab_visualizar, padding=10)
        frame.pack(fill="both", expand=True)

        # Treeview
        columns = ('id', 'profissional', 'servico', 'data', 'inicio', 'fim')
        self.tree = ttk.Treeview(frame, columns=columns, show='headings')

        self.tree.heading('id', text='ID')
        self.tree.heading('profissional', text='Profissional')
        self.tree.heading('servico', text='Serviço')
        self.tree.heading('data', text='Data')
        self.tree.heading('inicio', text='Início')
        self.tree.heading('fim', text='Fim')

        self.tree.column('id', width=30)
        self.tree.column('profissional', width=150)
        self.tree.column('servico', width=150)
        self.tree.column('data', width=100)
        self.tree.column('inicio', width=80)
        self.tree.column('fim', width=80)

        # Scrollbar
        scrollbar = ttk.Scrollbar(frame, orient=tk.VERTICAL, command=self.tree.yview)
        self.tree.configure(yscroll=scrollbar.set)

        self.tree.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)

        ttk.Button(frame, text="Atualizar Lista", command=self.carregar_agendamentos).pack(pady=5)

    def carregar_combos(self):
        # Carregar Profissionais
        profs = self.controller.listar_profissionais()
        prof_names = []
        for p in profs:
            # p = (id, nome, especialidade, comissao)
            name_display = f"{p[1]} - {p[2]}"
            prof_names.append(name_display)
            self.map_profissionais[name_display] = p[0]
        self.combo_profissional['values'] = prof_names

        # Carregar Serviços
        servs = self.controller.listar_servicos()
        serv_names = []
        for s in servs:
            # s = (id, nome, preco, duracao)
            name_display = f"{s[1]} - R${s[2]} ({s[3]}min)"
            serv_names.append(name_display)
            self.map_servicos[name_display] = s[0]
        self.combo_servico['values'] = serv_names

    def carregar_agendamentos(self):
        # Limpar Treeview
        for item in self.tree.get_children():
            self.tree.delete(item)

        try:
            agendamentos = self.controller.listar_agendamentos()
            for ag in agendamentos:
                self.tree.insert('', tk.END, values=ag)
        except AttributeError:
            pass # Caso o controller ainda não tenha o método (previne crash se rodar sem update)

    def salvar_agendamento(self):
        try:
            # Coleta dados
            prof_name = self.combo_profissional.get()
            serv_name = self.combo_servico.get()
            data = self.entry_data.get()
            hora = self.entry_hora.get()

            # Validação Simples
            if not all([prof_name, serv_name, data, hora]):
                messagebox.showwarning("Aviso", "Preencha todos os campos!")
                return

            # Regex Data e Hora
            if not re.match(r"\d{4}-\d{2}-\d{2}", data):
                messagebox.showerror("Erro", "Formato de Data Inválido! Use YYYY-MM-DD")
                return
            if not re.match(r"\d{2}:\d{2}", hora):
                messagebox.showerror("Erro", "Formato de Hora Inválido! Use HH:MM")
                return

            # Obter IDs
            id_prof = self.map_profissionais.get(prof_name)
            id_servico = self.map_servicos.get(serv_name)

            # Chamar Controller
            sucesso, msg = self.controller.salvar_novo_agendamento(id_prof, id_servico, data, hora)

            if sucesso:
                messagebox.showinfo("Sucesso", msg)
                self.entry_data.delete(0, tk.END)
                self.entry_hora.delete(0, tk.END)
                self.carregar_agendamentos()
            else:
                messagebox.showerror("Erro", msg)

        except Exception as e:
            messagebox.showerror("Erro Crítico", f"Ocorreu um erro: {e}")

if __name__ == "__main__":
    root = tk.Tk()

    # Configuração de Estilo (Opcional)
    style = ttk.Style()
    style.theme_use('clam')

    app = StudioBeautyApp(root)
    root.mainloop()
