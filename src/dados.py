from pathlib import Path
import os
import numpy as np
import pandas as pd
from dotenv import load_dotenv

load_dotenv()
ROOT = Path(__file__).resolve().parents[1]
DEMO = ROOT / "dados_demo"

def gerar_demo():
    DEMO.mkdir(exist_ok=True)
    rng = np.random.default_rng(42)
    cidades = ["São Paulo", "Teresina", "Fortaleza", "Recife", "Salvador"]
    clientes = pd.DataFrame({
        "id": range(1, 121),
        "nome": [f"Cliente {i:03d}" for i in range(1,121)],
        "email": [f"cliente{i:03d}@exemplo.com" for i in range(1,121)],
        "cidade": rng.choice(cidades,120,p=[.30,.20,.18,.17,.15]),
    })
    n=1800
    inicio = pd.Timestamp("2024-01-01")
    dias = rng.integers(0, 545, n)
    pedidos = pd.DataFrame({
        "id": range(1,n+1),
        "cliente_id": rng.integers(1,121,n),
        "status": rng.choice(["entregue","cancelado","pago","enviado"],n,p=[.57,.08,.18,.17]),
        "total": np.round(rng.gamma(2.2,85,n)+15,2),
        "criado_em": inicio + pd.to_timedelta(dias,unit="D"),
    })
    clientes.to_csv(DEMO/"clientes.csv",index=False)
    pedidos.to_csv(DEMO/"pedidos.csv",index=False)
    return clientes,pedidos

def _engine():
    url=os.getenv("DATABASE_URL","").strip()
    if not url:
        return None
    try:
        from sqlalchemy import create_engine
        return create_engine(url,pool_pre_ping=True)
    except Exception as exc:
        print("AVISO: não foi possível preparar a conexão PostgreSQL; continuando em MODO DEMO.")
        print("Motivo:",type(exc).__name__,str(exc).splitlines()[0][:180])
        return None

def carregar_clientes():
    eng=_engine()
    if eng is not None:
        try:
            df=pd.read_sql("SELECT id, nome, email, cidade FROM clientes ORDER BY id",eng)
            if not df.empty:
                return df,"POSTGRESQL"
            print("AVISO: tabela clientes está vazia; continuando em MODO DEMO.")
        except Exception as exc:
            print("AVISO: PostgreSQL falhou; continuando em MODO DEMO.")
            print("Motivo:",type(exc).__name__,str(exc).splitlines()[0][:180])
    if not (DEMO/"clientes.csv").exists(): gerar_demo()
    return pd.read_csv(DEMO/"clientes.csv"),"DEMO"

def carregar_pedidos():
    eng=_engine()
    if eng is not None:
        try:
            df=pd.read_sql("SELECT id, cliente_id, status, total, criado_em FROM pedidos ORDER BY criado_em",eng)
            if not df.empty:
                return df,"POSTGRESQL"
            print("AVISO: tabela pedidos está vazia; continuando em MODO DEMO.")
        except Exception as exc:
            print("AVISO: PostgreSQL falhou; continuando em MODO DEMO.")
            print("Motivo:",type(exc).__name__,str(exc).splitlines()[0][:180])
    if not (DEMO/"pedidos.csv").exists(): gerar_demo()
    df=pd.read_csv(DEMO/"pedidos.csv",parse_dates=["criado_em"])
    return df,"DEMO"
