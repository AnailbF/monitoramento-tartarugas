"""
Sistema de Monitoramento de Ninhos de Tartarugas Marinhas

Este script gerencia informações sobre ninhos de tartarugas marinhas,
permitindo a inserção, visualização, análise e integração meteorológica.
"""

import requests
from datetime import datetime

# Configuração OpenWeatherMap (substitua pela sua chave gratuita)
API_KEY_OWM = "SUA_CHAVE_AQUI"

# Fallback de coordenadas
COORDS_FALLBACK = {
    'Praia Norte': (-27.6, -48.5),
    'Praia Central': (-27.7, -48.5),
    'Praia Sul': (-27.8, -48.6),
    'Praia Leste': (-27.5, -48.4),
    'Praia Oeste': (-27.6, -48.6),
}

# --- Estrutura de Dados --- #
ninhos = [
    {'regiao': 'Praia Norte', 'quantidade_ovos': 102, 'status': 'intacto', 'risco': '🟢', 'dias_para_eclosao': 12, 'predadores': False},
    {'regiao': 'Praia Central', 'quantidade_ovos': 89, 'status': 'danificado', 'risco': '🔴', 'dias_para_eclosao': 3, 'predadores': True},
    {'regiao': 'Praia Sul', 'quantidade_ovos': 120, 'status': 'ameaçado', 'risco': '🟡', 'dias_para_eclosao': 7, 'predadores': False},
    {'regiao': 'Praia Central', 'quantidade_ovos': 75, 'status': 'intacto', 'risco': '🟢', 'dias_para_eclosao': 2, 'predadores': False},
    {'regiao': 'Praia Norte', 'quantidade_ovos': 60, 'status': 'danificado', 'risco': '🔴', 'dias_para_eclosao': 5, 'predadores': True},
    {'regiao': 'Praia Leste', 'quantidade_ovos': 95, 'status': 'intacto', 'risco': '🟢', 'dias_para_eclosao': 10, 'predadores': False},
    {'regiao': 'Praia Oeste', 'quantidade_ovos': 110, 'status': 'ameaçado', 'risco': '🟡', 'dias_para_eclosao': 6, 'predadores': False},
    {'regiao': 'Praia Norte', 'quantidade_ovos': 80, 'status': 'intacto', 'risco': '🟢', 'dias_para_eclosao': 15, 'predadores': False},
    {'regiao': 'Praia Sul', 'quantidade_ovos': 70, 'status': 'danificado', 'risco': '🔴', 'dias_para_eclosao': 1, 'predadores': True},
    {'regiao': 'Praia Central', 'quantidade_ovos': 100, 'status': 'intacto', 'risco': '🟢', 'dias_para_eclosao': 8, 'predadores': False}
]

# --- Funções de Geocodificação --- #
def obter_coordenadas_regiao(regiao: str) -> tuple:
    """Geocodificação dinâmica com Nominatim (OpenStreetMap)."""
    try:
        url = f"https://nominatim.openstreetmap.org/search?q={regiao.replace(' ', '+')},+Brasil&format=json&limit=1"
        headers = {'User-Agent': 'MonitorTartarugas/1.0'}
        resp = requests.get(url, headers=headers, timeout=10)
        data = resp.json()
        if data:
            return float(data[0]['lat']), float(data[0]['lon'])
    except:
        pass
    return COORDS_FALLBACK.get(regiao, (-27.6, -48.5))

# --- Funções Meteorológicas --- #
def obter_clima_regiao(regiao: str) -> dict:
    """Clima via OpenWeatherMap ou mock."""
    lat, lon = obter_coordenadas_regiao(regiao)
    if API_KEY_OWM != "SUA_CHAVE_AQUI":
        try:
            url = f"https://api.openweathermap.org/data/2.5/weather?lat={lat}&lon={lon}&appid={API_KEY_OWM}&units=metric&lang=pt_br"
            data = requests.get(url, timeout=10).json()
            return {
                'temperatura': data['main']['temp'],
                'umidade': data['main']['humidity'],
                'precipitacao': data.get('rain', {}).get('1h', 0),
                'vento': data['wind'].get('speed', 0) * 3.6,
                'descricao': data['weather'][0]['description']
            }
        except:
            pass
    # Mock
    mock = {
        'Praia Sul': {'temperatura': 23.0, 'precipitacao': 8.0, 'vento': 35},
    }
    return mock.get(regiao, {'temperatura': 25, 'precipitacao': 0, 'vento': 15})

def atualizar_risco_por_clima(lista_ninhos: list):
    """Atualiza o risco dos ninhos com base nas condições climáticas."""
    for ninho in lista_ninhos:
        clima = obter_clima_regiao(ninho['regiao'])
        if clima.get('precipitacao', 0) > 5 or clima.get('vento', 0) > 30:
            ninho['risco'] = '🔴'
            ninho['status'] = 'ameaçado'

# --- Funções de Validação --- #
def validar_ninho(ninho: dict) -> tuple:
    """Valida os dados de um ninho de tartaruga."""
    if not isinstance(ninho.get('regiao'), str) or not ninho.get('regiao'):
        return False, "Região inválida. Deve ser uma string não vazia."
    if not isinstance(ninho.get('quantidade_ovos'), int) or ninho.get('quantidade_ovos') <= 0:
        return False, "Quantidade de ovos inválida. Deve ser um número inteiro positivo."
    if ninho.get('status') not in ['intacto', 'ameaçado', 'danificado']:
        return False, "Status inválido. Use 'intacto', 'ameaçado' ou 'danificado'."
    if ninho.get('risco') not in ['🟢', '🟡', '🔴']:
        return False, "Risco inválido. Use 🟢, 🟡 ou 🔴."
    if not isinstance(ninho.get('dias_para_eclosao'), int) or ninho.get('dias_para_eclosao') < 0:
        return False, "Dias para eclosão inválidos. Deve ser um número inteiro não negativo."
    if not isinstance(ninho.get('predadores'), bool):
        return False, "Presença de predadores inválida. Use True ou False."
    return True, "Ninho válido."

# --- Funções de Análise de Dados --- #
def obter_total_ninhos(lista_ninhos: list) -> int:
    """Retorna o número total de ninhos registrados."""
    return len(lista_ninhos)

def calcular_media_ovos_por_risco(lista_ninhos: list, risco_alvo: str) -> float:
    """Calcula a média de ovos para ninhos com um risco específico."""
    total_ovos = 0
    ninhos_com_risco = 0
    for ninho in lista_ninhos:
        if ninho['risco'] == risco_alvo:
            total_ovos += ninho['quantidade_ovos']
            ninhos_com_risco += 1
    return total_ovos / ninhos_com_risco if ninhos_com_risco > 0 else 0.0

def contar_ninhos_prestes_a_eclodir(lista_ninhos: list, dias_limite: int = 5) -> int:
    """Conta quantos ninhos estão prestes a eclodir."""
    count = 0
    for ninho in lista_ninhos:
        if ninho['dias_para_eclosao'] <= dias_limite:
            count += 1
    return count

def encontrar_regiao_mais_risco(lista_ninhos: list) -> str:
    """Identifica a região com o maior número de ninhos sob risco '🔴'."""
    risco_por_regiao = {}
    for ninho in lista_ninhos:
        if ninho['risco'] == '🔴':
            regiao = ninho['regiao']
            risco_por_regiao[regiao] = risco_por_regiao.get(regiao, 0) + 1
    if not risco_por_regiao:
        return "Nenhuma região com ninhos sob risco '🔴'."
    return max(risco_por_regiao, key=risco_por_regiao.get)

def contar_ninhos_predadores_danificados(lista_ninhos: list) -> int:
    """Conta ninhos que têm predadores E estão danificados."""
    count = 0
    for ninho in lista_ninhos:
        if ninho['predadores'] and ninho['status'] == 'danificado':
            count += 1
    return count

# --- Funções de Interação com o Usuário --- #
def exibir_menu():
    print("\n--- Menu Guardião das Tartaruguinhas ---")
    print("1. Inserir novo ninho")
    print("2. Visualizar relatório completo")
    print("3. Consultar estatísticas")
    print("4. Atualizar riscos com clima")
    print("5. Sair")

def inserir_novo_ninho(lista_ninhos: list):
    print("\n--- Inserir Novo Ninho ---")
    try:
        regiao = input("Região: ")
        quantidade_ovos = int(input("Quantidade de ovos: "))
        status = input("Status (intacto, ameaçado, danificado): ")
        risco = input("Risco (🟢, 🟡, 🔴): ")
        dias_para_eclosao = int(input("Dias para eclosão: "))
        predadores_str = input("Predadores (True/False): ")
        predadores = predadores_str.lower() == 'true'

        novo_ninho = {
            'regiao': regiao,
            'quantidade_ovos': quantidade_ovos,
            'status': status,
            'risco': risco,
            'dias_para_eclosao': dias_para_eclosao,
            'predadores': predadores
        }

        valido, mensagem = validar_ninho(novo_ninho)
        if valido:
            lista_ninhos.append(novo_ninho)
            print("Ninho adicionado com sucesso!")
        else:
            print(f"Erro ao adicionar ninho: {mensagem}")
    except ValueError:
        print("Entrada inválida. Certifique-se de inserir números para ovos e dias, e True/False para predadores.")

def visualizar_relatorio_completo(lista_ninhos: list):
    print("\n--- Relatório Completo ---")
    if not lista_ninhos:
        print("Nenhum ninho registrado.")
    else:
        for i, ninho in enumerate(lista_ninhos):
            print(f"Ninho {i+1}:")
            for chave, valor in ninho.items():
                print(f" {chave.replace('_', ' ').title()}: {valor}")
            print("-" * 20)

def consultar_estatisticas(lista_ninhos: list):
    print("\n--- Estatísticas ---")
    print(f"Total de ninhos: {obter_total_ninhos(lista_ninhos)}")
    print(f"Média de ovos por ninho com risco '🟢': {calcular_media_ovos_por_risco(lista_ninhos, '🟢'):.2f}")
    print(f"Ninhos prestes a eclodir (<= 5 dias): {contar_ninhos_prestes_a_eclodir(lista_ninhos)}")
    print(f"Região com mais ninhos sob risco '🔴': {encontrar_regiao_mais_risco(lista_ninhos)}")
    print(f"Ninhos com predadores e danificados: {contar_ninhos_predadores_danificados(lista_ninhos)}")

# --- Menu Principal --- #
def menu_principal():
    while True:
        exibir_menu()
        escolha = input("Escolha uma opção (ou 'sair' para encerrar): ").lower().strip()
        if escolha == '1':
            inserir_novo_ninho(ninhos)
        elif escolha == '2':
            visualizar_relatorio_completo(ninhos)
        elif escolha == '3':
            consultar_estatisticas(ninhos)
        elif escolha == '4':
            atualizar_risco_por_clima(ninhos)
            print("Riscos atualizados com base no clima atual!")
        elif escolha == '5' or escolha == 'sair':
            print("Saindo do sistema. Proteja as tartarugas! 🐢")
            break
        else:
            print("Opção inválida.")

if __name__ == "__main__":
    menu_principal()
