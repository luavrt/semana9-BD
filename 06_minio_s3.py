from pathlib import Path
import os
from io import BytesIO
import boto3
import pandas as pd
from botocore.exceptions import ClientError
from dotenv import load_dotenv
load_dotenv()
ROOT=Path(__file__).parent
endpoint=os.getenv("MINIO_ENDPOINT","http://localhost:9000")
access=os.getenv("MINIO_ACCESS_KEY","minioadmin")
secret=os.getenv("MINIO_SECRET_KEY","minioadmin123")
bucket=os.getenv("MINIO_BUCKET","data-lake")
files=list((ROOT/"lake"/"silver"/"pedidos").rglob("*.parquet"))
if not files: raise SystemExit("Execute primeiro: python 01_parquet_particionado.py")
s3=boto3.client("s3",endpoint_url=endpoint,aws_access_key_id=access,aws_secret_access_key=secret,region_name="us-east-1")
try: s3.head_bucket(Bucket=bucket)
except ClientError: s3.create_bucket(Bucket=bucket)
f=files[0]
rel=f.relative_to(ROOT/"lake")
key=str(rel).replace("\\","/")
s3.upload_file(str(f),bucket,key)
print("Upload:",f.name,"→ s3://"+bucket+"/"+key)
resp=s3.list_objects_v2(Bucket=bucket,Prefix="silver/pedidos/")
print("\nOBJETOS:")
for obj in resp.get("Contents",[]): print(" ",obj["Key"],"|",obj["Size"],"bytes")
obj=s3.get_object(Bucket=bucket,Key=key)
df=pd.read_parquet(BytesIO(obj["Body"].read()))
print("\nLeitura de volta do objeto:",len(df),"linhas")
print(df.head().to_string(index=False))
print("\nMINIO / S3 OK")
