# --- Importações de Bibliotecas ---
import os
import nltk
from nltk.corpus import stopwords
from nltk.stem import WordNetLemmatizer
from nltk.tokenize import word_tokenize
from pathlib import Path
from typing import Optional
from llama_index.llms.groq import Groq
from llama_index.core import SimpleDirectoryReader, PromptTemplate
from pydantic import BaseModel, Field
from dotenv import load_dotenv
# --- Importações de Bibliotecas ---


# --- Configuração Inicial ---
load_dotenv()

# Inicializa o cliente do modelo de linguagem grande (LLM) da Groq.
llm = Groq(model="gemma2-9b-it", temperature=0.0)
# --- Configuração Inicial ---


# --- Configuração do Pré-processamento de NLP ---
NLP_PREPROCESSING = os.getenv("NLP_PREPROCESSING", "false").lower() == "true"
NLP_LANGUAGE = os.getenv("NLP_LANGUAGE", "portuguese").lower()

if NLP_PREPROCESSING:
    try:
        nltk.data.find("tokenizers/punkt")
        nltk.data.find("corpora/stopwords")
        nltk.data.find("corpora/wordnet")
        nltk.data.find("corpora/omw-1.4")
    except LookupError:
        print("A baixar recursos necessários do NLTK...")
        nltk.download("punkt", quiet=True)
        nltk.download("stopwords", quiet=True)
        nltk.download("wordnet", quiet=True)
        nltk.download("omw-1.4", quiet=True)
        print("Recursos do NLTK baixados com sucesso.")
# --- Configuração do Pré-processamento de NLP ---


# --- Modelos de Dados ---
class Invoice(BaseModel):
    classe: int = Field(
        description="Classifique o email sendo 1 para email improdutivo e 2 para e-mail produtivo, no meio corporativo."
    )
    texto: str = Field(
        description="Gere uma resposta cordial e profissional para o e-mail, agindo como um representante da empresa que o recebeu. Não responda como se fosse o autor do e-mail e sim quem o recebeu."
    )


class Response(BaseModel):
    status: str
    mensagem: str
    resultado: Optional[Invoice | str] = None


# --- Modelos de Dados ---


# --- Funções de Processamento ---
def preprocessar_texto_nlp(texto: str) -> str:
    stop_words = set(stopwords.words(NLP_LANGUAGE))
    lemmatizer = WordNetLemmatizer()
    tokens = word_tokenize(texto.lower(), language=NLP_LANGUAGE)

    tokens_processados = [
        lemmatizer.lemmatize(palavra)
        for palavra in tokens
        if palavra.isalpha() and palavra not in stop_words
    ]
    return " ".join(tokens_processados)


def email_arquivo(file_path: Path) -> Response:
    try:
        if file_path.suffix.lower() not in [".pdf", ".txt"]:
            return Response(
                status="erro",
                mensagem="Erro: Tipo de ficheiro não suportado. Forneça um ficheiro .pdf ou .txt.",
                resultado=None,
            )

        reader = SimpleDirectoryReader(
            input_dir=file_path.parent, required_exts=[file_path.suffix]
        )

        documents = reader.load_data()
        texto_completo = ""
        for doc in documents:
            if Path(doc.metadata.get("file_path")).name == file_path.name:
                texto_completo += doc.text + "\n"
        return Response(
            status="sucesso",
            mensagem="Ficheiro lido com sucesso.",
            resultado=texto_completo.strip(),
        )
    except Exception as e:
        return Response(
            status="erro",
            mensagem=f"Erro: Ocorreu um problema ao ler o ficheiro: {e}",
            resultado=None,
        )


def verificar_email(
    email_text: Optional[str] = None,
    email_file_path: Optional[str] = None,
) -> Response:
    content = ""
    if email_text:
        content = email_text
    elif email_file_path:
        response_arquivo = email_arquivo(Path(email_file_path))
        if response_arquivo.status == "erro":
            return response_arquivo
        content = response_arquivo.resultado
    else:
        return Response(
            status="erro",
            mensagem="Nenhum texto ou ficheiro foi fornecido.",
            resultado=None,
        )

    if not content:
        return Response(
            status="erro", mensagem="O conteúdo do e-mail está vazio.", resultado=None
        )

    if NLP_PREPROCESSING:
        print("INFO: Pré-processamento de NLP ativado.")
        content = preprocessar_texto_nlp(content)
        print(f"INFO: Conteúdo após NLP: {content}")

    try:
        template = """ Com base no e-mail fornecido abaixo, use a ferramenta 'Invoice' para extrair as informações solicitadas.
        ---
        {content}
        ---"""
        prompt = PromptTemplate(template)
        invoice_result = llm.structured_predict(Invoice, prompt, content=content)
        return Response(
            status="sucesso",
            mensagem="E-mail verificado e classificado com sucesso.",
            resultado=invoice_result,
        )
    except Exception as e:
        return Response(
            status="erro",
            mensagem=f"Falha ao processar o e-mail com a IA: {str(e)}",
            resultado=None,
        )


# --- Funções de Processamento ---
