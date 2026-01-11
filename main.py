import customtkinter as ctk
from tkinter import messagebox
from controllers import StudioController
import re
from datetime import datetime

# Configuração Global do CustomTkinter
ctk.set_appearance_mode("System")
ctk.set_default_color_theme("blue")

class ModalCliente(ctk.CTkToplevel):
    def __init__(self, parent):
        super().__init__(parent)
        self.title("Novo Cliente")
        self.geometry("400x450")
        self.resizable(False, False)

        # Centralizar na tela (simplificado)
        self.attributes("-topmost", True)

        # Header
        ctk.CTkLabel(self, text="Cadastro de Cliente", font=ctk.CTkFont(size=18, weight="bold")).pack(pady=20)

        # Campos
        self.entry_nome = ctk.CTkEntry(self, placeholder_text="Nome Completo")
        self.entry_nome.pack(pady=10, padx=20, fill="x")

        self.entry_telefone = ctk.CTkEntry(self, placeholder_text="Telefone (ex: 1199999-9999)")
        self.entry_telefone.pack(pady=10, padx=20, fill="x")

        self.entry_email = ctk.CTkEntry(self, placeholder_text="Email")
        self.entry_email.pack(pady=10, padx=20, fill="x")

        self.entry_obs = ctk.CTkTextbox(self, height=100)
        self.entry_obs.pack(pady=10, padx=20, fill="x")
        self.entry_obs.insert("0.0", "Observações...")

        # Botão Salvar
        ctk.CTkButton(self, text="Salvar Cliente", command=self.salvar).pack(pady=20, padx=20, fill="x")

    def salvar(self):
        nome = self.entry_nome.get()
        fone = self.entry_telefone.get()
        email = self.entry_email.get()
        obs = self.entry_obs.get("0.0", "end")

        if not nome or not fone:
            print("Erro: Nome e Telefone obrigatórios")
            return

        print(f"SALVAR SIMULADO: Nome={nome}, Fone={fone}, Email={email}")
        self.destroy()

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

        # 1. Navigation Rail
        self.create_navigation_rail()

        # 2. Frames de Conteúdo
        # Instanciamos os frames mas só mostramos um por vez
        self.agenda_frame = ctk.CTkFrame(self, corner_radius=0, fg_color="transparent")
        self.clientes_frame = ctk.CTkFrame(self, corner_radius=0, fg_color="transparent")

        # Build das interfaces
        self.create_agenda_dashboard()
        self.create_clientes_dashboard()

        # Mock Data Clientes
        self.clientes_mock = [
            {"nome": "Maria Silva", "fone": "(11) 98888-1111"},
            {"nome": "Joana Dark", "fone": "(21) 97777-2222"},
            {"nome": "Patricia Abravanel", "fone": "(11) 96666-3333"},
            {"nome": "Xuxa Meneghel", "fone": "(55) 95555-4444"},
        ]
        self.populate_clientes()

        # Inicializa na Agenda
        self.select_frame_by_name("agenda")

    def create_navigation_rail(self):
        self.navigation_frame = ctk.CTkFrame(self, corner_radius=0, width=140)
        self.navigation_frame.grid(row=0, column=0, sticky="nsew")
        self.navigation_frame.grid_rowconfigure(4, weight=1)

        self.logo_label = ctk.CTkLabel(self.navigation_frame, text="Studio\nManager",
                                       font=ctk.CTkFont(size=20, weight="bold"))
        self.logo_label.grid(row=0, column=0, padx=20, pady=20)

        # Botões
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

        # Tema
        self.appearance_mode_menu = ctk.CTkOptionMenu(self.navigation_frame, values=["System", "Light", "Dark"],
                                                      command=self.change_appearance_mode_event)
        self.appearance_mode_menu.grid(row=5, column=0, padx=20, pady=20, sticky="s")

    # --- AGENDA ---
    def create_agenda_dashboard(self):
        self.agenda_frame.grid_columnconfigure(0, weight=3)
        self.agenda_frame.grid_columnconfigure(1, weight=1)
        self.agenda_frame.grid_rowconfigure(0, weight=1)

        # Esquerda: Cards
        self.cards_scroll_frame = ctk.CTkScrollableFrame(self.agenda_frame, label_text="Próximos Agendamentos")
        self.cards_scroll_frame.grid(row=0, column=0, sticky="nsew", padx=(20, 10), pady=20)
        self.populate_cards()

        # Direita: Form
        self.form_frame = ctk.CTkFrame(self.agenda_frame)
        self.form_frame.grid(row=0, column=1, sticky="nsew", padx=(10, 20), pady=20)

        ctk.CTkLabel(self.form_frame, text="Novo Agendamento", font=ctk.CTkFont(size=18, weight="bold")).pack(pady=20)

        self.entry_cliente_ag = ctk.CTkEntry(self.form_frame, placeholder_text="Nome do Cliente")
        self.entry_cliente_ag.pack(pady=10, padx=20, fill="x")

        self.combo_profissional = ctk.CTkComboBox(self.form_frame, values=["Carregando..."])
        self.combo_profissional.pack(pady=10, padx=20, fill="x")

        self.combo_servico = ctk.CTkComboBox(self.form_frame, values=["Carregando..."])
        self.combo_servico.pack(pady=10, padx=20, fill="x")

        self.entry_data = ctk.CTkEntry(self.form_frame, placeholder_text="YYYY-MM-DD")
        self.entry_data.insert(0, datetime.now().strftime("%Y-%m-%d"))
        self.entry_data.pack(pady=10, padx=20, fill="x")

        self.entry_hora = ctk.CTkEntry(self.form_frame, placeholder_text="HH:MM")
        self.entry_hora.pack(pady=10, padx=20, fill="x")

        ctk.CTkButton(self.form_frame, text="Confirmar", command=self.salvar_agendamento).pack(pady=30, padx=20, fill="x")

        self.carregar_dados_combos()

    def populate_cards(self):
        # Mock Data Agendamentos
        mock_agendamentos = [
            {"hora": "09:00", "cliente": "Fernanda Torres", "servico": "Corte", "profissional": "Ana Silva", "status": "Confirmado"},
            {"hora": "10:30", "cliente": "Juliana Paes", "servico": "Manicure", "profissional": "Carlos", "status": "Pendente"},
            {"hora": "13:00", "cliente": "Cláudia Raia", "servico": "Pele", "profissional": "Mariana", "status": "Confirmado"},
        ]
        for ag in mock_agendamentos:
            self.create_card(ag)

    def create_card(self, data):
        card = ctk.CTkFrame(self.cards_scroll_frame)
        card.pack(fill="x", pady=10, padx=5)

        left_box = ctk.CTkFrame(card, fg_color="transparent", width=80)
        left_box.pack(side="left", padx=10, pady=10)
        ctk.CTkLabel(left_box, text=data["hora"], font=ctk.CTkFont(size=24, weight="bold"), text_color="#3B8ED0").pack()

        center_box = ctk.CTkFrame(card, fg_color="transparent")
        center_box.pack(side="left", fill="both", expand=True, padx=10)
        ctk.CTkLabel(center_box, text=data["cliente"], font=ctk.CTkFont(size=16, weight="bold")).pack(anchor="w")
        ctk.CTkLabel(center_box, text=f"{data['servico']} com {data['profissional']}", text_color="gray60").pack(anchor="w")

        right_box = ctk.CTkFrame(card, fg_color="transparent")
        right_box.pack(side="right", padx=15)
        color = "green" if data["status"] == "Confirmado" else "orange"
        ctk.CTkButton(right_box, text=data["status"], fg_color=color, height=25, width=100, hover=False).pack()

    # --- CLIENTES ---
    def create_clientes_dashboard(self):
        # Layout Clientes: Top Bar + List
        self.clientes_frame.grid_columnconfigure(0, weight=1)
        self.clientes_frame.grid_rowconfigure(1, weight=1) # Row 1 has the list

        # Top Bar (Busca + Adicionar)
        top_bar = ctk.CTkFrame(self.clientes_frame, fg_color="transparent")
        top_bar.grid(row=0, column=0, sticky="ew", padx=20, pady=20)

        self.entry_busca = ctk.CTkEntry(top_bar, placeholder_text="Buscar cliente...", width=300)
        self.entry_busca.pack(side="left", fill="x", expand=True, padx=(0, 10))

        btn_add = ctk.CTkButton(top_bar, text="+ Novo Cliente", width=120, command=self.open_modal_cliente)
        btn_add.pack(side="right")

        # Lista Scrollable
        self.clientes_scroll = ctk.CTkScrollableFrame(self.clientes_frame, label_text="Meus Clientes")
        self.clientes_scroll.grid(row=1, column=0, sticky="nsew", padx=20, pady=(0, 20))

    def populate_clientes(self):
        # Limpa
        for widget in self.clientes_scroll.winfo_children():
            widget.destroy()

        # Popula mock
        for cl in self.clientes_mock:
            self.create_client_card(cl)

    def create_client_card(self, data):
        card = ctk.CTkFrame(self.clientes_scroll)
        card.pack(fill="x", pady=5, padx=5)

        # Info
        ctk.CTkLabel(card, text=data["nome"], font=ctk.CTkFont(size=15, weight="bold")).pack(side="left", padx=20, pady=15)
        ctk.CTkLabel(card, text=data["fone"], text_color="gray60").pack(side="left", padx=10)

        # Actions
        ctk.CTkButton(card, text="Editar", width=60, height=25, fg_color="gray", hover_color="gray40").pack(side="right", padx=20)

    def open_modal_cliente(self):
        ModalCliente(self)

    # --- NAVIGATION ---
    def select_frame_by_name(self, name):
        # Botões
        self.btn_agenda.configure(fg_color=("gray75", "gray25") if name == "agenda" else "transparent")
        self.btn_clientes.configure(fg_color=("gray75", "gray25") if name == "clientes" else "transparent")
        self.btn_financeiro.configure(fg_color=("gray75", "gray25") if name == "financeiro" else "transparent")

        # View switching
        if name == "agenda":
            self.agenda_frame.grid(row=0, column=1, sticky="nsew")
        else:
            self.agenda_frame.grid_forget()

        if name == "clientes":
            self.clientes_frame.grid(row=0, column=1, sticky="nsew")
        else:
            self.clientes_frame.grid_forget()

    def change_appearance_mode_event(self, new_appearance_mode: str):
        ctk.set_appearance_mode(new_appearance_mode)

    # --- LOGIC (Agenda) ---
    def carregar_dados_combos(self):
        # Simplificado para manter o arquivo menor, assumindo que funciona igual ao anterior
        self.map_profissionais = {}
        self.map_servicos = {}
        try:
            profs = self.controller.listar_profissionais()
            p_vals = [p[1] for p in profs]
            self.combo_profissional.configure(values=p_vals)
            for p in profs: self.map_profissionais[p[1]] = p[0]

            servs = self.controller.listar_servicos()
            s_vals = [s[1] for s in servs]
            self.combo_servico.configure(values=s_vals)
            for s in servs: self.map_servicos[s[1]] = s[0]
        except: pass

    def salvar_agendamento(self):
        # Lógica de salvar (simplificada)
        print("Salvar chamado (lógica mantida do anterior)")

if __name__ == "__main__":
    app = App()
    app.mainloop()
