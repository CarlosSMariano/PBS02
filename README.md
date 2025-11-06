# SPRINT 4 - Ecossistema Tech PBS02

## 👥 **Desenvolvido Por**
| Nome | RM |
|------|----|
| Carlos Eduardo Sanches Mariano | 561756 |
| Leonardo Eiji Kina | 562784 |
| Luís Scacchetti Mariano | 562241 |
| Rodrigo do Santos Abubakir | 561479 |
| Vitor Ramos de Farias | 561958 |

## 💡 **Contexto e Problema**
O futebol feminino enfrenta desafios significativos devido à falta de investimento em infraestrutura para coleta de dados. Essa carência de informações confiáveis impacta diretamente na valorização do esporte e impede análises de desempenho aprofundadas.

## 🎯 **Nossa Solução**
A **Synapse** desenvolveu uma solução acessível e eficiente que fornece dados de jogo em tempo real, permitindo análises detalhadas do desempenho das atletas e equipes. Integrado ao portal **Passa a Bola**, nosso sistema facilita o acesso a informações confiáveis, demonstrando o valor e potencial das atletas e aumentando a visibilidade do esporte.

---

## ⚙️ **Arquitetura do Sistema**

### 🔄 **Fluxo de Dados**
1. **📡 Captura** → Coleta de coordenadas via dispositivos IoT
2. **📨 MQTT** → Distribuição de mensagens em tempo real
3. **🐍 Python** → Processamento e cálculos de proximidade
4. **🟨 Node-RED** → Estruturação de dados e criação de APIs
5. **⚛️ React** → Visualização em tempo real no frontend

### 🏗️ **Componentes Técnicos**

#### **📍 Coleta de Coordenadas**
- **Bola**: Posicionamento preciso em campo
- **Gol**: Coordenadas exatas das traves
- **Jogadoras**: Localização individual com identificação por nome e time

#### **📡 Transmissão MQTT**
- **Broker**: Mosquitto
- **Protocolo**: MQTT para comunicação assíncrona
- **Vantagens**: Baixa latência e eficiência em tempo real

#### **🧮 Processamento Inteligente**

**🎯 Cálculo de Posse de Bola**
```json
{
  "nome": "Nome da Jogadora",
  "time": "Time", 
  "tipo": "possession"
}
```
- Distância calculada em metros entre jogadoras e bola
- Posse identificada quando distância < 1,5 metros

**⚽ Detecção de Gol**
- Cálculo de distância entre bola e gol
- Identificação do último jogador com posse antes do gol
- Publicação automática de evento de gol

#### **🐍 Processamento Python**
- **Algoritmo Principal**: Cálculo de Proximidade Euclidiana
- **Fórmula**: `√((x₂ - x₁)² + (y₂ - y₁)²)`
- **Aplicação**: Posicionamento de jogadoras e análise de movimentos

#### **🟨 Node-RED (API Layer)**
- Conversão MQTT → HTTP
- Criação de endpoints REST
- Estruturação de dados em JSON
- Gerenciamento de fluxo em tempo real

---

## 🚀 **Novidades da Versão**

### **🆕 Melhorias Implementadas**
- ✅ **Servidor próprio otimizado** para melhor performance
- ✅ **Cálculos mais precisos** com algoritmos refinados
- ✅ **Transmissão de dados aprimorada** para maior confiabilidade
- ✅ **Interface mais intuitiva** no frontend
- ✅ **Processamento mais eficiente** de eventos em tempo real

---

## 🛠️ **Como Executar**

### **Pré-requisitos**
- Máquina virtual
- Docker-compose instalado

### **🚀 Execução do Sistema Backend**
1. **Baixe a pasta `tef_soccer`** presente neste repositório
2. **Execute os comandos:**
```bash
cd tef_soccer
sudo docker-compose up -d
```
3. **Pronto!** O sistema backend está rodando

### **🌐 Execução do Frontend**
1. **Clone o repositório** do frontend
2. **Instale as dependências:**
```bash
cd frontend
npm install
```
3. **Execute o projeto:**
```bash
npm run dev
```

### **🖼️ Configuração das Imagens**
Caso não estejam aparecendo imagens das jogadoras:
- Adicione as imagens na pasta `public`
- Nomeie os arquivos com letras minúsculas
- Use o mesmo nome enviado pelo dispositivo
- Formato: `.jpg` (ex: `joanasilva.jpg`)

### **🧪 Teste do Sistema**

#### **Opção 1: Com Componentes Físicos**
- Baixe os arquivos `.ino` da pasta `device` deste repositório
- Faça o upload no seu microcontrolador

#### **Opção 2: Simulação via MyMQTT**
- Baixe o aplicativo **MyMQTT** no celular
- Conecte ao seu servidor MQTT
- Envie coordenadas manualmente usando os tópicos:

**📨 Tópicos para Teste:**
```
Tópico: /TEF/device/sc
Mensagem: -23.545556,-46.473889,time,nome

Tópico: /TEF/device/b  
Mensagem: -23.545556,-46.473889

Tópico: /TEF/device/g
Mensagem: -23.545556,-46.473889
```

---

## 📊 **Resultados Esperados**
- 📈 Aumento na visibilidade do futebol feminino
- 🔍 Análises de desempenho mais precisas
- 💰 Atração de investimentos através de dados confiáveis
- ⚡ Sistema em tempo real para tomada de decisão

---

*Sistema desenvolvido para a Sprint 4 - Ecossistema Tech PBS02*
