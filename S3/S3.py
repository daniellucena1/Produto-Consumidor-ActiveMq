import os
from dotenv import load_dotenv
import boto3
from botocore.exceptions import BotoCoreError, ClientError

# Lê variáveis do .env (se existir)
load_dotenv()

def get_s3():
    """Client S3 a partir do ambiente/.env (suporta AWS_PROFILE e endpoint opcional)."""
    profile = os.getenv("AWS_PROFILE")
    endpoint = os.getenv("AWS_S3_ENDPOINT_URL")
    session = boto3.session.Session(profile_name=profile) if profile else boto3.session.Session()
    return session.client("s3", endpoint_url=endpoint) if endpoint else session.client("s3")

def escolher(opcoes, titulo):
    """Mostra opções numeradas e retorna o item escolhido."""
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

    # 1) Buckets
    buckets = sorted([b["Name"] for b in s3.list_buckets().get("Buckets", [])])
    if not buckets:
        print("Nenhum bucket encontrado.")
        return
    bucket = escolher(buckets, "Buckets S3")

    # 2) (Opcional) prefixo simples para filtrar a listagem
    prefix = input("Prefixo para filtrar (ENTER para listar tudo): ").strip()

    # 3) Lista até 50 objetos (simples, sem paginação)
    resp = s3.list_objects_v2(Bucket=bucket, Prefix=prefix, MaxKeys=50)
    objs = resp.get("Contents", [])
    if not objs:
        print("Nenhum objeto encontrado (tente outro prefixo).")
        return

    # Monta lista de chaves legíveis
    chaves = [o["Key"] for o in objs]
    escolha_key = escolher(chaves, f"Arquivos em s3://{bucket}/{prefix}")

    # 4) Destino local (padrão: nome do arquivo)
    nome_default = os.path.basename(escolha_key) or "download.bin"
    destino = input(f"Salvar como [{nome_default}]: ").strip() or nome_default
    os.makedirs(os.path.dirname(destino) or ".", exist_ok=True)

    # 5) Download
    print(f"Baixando s3://{bucket}/{escolha_key} -> {destino} ...")
    try:
        s3.download_file(bucket, escolha_key, destino)
        print("Pronto!")
    except (BotoCoreError, ClientError) as e:
        print("Erro no download:", e)

if __name__ == "__main__":
    main()
