# Monitoramento de Ninhos de Tartarugas Marinhas 🐢

Este projeto é um sistema de gerenciamento e monitoramento de ninhos de tartarugas marinhas, integrando dados meteorológicos em tempo real para avaliar riscos aos ninhos.

## 🚀 Funcionalidades

- **Gerenciamento de Ninhos**: Inserção, visualização e análise estatística de dados dos ninhos.
- **Geocodificação Dinâmica**: Suporte automático para qualquer nome de praia ou região através do OpenStreetMap (Nominatim).
- **Integração Meteorológica**: Consulta automática de condições climáticas (temperatura, vento, precipitação) via OpenWeatherMap.
- **Avaliação de Risco**: Atualização automática do status de risco dos ninhos com base em alertas climáticos.

## 🛠️ Tecnologias Utilizadas

- **Python 3**
- **Requests**: Para integração com APIs externas.
- **OpenWeatherMap API**: Dados climáticos em tempo real.
- **Nominatim API**: Geocodificação de localizações.

## 📋 Pré-requisitos

Para utilizar a integração meteorológica completa, você precisará de uma chave de API gratuita do [OpenWeatherMap](https://openweathermap.org/api).

## 🔧 Configuração

1. Clone o repositório.
2. Abra o arquivo `monitoramento_tartarugas.py`.
3. Substitua `SUA_CHAVE_AQUI` pela sua chave da API OpenWeatherMap na variável `API_KEY_OWM`.
4. Execute o script:
   ```bash
   python monitoramento_tartarugas.py
   ```

---
Desenvolvido por **Ana Furtado Moreira Rodrigues** como parte de sua jornada em Ciência de Dados e Engenharia.
