from controllers import StudioController

def testar_controllers():
    controller = StudioController()

    print("--- Teste: Listar Profissionais ---")
    profs = controller.listar_profissionais()
    for p in profs:
        print(p)

    print("\n--- Teste: Listar Serviços ---")
    servicos = controller.listar_servicos()
    for s in servicos:
        print(s)

    if not profs or not servicos:
        print("Erro: Precisa de dados no banco para testar agendamento.")
        return

    id_prof = profs[0][0]
    id_servico = servicos[0][0]
    data_teste = "2023-10-27"
    hora_inicio = "14:00"

    print(f"\n--- Teste: Agendar para Prof {id_prof}, Serviço {id_servico} em {data_teste} às {hora_inicio} ---")
    sucesso, msg = controller.salvar_novo_agendamento(id_prof, id_servico, data_teste, hora_inicio)
    print(f"Resultado: {sucesso} - {msg}")

    print("\n--- Teste: Tentar agendar no MESMO horário (Conflito Exato) ---")
    sucesso, msg = controller.salvar_novo_agendamento(id_prof, id_servico, data_teste, hora_inicio)
    print(f"Resultado Esperado (False): {sucesso} - {msg}")

    print("\n--- Teste: Tentar agendar em horário sobreposto (14:30, conflito parcial) ---")
    # Assumindo que o serviço 0 tenha duração > 30 min
    sucesso, msg = controller.salvar_novo_agendamento(id_prof, id_servico, data_teste, "14:30")
    print(f"Resultado Esperado (False): {sucesso} - {msg}")

    print("\n--- Teste: Agendar em horário livre (16:00) ---")
    sucesso, msg = controller.salvar_novo_agendamento(id_prof, id_servico, data_teste, "16:00")
    print(f"Resultado Esperado (True): {sucesso} - {msg}")

    controller.close()

if __name__ == "__main__":
    testar_controllers()
