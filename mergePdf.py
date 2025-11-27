"""
merge_pdfs_tk.py
Interface simples para unir PDFs com PyPDF2 e Tkinter.

Dependências:
    pip install PyPDF2
Tkinter já vem com o Python (versões oficiais).
"""

import sys
from pathlib import Path
import tkinter as tk
from tkinter import ttk, filedialog, messagebox
from PyPDF2 import PdfMerger

class PDFMergerApp(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("Unir PDFs — Merge Tool")
        self.geometry("720x420")
        self.minsize(640, 360)

        # Lista interna de caminhos (Path objects)
        self.pdf_list = []

        self.create_widgets()

    def create_widgets(self):
        frm = ttk.Frame(self, padding=10)
        frm.pack(fill="both", expand=True)

        # Botões no topo
        top_row = ttk.Frame(frm)
        top_row.pack(fill="x", pady=(0,8))

        ttk.Button(top_row, text="Adicionar arquivos", command=self.add_files).pack(side="left", padx=4)
        ttk.Button(top_row, text="Adicionar pasta (todos PDFs)", command=self.add_folder).pack(side="left", padx=4)
        ttk.Button(top_row, text="Remover selecionado", command=self.remove_selected).pack(side="left", padx=4)
        ttk.Button(top_row, text="Limpar lista", command=self.clear_list).pack(side="left", padx=4)

        # Listbox com scrollbar para mostrar arquivos e permitir reordenar
        list_frame = ttk.Frame(frm)
        list_frame.pack(fill="both", expand=True)

        self.listbox = tk.Listbox(list_frame, selectmode="extended")
        self.listbox.pack(side="left", fill="both", expand=True)

        scrollbar = ttk.Scrollbar(list_frame, orient="vertical", command=self.listbox.yview)
        scrollbar.pack(side="left", fill="y")
        self.listbox.config(yscrollcommand=scrollbar.set)

        # Painel de botões para mover
        move_frame = ttk.Frame(frm)
        move_frame.pack(fill="x", pady=8)

        ttk.Button(move_frame, text="Subir ↑", command=self.move_up).pack(side="left", padx=4)
        ttk.Button(move_frame, text="Descer ↓", command=self.move_down).pack(side="left", padx=4)
        ttk.Button(move_frame, text="Selecionar saída...", command=self.choose_output).pack(side="left", padx=12)

        # Linha de saída (arquivo final)
        out_frame = ttk.Frame(frm)
        out_frame.pack(fill="x", pady=(8,0))

        ttk.Label(out_frame, text="Arquivo de saída:").pack(side="left")
        self.output_var = tk.StringVar(value="resultado_unido.pdf")
        self.output_entry = ttk.Entry(out_frame, textvariable=self.output_var)
        self.output_entry.pack(side="left", fill="x", expand=True, padx=6)

        # Botão de unir
        bottom = ttk.Frame(frm)
        bottom.pack(fill="x", pady=10)
        ttk.Button(bottom, text="Unir PDFs", command=self.merge_pdfs, width=20).pack(side="left", padx=6)
        ttk.Button(bottom, text="Fechar", command=self.quit).pack(side="right", padx=6)

    # ---------- ações ----------
    def add_files(self):
        files = filedialog.askopenfilenames(title="Selecione arquivos PDF",
                                            filetypes=[("PDF files", "*.pdf")])
        for f in files:
            p = Path(f)
            if p not in self.pdf_list:
                self.pdf_list.append(p)
                self.listbox.insert(tk.END, str(p.name))

    def add_folder(self):
        folder = filedialog.askdirectory(title="Selecione a pasta com PDFs")
        if not folder:
            return
        folder_path = Path(folder)
        pdfs = sorted([p for p in folder_path.iterdir() if p.is_file() and p.suffix.lower() == ".pdf"])
        if not pdfs:
            messagebox.showinfo("Nenhum PDF", "Não foram encontrados PDFs nessa pasta.")
            return
        for p in pdfs:
            if p not in self.pdf_list:
                self.pdf_list.append(p)
                self.listbox.insert(tk.END, str(p.name))

    def remove_selected(self):
        sel = list(self.listbox.curselection())
        if not sel:
            return
        # remover da lista interna em ordem reversa para manter índices válidos
        for i in reversed(sel):
            del self.pdf_list[i]
            self.listbox.delete(i)

    def clear_list(self):
        self.pdf_list.clear()
        self.listbox.delete(0, tk.END)

    def move_up(self):
        sel = self.listbox.curselection()
        if not sel:
            return
        for i in sel:
            if i == 0:
                continue
            # swap in listbox
            above = self.listbox.get(i-1)
            current = self.listbox.get(i)
            self.listbox.delete(i-1, i)
            self.listbox.insert(i-1, current)
            self.listbox.insert(i, above)
            # swap in internal list
            self.pdf_list[i-1], self.pdf_list[i] = self.pdf_list[i], self.pdf_list[i-1]
        # recolocar seleção (aprox)
        self.listbox.selection_clear(0, tk.END)
        for i in [max(0, idx-1) for idx in sel]:
            self.listbox.selection_set(i)

    def move_down(self):
        sel = self.listbox.curselection()
        if not sel:
            return
        # processar em ordem reversa para mover corretamente
        for i in reversed(sel):
            if i >= self.listbox.size() - 1:
                continue
            below = self.listbox.get(i+1)
            current = self.listbox.get(i)
            self.listbox.delete(i, i+1)
            self.listbox.insert(i, below)
            self.listbox.insert(i+1, current)
            self.pdf_list[i], self.pdf_list[i+1] = self.pdf_list[i+1], self.pdf_list[i]
        # recolocar seleção (aprox)
        self.listbox.selection_clear(0, tk.END)
        for i in [min(self.listbox.size()-1, idx+1) for idx in sel]:
            self.listbox.selection_set(i)

    def choose_output(self):
        f = filedialog.asksaveasfilename(defaultextension=".pdf",
                                         filetypes=[("PDF files", "*.pdf")],
                                         title="Salvar arquivo como")
        if f:
            self.output_var.set(f)

    def merge_pdfs(self):
        if not self.pdf_list:
            messagebox.showwarning("Sem arquivos", "Adicione pelo menos um PDF para unir.")
            return

        output_path = Path(self.output_var.get()).expanduser()
        # Se o nome informado for somente um nome (sem pasta), colocar no diretório atual
        if not output_path.parent.exists():
            try:
                output_path.parent.mkdir(parents=True, exist_ok=True)
            except Exception as e:
                messagebox.showerror("Erro", f"Não foi possível criar pasta de saída:\n{e}")
                return

        merger = PdfMerger()
        try:
            for p in self.pdf_list:
                merger.append(str(p))
            merger.write(str(output_path))
            merger.close()
            messagebox.showinfo("Sucesso", f"PDF criado em:\n{output_path}")
        except Exception as e:
            messagebox.showerror("Erro ao unir", f"Ocorreu um erro ao unir os PDFs:\n{e}")
            try:
                merger.close()
            except:
                pass


if __name__ == "__main__":
    # Verificação simples: PyPDF2 importado?
    try:
        app = PDFMergerApp()
        app.mainloop()
    except Exception as e:
        messagebox.showerror("Erro fatal", f"Aplicação terminou com erro:\n{e}")
        sys.exit(1)