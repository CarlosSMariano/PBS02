# SPRINT 3 - Ecossistema Tech PBS02

  
## Desenvolvido Por 
* **Carlos Eduardo Sanches mariano Rm: 561756**
* **Leonardo Eiji Kina RM: 562784**
* **Luís Scacchetti Mariano RM: 562241**
* **Rodrigo do Santos Abubakir RM: 561479**
* **Vitor Ramos de Farias RM: 561958**

## 💡Resumo
Um dos desafios enfrentados pelo futebol feminino é a falta de investimento em estruturas adequadas para a coleta de dados necessários dos jogos e atletas. Essa carência de informações confiáveis contribui para a desvalorização do esporte e dificulta análises de desempenho aprofundadas.

Visando essa problemática, a Synapse apresenta uma solução simples e acessível, que fornece dados de jogo em tempo real, permitindo uma análise mais profunda do desempenho das atletas e equipes. 

Essa solução permite que a coleta de dados seja mais eficiênte e confiável, e em conjunto com o portal Passa a Bola, facilitamos a busca por informações confiáveis, o que demonstra o valor e potencial das atletas, aumentando a visibilidade do esporte e por consequência atraindo mais investimento.

---

## ✨ Como funciona

---



## 📦 Componentes do Projeto

### 1. 🟨 Node-RED (Camada de API)
- **Função**: Cria endpoints REST para comunicação
- **Responsabilidades**:
  - Receber dados de sensores/tracking
  - Publicar mensagens via MQTT
  - Gerenciar fluxo de dados em tempo real
  - Fornecer API para o frontend

### 2. 🟦 Mosquitto MQTT (Message Broker)
- **Função**: Middleware de mensagens em tempo real
- **Protocolo**: MQTT para comunicação assíncrona
- **Vantagens**: Baixa latência, ideal para tempo real

### 3. 🐍 Python (Processamento de Dados)
- **Função**: Cálculos avançados e análise de dados
- **Algoritmo Principal**: **Cálculo de Proximidade Euclidiana**
  - Fórmula: `√((x₂ - x₁)² + (y₂ - y₁)²)`
  - Aplica-se para determinar posicionamento de jogadoras
  - Calcula distâncias entre jogadoras, bola, gol e referências


## 🔄 Fluxo de Dados

1. **Captura** → Dados coletados de sensores/câmeras
2. **MQTT** → Distribui mensagens para subscribers
3. **Python** → Processa cálculos de proximidade euclidiana
4. **Node-RED** → Recebe e estrutura os dados brutos
5. **React** → Visualiza dados processados em tempo real

## 🚀 Como Executar


