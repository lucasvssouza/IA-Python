
---
# Classificador de E-mails com IA - Case Prático
---

## 📄 Sobre o Projeto

Este projeto é uma solução web desenvolvida como parte de um case prático. A aplicação utiliza Inteligência Artificial para automatizar a análise e triagem de e-mails, com o objetivo de otimizar o fluxo de trabalho de equipes que lidam com um alto volume de comunicação diária.

A solução classifica os e-mails em categorias de **Produtivo** ou **Improdutivo** e sugere uma resposta automática adequada ao contexto, liberando a equipe de tarefas manuais e repetitivas.


## ✨ Funcionalidades Principais

  * **Análise de E-mail via Texto ou Arquivo:** Permite colar o conteúdo de um e-mail diretamente ou fazer o upload de arquivos `.txt` e `.pdf`.
  * **Classificação com IA:** Utiliza um Modelo de Linguagem Grande (LLM) para classificar o e-mail como "Produtivo" ou "Improdutivo".
  * **Geração de Resposta Automática:** A IA sugere uma resposta contextualizada com base no conteúdo e na classificação do e-mail.
  * **Interface Web Responsiva:** Front-end moderno e intuitivo, desenvolvido com Bootstrap 5, que se adapta a diferentes tamanhos de tela.
  * **Tema Claro e Escuro:** Botão para alternar entre os modos de visualização, com a preferência salva no navegador.
  * **Experiência de Usuário Aprimorada:** Validações de formulário em tempo real, indicadores de carregamento e alertas interativos com SweetAlert2.

-----

## 🚀 Link da Aplicação (Deploy)

A versão funcional da aplicação está hospedada e pode ser acessada através do seguinte link:

➡️ **[link](https://www.link.com)**

-----

## 🛠️ Tecnologias Utilizadas

O projeto foi construído com as seguintes tecnologias:

### **Backend**

  * **Python 3.12** Base para o backend.
  * **FastAPI:** Para a construção da API web de alta performance.
  * **LlamaIndex:** Para a orquestração e integração com o modelo de linguagem.
  * **Groq API:** Fornece acesso a LLMs de alta velocidade.
  * **Pydantic:** Para validação e modelagem de dados.
  * **Uvicorn:** Como servidor ASGI para rodar a aplicação.

### **Frontend**

  * **HTML5 / CSS3 / JavaScript** Base para o frontend.
  * **Bootstrap 5:** Para a criação de uma interface responsiva e moderna.
  * **jQuery:** Para manipulação do DOM e interatividade.
  * **SweetAlert2:** Para alertas e modais elegantes.

-----

## ⚙️ Instalação e Execução Local

Siga os passos abaixo para executar o projeto em seu ambiente local.

**1. Clone o Repositório:**

```bash
git clone https://github.com/lucasvssouza/IA-Python.git
cd nome-do-repositorio
```

**2. Crie e Ative o Ambiente Virtual:**

```bash
# Crie o ambiente virtual
python -m venv .venv

# Ative o ambiente (Linux/macOS)
source .venv/bin/activate

# Ative o ambiente (Windows)
.\.venv\Scripts\activate
```

**3. Instale as Dependências:**
O projeto usa `uv` para gerenciamento de pacotes. Se não o tiver, você pode instalar as dependências com `pip`.

```bash
# Com uv (recomendado)
uv sync

# Ou com pip, usando o arquivo requirements.txt
pip install -r requirements.txt
```

**4. Configure as Variáveis de Ambiente:**
Crie um arquivo chamado `.env` na raiz do projeto, copiando o exemplo `.env.example` ou adicionando a seguinte linha:

```
GROQ_API_KEY="sua_chave_de_api_da_groq"
```

*Substitua `sua_chave_de_api_da_groq` pela sua chave de API real.*

**5. Inicie o Servidor:**
Com as dependências instaladas e o ambiente configurado, inicie o servidor FastAPI.

```bash
uvicorn main:app --reload
```

**6. Acesse a Aplicação:**
Abra seu navegador e acesse a seguinte URL:
[http://127.0.0.1:8000](http://127.0.0.1:8000)

-----

## 📂 Estrutura do Projeto

```
├── main.py                # Ponto de entrada da API FastAPI e servidor web
├── requirements.txt       # Lista de dependências Python
├── .env                   # Arquivo para variáveis de ambiente (chave de API)
├── src/
│   ├── backend/
│   │   └── agents.py      # Lógica principal da IA, classificação e resposta
│   └── frontend/
│       ├── assets/        # Ícones e imagens
│       ├── css/
│       │   └── style.css  # Estilos customizados
│       ├── js/
│       │   └── script.js  # Lógica de interatividade do front-end
│       └── index.html     # Estrutura principal da página
└── README.md              # Este arquivo
```

-----

## ⚖️ Licença

Este projeto está sob a licença MIT.
