# PDFMerge

PDFMerge é uma ferramenta livre para unir arquivos PDF de forma simples e eficiente, com interface gráfica (Tkinter) e scripts automáticos/manual para mesclagem em lote. O projeto é distribuído sob licença MIT, com 90% do código gerado por IA e revisado pelo proprietário do repositório.

## Funcionalidades
- Interface gráfica amigável para unir PDFs (Tkinter)
- Adição de arquivos e pastas, reordenação, remoção e seleção de saída
- Scripts automáticos e manuais para mesclagem em lote
- Compatível com Windows, Linux e Mac (Python 3.7+)

## Instalação
1. Certifique-se de ter o Python 3.7 ou superior instalado.
2. Instale as dependências:

```bash
pip install -r requirements.txt
```

## Uso

### Interface Gráfica
Execute o arquivo principal para abrir a interface:

```bash
python mergePdf.py
```

- Adicione arquivos PDF individualmente ou por pasta
- Reordene, remova ou limpe a lista de PDFs
- Escolha o nome e local do arquivo de saída
- Clique em "Unir PDFs" para gerar o PDF final

### Script Automático
Edite `automatic.py` para definir a pasta dos PDFs. O script irá unir todos os PDFs da pasta, em ordem alfabética:

```python
PASTA = Path(r"C:\caminho\para\a\pasta")  # Altere para sua pasta
```
Execute:
```bash
python automatic.py
```

### Script Manual
Edite `manual.py` para definir a pasta e a ordem dos arquivos:

```python
PASTA = Path(r"C:\caminho\para\a\pasta")  # Altere para sua pasta
arquivos = [
    "01_capa.pdf",
    "02_conteudo.pdf",
    "03_anexos.pdf"
]
```
Execute:
```bash
python manual.py
```


## Como Contribuir

Contribuições são bem-vindas! Para colaborar com o PDFMerge:

1. Faça um fork deste repositório e clone para sua máquina.
2. Crie uma branch para sua feature ou correção:
    ```bash
    git checkout -b minha-nova-feature
    ```
3. Faça suas alterações e adicione testes, se aplicável.
4. Realize um commit descritivo:
    ```bash
    git commit -m "Descrição clara da mudança"
    ```
5. Envie para seu fork:
    ```bash
    git push origin minha-nova-feature
    ```
6. Abra um Pull Request detalhando sua contribuição.

Sugestões, correções de bugs, melhorias de documentação e novas funcionalidades são sempre apreciadas!

## Licença
Este software é distribuído sob a Licença MIT. Consulte o arquivo LICENSE para mais detalhes.

> 90% do código foi gerado por Inteligência Artificial e revisado pelo proprietário do repositório.

---

**Autor:** fernandosserra
