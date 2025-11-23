# MarkItDown Converter (modo local)

Conversor simples em Python que lê arquivos da pasta `uploads/` e salva o Markdown em `results/` usando a biblioteca [MarkItDown](https://github.com/microsoft/markitdown).

## Requisitos
- Python 3.11+
- Dependências: `pip install -r apps/processor/requirements.txt`  
  - Para converter `.docx`, o `requirements.txt` já inclui `markitdown[pdf,docx]`.

## Como usar
1) Instale as dependências:
   ```bash
   pip install -r apps/processor/requirements.txt
   ```
2) Coloque os arquivos a serem convertidos em `uploads/` (suporta: PDF, DOCX, TXT, MD, RTF, HTML).
3) Rode o worker:
   ```bash
   python apps/processor/worker.py
   ```
4) Os arquivos convertidos em Markdown ficarão em `results/` com o mesmo nome-base do original.
5) O processo termina quando todos os arquivos suportados forem processados. Falhas são reportadas no console.

## Estrutura de pastas (essencial)
```
apps/
  processor/
    convert_watch.py   # lógica de conversão
    worker.py          # ponto de entrada
    requirements.txt
uploads/               # entrada (não versionar)
results/               # saída (não versionar)
```

## Observações
- Se a conversão de DOCX falhar por falta de dependência, reinstale: `pip install "markitdown[pdf,docx]>=0.1.3"`.
- Pastas de trabalho como `uploads/`, `results/` e caches (`__pycache__`) não devem ser versionadas.
