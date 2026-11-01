from pathlib import Path
import shutil
import pandas as pd
from src.dados import carregar_pedidos
ROOT=Path(__file__).parent
OUT=ROOT/"lake"/"silver"/"pedidos"
if OUT.exists(): shutil.rmtree(OUT)
df,modo=carregar_pedidos()
df["criado_em"]=pd.to_datetime(df["criado_em"])
df["status"]=df["status"].astype(str).str.lower().str.strip()
df["ano"]=df["criado_em"].dt.year
df["mes"]=df["criado_em"].dt.month
df.to_parquet(OUT,partition_cols=["ano","mes"],compression="zstd",index=False,engine="pyarrow")
files=sorted(OUT.rglob("*.parquet"))
print("Modo:",modo)
print("Linhas escritas:",len(df))
print("Arquivos Parquet:",len(files))
print("\nPARTIÇÕES CRIADAS (primeiras 20):")
for f in files[:20]: print(" ",f.relative_to(ROOT))
print("\nPARQUET PARTICIONADO OK")
