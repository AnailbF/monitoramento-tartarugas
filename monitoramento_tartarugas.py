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
    # Mock para testes
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

# --- Funções de Gerenciamento de Ninhos --- #
def validar_ninho(ninho: dict) -> tuple:
    """Valida os dados de um ninho."""
    if not isinstance(ninho.get('regiao'), str) or not ninho.get('regiao'):
        return False, "Região inválida."
    if not isinstance(ninho.get('quantidade_ovos'), int) or ninho['quantidade_ovos'] < 0:
        return False, "Quantidade de ovos inválida."
    return True, "Válido"

def inserir_novo_ninho(lista_ninhos: list):
    """Permite ao usuário inserir um novo ninho."""
    print("\n--- Inserir Novo Ninho ---")
    regiao = input("Nome da Praia/Região: ").strip()
    try:
        ovos = int(input("Quantidade de ovos: "))
        dias = int(input("Dias para eclosão: "))
        predadores = input("Predadores detectados? (s/n): ").lower() == 's'
        
        novo_ninho = {
            'regiao': regiao,
            'quantidade_ovos': ovos,
            'status': 'intacto',
            'risco': '🟢',
            'dias_para_eclosao': dias,
            'predadores': predadores
        }
        
        valido, msg = validar_ninho(novo_ninho)
        if valido:
            lista_ninhos.append(novo_ninho)
            print(f"Ninho em {regiao} adicionado com sucesso!")
        else:
            print(f"Erro: {msg}")
    except ValueError:
        print("Erro: Insira valores numéricos válidos.")

def visualizar_relatorio_completo(lista_ninhos: list):
    """Exibe todos os ninhos monitorados."""
    print("\n--- Relatório de Monitoramento ---")
    print(f"{'Região':<20} | {'Ovos':<5} | {'Status':<10} | {'Risco':<5} | {'Eclosão':<7}")
    print("-" * 60)
    for ninho in lista_ninhos:
        print(f"{ninho['regiao']:<20} | {ninho['quantidade_ovos']:<5} | {ninho['status']:<10} | {ninho['risco']:<5} | {ninho['dias_para_eclosao']:<7} dias")

def consultar_estatisticas(lista_ninhos: list):
    """Exibe estatísticas básicas sobre os ninhos."""
    if not lista_ninhos:
        print("Nenhum dado disponível.")
        return
    total_ovos = sum(n['quantidade_ovos'] for n in lista_ninhos)
    media_ovos = total_ovos / len(lista_ninhos)
    ameaçados = sum(1 for n in lista_ninhos if n['risco'] in ['🟡', '🔴'])
    
    print("\n--- Estatísticas ---")
    print(f"Total de ninhos: {len(lista_ninhos)}")
    print(f"Total de ovos monitorados: {total_ovos}")
    print(f"Média de ovos por ninho: {media_ovos:.2f}")
    print(f"Ninhos em risco/ameaçados: {ameaçados}")

# --- Menu Principal --- #
def exibir_menu():
    print("\n--- Menu Guardião das Tartaruguinhas ---")
    print("1. Inserir novo ninho")
    print("2. Visualizar relatório completo")
    print("3. Consultar estatísticas")
    print("4. Atualizar riscos com clima")
    print("5. Sair")

def menu_principal():
    while True:
        exibir_menu()
        escolha = input("Escolha (1-5): ").strip()
        if escolha == '1':
            inserir_novo_ninho(ninhos)
        elif escolha == '2':
            visualizar_relatorio_completo(ninhos)
        elif escolha == '3':
            consultar_estatisticas(ninhos)
        elif escolha == '4':
            atualizar_risco_por_clima(ninhos)
            print("Riscos atualizados com base no clima atual!")
        elif escolha == '5':
            print("Encerrando sistema. Proteja as tartarugas! 🐢")
            break
        else:
            print("Opção inválida.")

if __name__ == "__main__":
    menu_principal()
