# Chat Bot GROQ - Conversational AI com LangChain e Streamlit

Este é um projeto de Chatbot utilizando os modelos **GROQ** e a estrutura do **LangChain** com interface **Streamlit**. O bot é capaz de manter a memória da conversa, utilizando entidades com **ConversationEntityMemory** para gerar interações contínuas e naturais.

## Funcionalidades

- Interface em tempo real com **Streamlit**
- Suporte a múltiplos modelos da **GROQ**
- Memória de entidades com **LangChain**
- Configuração personalizável de temperatura, top_p, e comprimento máximo da resposta
- Histórico da conversa com opção para download em texto ou Markdown

## Tecnologias Utilizadas

- **LangChain**: Framework para integrar modelos de linguagem.
- **Streamlit**: Biblioteca para criar aplicações web de forma rápida e simples.
- **GROQ**: Modelos de IA otimizados para aprendizado profundo.
- **Python**: Linguagem de programação principal.

## Requisitos

- Python 3.7+
- Biblioteca **Streamlit**
- Biblioteca **LangChain**
- Conta e API Key na **GROQ**

## Como Instalar

1. Clone o repositório:

    ```bash
    git clone https://github.com/seu-usuario/chatbot-groq.git
    ```

2. Navegue até o diretório do projeto:

    ```bash
    cd chatbot-groq
    ```

3. Instale as dependências:

    ```bash
    pip install -r requirements.txt
    ```

4. Crie um arquivo `.env` para salvar sua chave da API da GROQ:

    ```bash
    echo "GROQ_API_KEY=your_api_key_here" > .env
    ```

5. Execute a aplicação:

    ```bash
    streamlit run groq_modelos.py
    ```

## Interface do Usuário

A aplicação possui uma interface simplificada com:

- **Caixa de texto** para inserir perguntas e comandos.
- **Barra lateral** para selecionar o modelo, configurar a temperatura, top_p, e comprimento máximo de tokens.
- **Histórico da conversa**, onde as interações anteriores podem ser visualizadas e baixadas em texto ou Markdown.
  
## Configurações

A barra lateral oferece opções para personalizar o comportamento do chatbot:

- **Modelo**: Escolha entre vários modelos disponíveis na **GROQ**.
- **Temperatura**: Controle da aleatoriedade das respostas (valores baixos para respostas mais previsíveis, valores altos para respostas mais criativas).
- **Top_p**: Ajusta a amostra de tokens baseados na probabilidade cumulativa.
- **Max_length**: Número máximo de tokens gerados em uma resposta.

## Exemplos de Uso

### Configuração do Modelo
No menu lateral, selecione o modelo desejado, ajuste a temperatura e top_p para controlar o comportamento do modelo.

### Histórico de Conversa
As interações são registradas e podem ser visualizadas no painel principal da aplicação. Use a opção de download para exportar a conversa em formato de texto ou Markdown.

### Exemplo de Interação

1. **Usuário**: Como posso acessar os modelos da GROQ?
2. **Assistente**: Para acessar os modelos da GROQ, você precisa de uma chave de API. Crie uma conta na [GROQ Console](https://console.groq.com/keys) e obtenha sua chave.

## Contribuição

1. Faça um fork do projeto.
2. Crie uma branch para sua feature (`git checkout -b feature/minha-feature`).
3. Faça commit das suas alterações (`git commit -am 'Adiciona nova feature'`).
4. Envie para o repositório (`git push origin feature/minha-feature`).
5. Crie um novo Pull Request.

## Contato

- [GitHub](https://github.com/jeferson100)
- [LinkedIn](https://www.linkedin.com/in/jefersonsehnem/)

---

Projeto criado por [Seu Nome].
