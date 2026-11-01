from pathlib import Path
import shutil
import pandas as pd
from src.dados import carregar_pedidos
ROOT=Path(__file__).parent
OUT=ROOT/"comparacao"
if OUT.exists(): shutil.rmtree(OUT)
OUT.mkdir()
df,modo=carregar_pedidos(); df["criado_em"]=pd.to_datetime(df["criado_em"])
paths={
 "CSV":OUT/"pedidos.csv",
 "Parquet Snappy":OUT/"pedidos_snappy.parquet",
 "Parquet Zstd":OUT/"pedidos_zstd.parquet",
}
df.to_csv(paths["CSV"],index=False)
df.to_parquet(paths["Parquet Snappy"],index=False,compression="snappy")
df.to_parquet(paths["Parquet Zstd"],index=False,compression="zstd")
base=paths["CSV"].stat().st_size
rows=[]
for nome,p in paths.items():
    size=p.stat().st_size
    rows.append({"formato":nome,"bytes":size,"KB":round(size/1024,1),"% do CSV":round(size/base*100,1)})
print("Modo:",modo)
print(pd.DataFrame(rows).to_string(index=False))
print("\nLembrete: menor arquivo não significa automaticamente menor tempo total de processamento.")
