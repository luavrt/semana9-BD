from pathlib import Path
import pyarrow.dataset as ds
ROOT=Path(__file__).parent
PATH=ROOT/"lake"/"silver"/"pedidos"
if not PATH.exists():
    raise SystemExit("Execute primeiro: python 01_parquet_particionado.py")
dataset=ds.dataset(PATH,format="parquet",partitioning="hive")
todos=list(dataset.get_fragments())
f_part=(ds.field("ano")==2025)&(ds.field("mes")==1)
selecionados=list(dataset.get_fragments(filter=f_part))
f_total=f_part & (ds.field("total")>=200)
tabela=dataset.to_table(filter=f_total,columns=["id","cliente_id","status","total"])
print("Fragmentos totais:",len(todos))
print("Fragmentos após filtro de partição ano=2025/mes=1:",len(selecionados))
print("Colunas realmente solicitadas:",tabela.column_names)
print("Linhas após total >= 200:",tabela.num_rows)
print("\nAMOSTRA:")
print(tabela.to_pandas().head(10).to_string(index=False))
print("\nINTERPRETAÇÃO:")
print("1) ano/mes permite PARTITION PRUNING (elimina arquivos).")
print("2) total>=200 pode usar PREDICATE PUSHDOWN/estatísticas do Parquet.")
print("3) columns=[...] faz COLUMN PRUNING (evita colunas não usadas).")
