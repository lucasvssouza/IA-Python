from pathlib import Path
from typing import Optional
from llama_index.llms.groq import Groq
from llama_index.core import SimpleDirectoryReader, PromptTemplate
from pydantic import BaseModel, Field
from dotenv import load_dotenv

load_dotenv()

llm = Groq(model="openai/gpt-oss-120b", temperature=0.0)


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
    resultado: Optional[Invoice] | str = None


def email_arquivo(file_path: Path) -> Response:
    try:
        if file_path.suffix.lower() not in [".pdf", ".txt"]:
            return Response(
                status="erro",
                mensagem="Erro: Tipo de arquivo não suportado. Forneça um arquivo .pdf ou .txt.",
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
            mensagem="Arquivo lido com sucesso.",
            resultado=texto_completo.strip(),
        )
    except Exception as e:
        return Response(
            status="erro",
            mensagem=f"Erro: Ocorreu um problema ao ler o arquivo: {e}",
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
            mensagem="Nenhum texto ou arquivo foi fornecido.",
            resultado=None,
        )

    if not content:
        return Response(
            status="erro", mensagem="O conteúdo do e-mail está vazio.", resultado=None
        )

    try:
        template = """ Com base no e-mail fornecido abaixo, use a ferramenta 'Invoice' para extrair as informações solicitadas.
        ---
        {content} 
        ---"""
        template = PromptTemplate(template)

        invoice_result = llm.structured_predict(Invoice, template, content=content)

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
