from pathlib import Path
import pandas as pd
import pyarrow as pa
from deltalake import DeltaTable
ROOT=Path(__file__).parent
PATH=ROOT/"lake"/"gold"/"features_cliente"
if not PATH.exists(): raise SystemExit("Execute primeiro: python 04_delta_time_travel.py")
dt=DeltaTable(str(PATH))
atual=dt.to_pandas().sort_values("cliente_id")
alvo=int(atual.iloc[0]["cliente_id"])
antes=atual[atual.cliente_id==alvo].copy()
novo_id=int(atual.cliente_id.max())+100
fonte=pd.DataFrame({
 "cliente_id":[alvo,novo_id],
 "total_pedidos":[int(antes.iloc[0].total_pedidos)+1,1],
 "total_gasto":[float(antes.iloc[0].total_gasto)+500.0,250.0],
 "ultimo_pedido":[pd.Timestamp("2025-06-30"),pd.Timestamp("2025-06-30")],
})
source=pa.Table.from_pandas(fonte,preserve_index=False)
metrics=(dt.merge(source=source,predicate="target.cliente_id = source.cliente_id",source_alias="source",target_alias="target")
 .when_matched_update(updates={
   "total_pedidos":"source.total_pedidos",
   "total_gasto":"source.total_gasto",
   "ultimo_pedido":"source.ultimo_pedido"})
 .when_not_matched_insert(updates={
   "cliente_id":"source.cliente_id","total_pedidos":"source.total_pedidos",
   "total_gasto":"source.total_gasto","ultimo_pedido":"source.ultimo_pedido"})
 .execute())
dt=DeltaTable(str(PATH)); depois=dt.to_pandas().sort_values("cliente_id")
print("Cliente atualizado:",alvo)
print("ANTES:\n",antes.to_string(index=False))
print("\nDEPOIS:\n",depois[depois.cliente_id==alvo].to_string(index=False))
print("\nCliente novo inserido:\n",depois[depois.cliente_id==novo_id].to_string(index=False))
print("\nVersão após MERGE:",dt.version())
print("Métricas MERGE:",metrics)
print("\nMERGE OK — update + insert na mesma operação lógica.")
