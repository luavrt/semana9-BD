from pathlib import Path
import sys
print("=== BANCO DE DADOS · SEMANA 09 ===")
print("Python:",sys.version.split()[0])
try:
    import pandas as pd, pyarrow, deltalake, boto3, sqlalchemy
    print("pandas:",pd.__version__)
    print("pyarrow:",pyarrow.__version__)
    print("deltalake:",getattr(deltalake,"__version__","instalado"))
    print("boto3:",boto3.__version__)
    print("SQLAlchemy:",sqlalchemy.__version__)
except Exception as exc:
    print("ERRO DE DEPENDÊNCIA:",exc)
    print("Rode: python -m pip install -r requirements.txt")
    raise SystemExit(1)
from src.dados import carregar_clientes, carregar_pedidos
c,mc=carregar_clientes(); p,mp=carregar_pedidos()
print("\nOrigem clientes:",mc,"| linhas:",len(c))
print("Origem pedidos :",mp,"| linhas:",len(p))
print("Período:",pd.to_datetime(p.criado_em).min(),"→",pd.to_datetime(p.criado_em).max())
print("Status:",sorted(p.status.astype(str).unique().tolist()))
print("\nAMBIENTE OK")
