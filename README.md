# Banco de Dados — Semana 09 — Armazenamento Distribuído

Projeto prático guiado para VS Code.

## Ordem

1. `python 00_testar_ambiente.py` — preparação do ambiente
2. `python 01_parquet_particionado.py` — checkpoint 1
3. `python 02_leitura_seletiva.py` — checkpoint 2
4. `python 03_comparar_formatos.py` — checkpoint 3
5. opcional neste ponto: `docker compose up -d` e `python 06_minio_s3.py` — MinIO/S3
6. `python 04_delta_time_travel.py` — checkpoint 4
7. `python 05_delta_merge.py` — checkpoint 5

> O arquivo se chama `06_minio_s3.py` porque é uma extensão opcional. Na sequência didática da aula ele pode ser executado logo após o comparativo de formatos, antes de entrar em Delta Lake.

## Windows / VS Code

```powershell
python -m venv .venv
.\.venv\Scripts\Activate.ps1
python -m pip install -r requirements.txt
python 00_testar_ambiente.py
```

Se a política do PowerShell bloquear a ativação:

```powershell
Set-ExecutionPolicy -Scope Process -ExecutionPolicy Bypass
.\.venv\Scripts\Activate.ps1
```

## PostgreSQL ou modo DEMO

Copie `.env.example` para `.env` e preencha `DATABASE_URL` se a conexão da turma estiver disponível. Se ela estiver vazia ou falhar, os scripts usam um dataset local determinístico para a prática continuar.

## MinIO

```powershell
docker compose up -d
```

Console: `http://localhost:9001`

- usuário: `minioadmin`
- senha: `minioadmin123`

O MinIO é opcional para a continuidade da aula: se Docker não estiver disponível, faça os scripts 00–05 e registre a limitação no caderno.
