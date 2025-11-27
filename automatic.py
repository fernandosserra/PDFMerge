from PyPDF2 import PdfMerger
from pathlib import Path

# --- Defina aqui a pasta onde estão os PDFs ---
PASTA = Path(r"C:\caminho\para\a\pasta")  # <-- altere para sua pasta

merger = PdfMerger()

# Listar somente .pdf e ordenar (alfabeticamente)
pdfs = sorted([p for p in PASTA.iterdir() if p.is_file() and p.suffix.lower() == ".pdf"])

if not pdfs:
    raise SystemExit("Nenhum PDF encontrado na pasta.")

for p in pdfs:
    merger.append(str(p))

saida = PASTA / "resultado_automatico.pdf"
merger.write(str(saida))
merger.close()

print(f"Todos os PDFs da pasta foram unidos em: {saida}")