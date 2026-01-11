import customtkinter as ctk
from tkinter import messagebox
from controllers import StudioController
import re
from datetime import datetime

# Configuração Global do CustomTkinter
ctk.set_appearance_mode("System")  # Modes: "System" (standard), "Dark", "Light"
ctk.set_default_color_theme("blue")  # Themes: "blue" (standard), "green", "dark-blue"

class App(ctk.CTk):
    def __init__(self):
        super().__init__()

        # Configuração da Janela Principal
        self.title("Studio Beauty Manager")
        self.geometry("1100x700")

        # Controller
        self.controller = StudioController()

        # Layout de Grid Principal (2 colunas: Navigation Rail + Conteúdo)
        self.grid_columnconfigure(1, weight=1)
        self.grid_rowconfigure(0, weight=1)

        # 1. Navigation Rail (Menu Lateral)
        self.create_navigation_rail()

        # 2. Frames de Conteúdo (Paginas)
        self.home_frame = ctk.CTkFrame(self, corner_radius=0, fg_color="transparent")
        self.agenda_frame = ctk.CTkFrame(self, corner_radius=0, fg_color="transparent")
        self.clientes_frame = ctk.CTkFrame(self, corner_radius=0, fg_color="transparent")

        # Inicializa a Home (Agenda Dashboard)
        self.create_agenda_dashboard()


        # Seleciona a primeira rota
        self.select_frame_by_name("agenda")

    def create_navigation_rail(self):
        self.navigation_frame = ctk.CTkFrame(self, corner_radius=0, width=140)
        self.navigation_frame.grid(row=0, column=0, sticky="nsew")
        self.navigation_frame.grid_rowconfigure(4, weight=1)

        self.logo_label = ctk.CTkLabel(self.navigation_frame, text="Studio\nManager",
                                       font=ctk.CTkFont(size=20, weight="bold"))
        self.logo_label.grid(row=0, column=0, padx=20, pady=20)

        # Botões de Navegação
        self.btn_agenda = ctk.CTkButton(self.navigation_frame, corner_radius=0, height=40, border_spacing=10, text="Agenda",
                                        fg_color="transparent", text_color=("gray10", "gray90"), hover_color=("gray70", "gray30"),
                                        anchor="w", command=lambda: self.select_frame_by_name("agenda"))
        self.btn_agenda.grid(row=1, column=0, sticky="ew")

        self.btn_clientes = ctk.CTkButton(self.navigation_frame, corner_radius=0, height=40, border_spacing=10, text="Clientes",
                                          fg_color="transparent", text_color=("gray10", "gray90"), hover_color=("gray70", "gray30"),
                                          anchor="w", command=lambda: self.select_frame_by_name("clientes"))
        self.btn_clientes.grid(row=2, column=0, sticky="ew")

        self.btn_financeiro = ctk.CTkButton(self.navigation_frame, corner_radius=0, height=40, border_spacing=10, text="Financeiro",
                                            fg_color="transparent", text_color=("gray10", "gray90"), hover_color=("gray70", "gray30"),
                                            anchor="w", command=lambda: self.select_frame_by_name("financeiro"))
        self.btn_financeiro.grid(row=3, column=0, sticky="ew")

        # Switch de Tema (Extra)
        self.appearance_mode_menu = ctk.CTkOptionMenu(self.navigation_frame, values=["System", "Light", "Dark"],
                                                      command=self.change_appearance_mode_event)
        self.appearance_mode_menu.grid(row=5, column=0, padx=20, pady=20, sticky="s")

    def create_agenda_dashboard(self):
        # Configuração do Grid da Agenda: Coluna 0 (Cards/Lista), Coluna 1 (Formulário Rápido)
        self.agenda_frame.grid_columnconfigure(0, weight=3) # Area de cards maior
        self.agenda_frame.grid_columnconfigure(1, weight=1) # Sidebar direita
        self.agenda_frame.grid_rowconfigure(0, weight=1)

        # --- Área de Cards (Esquerda) ---
        self.cards_scroll_frame = ctk.CTkScrollableFrame(self.agenda_frame, label_text="Próximos Agendamentos")
        self.cards_scroll_frame.grid(row=0, column=0, sticky="nsew", padx=(20, 10), pady=20)

        # Popular com Mock Data + Dados Reais
        self.populate_cards()

        # --- Formulário Lateral (Direita) ---
        self.form_frame = ctk.CTkFrame(self.agenda_frame)
        self.form_frame.grid(row=0, column=1, sticky="nsew", padx=(10, 20), pady=20)

        ctk.CTkLabel(self.form_frame, text="Novo Agendamento", font=ctk.CTkFont(size=18, weight="bold")).pack(pady=20)

        self.entry_cliente = ctk.CTkEntry(self.form_frame, placeholder_text="Nome do Cliente")
        self.entry_cliente.pack(pady=10, padx=20, fill="x")

        # Combos (Carregar dados)
        self.combo_profissional = ctk.CTkComboBox(self.form_frame, values=["Carregando..."])
        self.combo_profissional.pack(pady=10, padx=20, fill="x")

        self.combo_servico = ctk.CTkComboBox(self.form_frame, values=["Carregando..."])
        self.combo_servico.pack(pady=10, padx=20, fill="x")

        # Data e Hora
        self.entry_data = ctk.CTkEntry(self.form_frame, placeholder_text="YYYY-MM-DD")
        self.entry_data.insert(0, datetime.now().strftime("%Y-%m-%d"))
        self.entry_data.pack(pady=10, padx=20, fill="x")

        self.entry_hora = ctk.CTkEntry(self.form_frame, placeholder_text="HH:MM")
        self.entry_hora.pack(pady=10, padx=20, fill="x")

        self.btn_salvar = ctk.CTkButton(self.form_frame, text="Confirmar Agendamento", command=self.salvar_agendamento)
        self.btn_salvar.pack(pady=30, padx=20, fill="x")

        self.carregar_dados_combos()

    def populate_cards(self):
        # Limpar cards antigos
        for widget in self.cards_scroll_frame.winfo_children():
            widget.destroy()

        # Mock Data para Visual App Feel
        mock_agendamentos = [
            {"hora": "09:00", "cliente": "Fernanda Torres", "servico": "Corte e Hidratação", "profissional": "Ana Silva", "status": "Confirmado"},
            {"hora": "10:30", "cliente": "Juliana Paes", "servico": "Manicure Completa", "profissional": "Carlos Oliveira", "status": "Pendente"},
            {"hora": "13:00", "cliente": "Cláudia Raia", "servico": "Limpeza de Pele", "profissional": "Mariana Souza", "status": "Confirmado"},
            {"hora": "14:30", "cliente": "Giovanna Antonelli", "servico": "Design de Sobrancelhas", "profissional": "Ana Silva", "status": "Em Andamento"},
            {"hora": "16:00", "cliente": "Taís Araújo", "servico": "Escova Progressiva", "profissional": "Mariana Souza", "status": "Confirmado"},
        ]

        # Loop para criar Cards
        for ag in mock_agendamentos:
            self.create_card(ag)

    def create_card(self, data):
        card = ctk.CTkFrame(self.cards_scroll_frame)
        card.pack(fill="x", pady=10, padx=5)

        # Layout do Card
        # Esquerda: Horário em destaque
        left_box = ctk.CTkFrame(card, fg_color="transparent", width=80)
        left_box.pack(side="left", padx=10, pady=10)

        lbl_hora = ctk.CTkLabel(left_box, text=data["hora"], font=ctk.CTkFont(size=24, weight="bold"), text_color="#3B8ED0")
        lbl_hora.pack()

        # Centro: Informações
        center_box = ctk.CTkFrame(card, fg_color="transparent")
        center_box.pack(side="left", fill="both", expand=True, padx=10)

        lbl_cliente = ctk.CTkLabel(center_box, text=data["cliente"], font=ctk.CTkFont(size=16, weight="bold"))
        lbl_cliente.pack(anchor="w")

        lbl_info = ctk.CTkLabel(center_box, text=f"{data['servico']} com {data['profissional']}", text_color="gray60")
        lbl_info.pack(anchor="w")

        # Direita: Status Badge (Simples Label por enquanto)
        right_box = ctk.CTkFrame(card, fg_color="transparent")
        right_box.pack(side="right", padx=15)

        color_status = "green" if data["status"] == "Confirmado" else "orange"
        btn_status = ctk.CTkButton(right_box, text=data["status"], fg_color=color_status, height=25,
                                   font=ctk.CTkFont(size=11), width=100, hover=False, corner_radius=20)
        btn_status.pack()

    def select_frame_by_name(self, name):
        # Atualiza botões
        self.btn_agenda.configure(fg_color=("gray75", "gray25") if name == "agenda" else "transparent")
        self.btn_clientes.configure(fg_color=("gray75", "gray25") if name == "clientes" else "transparent")
        self.btn_financeiro.configure(fg_color=("gray75", "gray25") if name == "financeiro" else "transparent")

        # Mostra frame selecionado
        if name == "agenda":
            self.agenda_frame.grid(row=0, column=1, sticky="nsew")
        else:
            self.agenda_frame.grid_forget()

        # Placeholder para outras paginas
        if name == "clientes":
            self.clientes_frame.grid(row=0, column=1, sticky="nsew")
            ctk.CTkLabel(self.clientes_frame, text="Gestão de Clientes (Em Breve)", font=ctk.CTkFont(size=20, weight="bold")).pack(expand=True)
        else:
            self.clientes_frame.grid_forget()

    def change_appearance_mode_event(self, new_appearance_mode: str):
        ctk.set_appearance_mode(new_appearance_mode)

    def carregar_dados_combos(self):
        self.map_profissionais = {}
        self.map_servicos = {}

        try:
            profs = self.controller.listar_profissionais()
            prof_vals = []
            for p in profs:
                label = f"{p[1]}"
                prof_vals.append(label)
                self.map_profissionais[label] = p[0]
            self.combo_profissional.configure(values=prof_vals)
            if prof_vals: self.combo_profissional.set(prof_vals[0])

            servs = self.controller.listar_servicos()
            serv_vals = []
            for s in servs:
                label = f"{s[1]} - R${s[2]}"
                serv_vals.append(label)
                self.map_servicos[label] = s[0]
            self.combo_servico.configure(values=serv_vals)
            if serv_vals: self.combo_servico.set(serv_vals[0])

        except Exception as e:
            print(f"Erro ao carregar combos: {e}")

    def salvar_agendamento(self):
        prof_name = self.combo_profissional.get()
        serv_name = self.combo_servico.get()
        data = self.entry_data.get()
        hora = self.entry_hora.get()

        # Validação Rápida
        if not hora or not data:
            messagebox.showwarning("Aviso", "Preencha a data e hora!")
            return

        id_prof = self.map_profissionais.get(prof_name)
        id_servico = self.map_servicos.get(serv_name)

        if id_prof and id_servico:
             sucesso, msg = self.controller.salvar_novo_agendamento(id_prof, id_servico, data, hora)
             if sucesso:
                 messagebox.showinfo("Sucesso", "Agendamento Criado! (Atualize a lista para ver - Mock não atualiza auto)")
             else:
                 messagebox.showerror("Erro", msg)
        else:
             messagebox.showerror("Erro", "Erro ao identificar IDs. Verifique o banco de dados.")

if __name__ == "__main__":
    app = App()
    app.mainloop()
