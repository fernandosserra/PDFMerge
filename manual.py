from PyPDF2 import PdfMerger
from pathlib import Path

# --- Defina aqui a pasta onde estão os PDFs ---
PASTA = Path(r"C:\caminho\para\a\pasta")  # <-- altere para sua pasta

# Lista de nomes (ordem desejada). Apenas nomes de arquivo (ou caminhos relativos à PASTA).
arquivos = [
    "01_capa.pdf",
    "02_conteudo.pdf",
    "03_anexos.pdf"
]

merger = PdfMerger()

for nome in arquivos:
    caminho = PASTA / nome
    if caminho.exists():
        merger.append(str(caminho))
    else:
        raise FileNotFoundError(f"Arquivo não encontrado: {caminho}")

saida = PASTA / "resultado_manual.pdf"
merger.write(str(saida))
merger.close()

print(f"PDF criado em: {saida}")