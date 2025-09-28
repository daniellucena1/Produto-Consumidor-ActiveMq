import os
from dotenv import load_dotenv
import boto3
from botocore.exceptions import BotoCoreError, ClientError

load_dotenv()

def get_s3():
    profile = os.getenv("AWS_PROFILE")
    session = boto3.session.Session(profile_name=profile) if profile else boto3.session.Session()
    return session.client("s3")

def escolher(opcoes, titulo):
    print(f"\n== {titulo} ==")
    for i, x in enumerate(opcoes, 1):
        print(f"{i:>2}. {x}")
    while True:
        s = input(f"Escolha [1-{len(opcoes)}]: ").strip()
        if s.isdigit() and 1 <= int(s) <= len(opcoes):
            return opcoes[int(s)-1]
        print("Opção inválida.")

def main():
    s3 = get_s3()

    buckets = sorted([b["Name"] for b in s3.list_buckets().get("Buckets", [])])
    if not buckets:
        print("Nenhum bucket encontrado.")
        return
    bucket = escolher(buckets, "Buckets S3")

    pasta = "assets"
    if not os.path.isdir(pasta):
        print(f"Pasta '{pasta}' não encontrada.")
        return

    arquivos = sorted([f for f in os.listdir(pasta) if os.path.isfile(os.path.join(pasta, f))])
    if not arquivos:
        print(f"Nenhum arquivo encontrado em '{pasta}'.")
        return

    escolha_local = escolher(arquivos, f"Arquivos locais em {pasta}/")
    caminho_local = os.path.join(pasta, escolha_local)

    key_default = "Docs/" + escolha_local
    key = input(f"Salvar no S3 como [{key_default}]: ").strip() or key_default

    print(f"Enviando {caminho_local} -> s3://{bucket}/{key} ...")
    try:
        s3.upload_file(caminho_local, bucket, key)
        print("Upload concluído!")
    except (BotoCoreError, ClientError) as e:
        print("Erro no upload:", e)

if __name__ == "__main__":
    main()
