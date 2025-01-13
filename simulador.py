import sys

hits = 0
misses = 0

# Verifica se o número correto de argumentos foi passado
if len(sys.argv) != 5:
    sys.exit(1)

# Captura os argumentos da linha de comando
valor1 = int(sys.argv[1])
valor2 = int(sys.argv[2])  
valor3 = int(sys.argv[3])  
arquivo = sys.argv[4]      

try:
    with open(arquivo, 'r') as file:
        hexadecimais = file.readlines()

    # Remove espaços em branco e valida os endereços
    hexadecimais = [linha.strip() for linha in hexadecimais if linha.strip()]

    for endereco in hexadecimais:
        # Verifica o formato do endereço
        if not endereco.startswith("0x") or len(endereco) != 10:
            print(f"Endereço inválido encontrado: {endereco}")
            continue  # Pula endereços inválidos

        print(f"Endereço válido lido: {endereco}")

except FileNotFoundError:
    print(f"Erro: Arquivo '{arquivo}' não encontrado.")
    sys.exit(1)
except Exception as e:
    print(f"Erro ao ler o arquivo: {e}")
    sys.exit(1)