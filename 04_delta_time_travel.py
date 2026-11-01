from pathlib import Path
import shutil
import pandas as pd
from deltalake import DeltaTable, write_deltalake
from src.dados import carregar_clientes, carregar_pedidos
ROOT=Path(__file__).parent
PATH=ROOT/"lake"/"gold"/"features_cliente"
if PATH.exists(): shutil.rmtree(PATH)
clientes,mc=carregar_clientes(); pedidos,mp=carregar_pedidos()
pedidos["criado_em"]=pd.to_datetime(pedidos["criado_em"])
features=(pedidos.groupby("cliente_id").agg(total_pedidos=("id","count"),total_gasto=("total","sum"),ultimo_pedido=("criado_em","max")).reset_index())
features["total_gasto"]=features["total_gasto"].round(2)
if features.empty:
    raise SystemExit("Não há pedidos suficientes para criar features. Verifique a fonte ou use o MODO DEMO.")
# Reserve até 5 clientes para a segunda versão. Assim o exemplo funciona
# também quando o banco da turma tem menos de 45 clientes.
if len(features) > 1:
    corte = min(40, len(features)-1)
    v0 = features.iloc[:corte].copy()
    novos = features.iloc[corte:corte+5].copy()
else:
    v0 = features.copy()
    novos = features.copy()
    novos["cliente_id"] = novos["cliente_id"].astype(int) + 100000
write_deltalake(str(PATH),v0,mode="overwrite")
write_deltalake(str(PATH),novos,mode="append")
dt=DeltaTable(str(PATH))
atual=dt.to_pandas().sort_values("cliente_id")
antiga=DeltaTable(str(PATH),version=0).to_pandas().sort_values("cliente_id")
print("Origem:",mp)
print("Versão atual:",dt.version(),"| linhas:",len(atual))
print("Versão 0     : 0 | linhas:",len(antiga))
print("\nHISTÓRICO (mais recente primeiro):")
for h in dt.history(): print(" v",h.get("version"),"|",h.get("operation"),"|",h.get("timestamp"))
print("\nTIME TRAVEL OK: v0 continua acessível mesmo após nova versão.")
