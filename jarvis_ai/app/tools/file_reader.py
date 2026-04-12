# ============================================================
# app/tools/file_reader.py
# Ferramenta para ler arquivos enviados pelo usuário
# Será usado nas próximas fases do projeto
# ============================================================

import os


def read_text_file(filepath: str) -> str:
    """
    Lê um arquivo de texto (.txt ou .md) e retorna seu conteúdo.
    
    Args:
        filepath: Caminho completo do arquivo
    
    Returns:
        Conteúdo do arquivo como string
    
    Raises:
        FileNotFoundError: Se o arquivo não existir
        ValueError: Se a extensão não for suportada
    """
    if not os.path.exists(filepath):
        raise FileNotFoundError(f"Arquivo não encontrado: {filepath}")

    extension = os.path.splitext(filepath)[1].lower()
    if extension not in [".txt", ".md"]:
        raise ValueError(f"Extensão não suportada: {extension}. Use .txt ou .md")

    with open(filepath, "r", encoding="utf-8") as f:
        return f.read()


def get_file_info(filepath: str) -> dict:
    """Retorna informações básicas sobre um arquivo."""
    if not os.path.exists(filepath):
        raise FileNotFoundError(f"Arquivo não encontrado: {filepath}")

    stat = os.stat(filepath)
    return {
        "name": os.path.basename(filepath),
        "size_kb": round(stat.st_size / 1024, 2),
        "extension": os.path.splitext(filepath)[1],
    }
