import sys
from collections import deque

def main():
    
    if len(sys.argv) != 5:
        print("Uso: python3 simulador.py <tamanho_cache> <tamanho_linha> <tamanho_grupo> <arquivo_entrada>")
        return

    tamanho_cache = int(sys.argv[1])
    tamanho_linha = int(sys.argv[2])
    tamanho_grupo = int(sys.argv[3])
    arquivo_entrada = sys.argv[4]

    # Verificações básicas
    if tamanho_cache % tamanho_linha != 0:
        print("Erro: O tamanho da cache deve ser múltiplo do tamanho de cada linha.")
        return

    if tamanho_grupo <= 0:
        print("Erro: O tamanho do grupo deve ser maior que zero.")
        return

    # Configurações da cache
    num_linhas = tamanho_cache // tamanho_linha
    num_conjuntos = num_linhas // tamanho_grupo

    # Inicializa a cache como uma lista de deques (para FIFO)
    cache = [deque(maxlen=tamanho_grupo) for _ in range(num_conjuntos)]

    # Estatísticas
    hits = 0
    misses = 0

    try:
        with open(arquivo_entrada, 'r') as f:
            acessos = [int(linha.strip(), 16) for linha in f if linha.strip().startswith("0x") and len(linha.strip()) == 10]
    except FileNotFoundError:
        print(f"Erro: Arquivo {arquivo_entrada} não encontrado.")
        return
    except ValueError:
        print("Erro: O arquivo de entrada deve conter apenas endereços hexadecimais válidos no formato 0xXXXXXXXX.")
        return

    # Abrir o arquivo de saída
    with open("output.txt", "w") as output:
        for endereco in acessos:
            bloco = endereco // tamanho_linha
            conjunto_idx = bloco % num_conjuntos

            conjunto = cache[conjunto_idx]

            if bloco in conjunto:
                hits += 1
            else:
                misses += 1
                conjunto.append(bloco)

            # Estado atual da cache
            output.write("================\n")
            output.write("IDX V ** ADDR **\n")
            for idx, line in enumerate(cache):
                for bloco_cache in line:
                    bloco_formatado = f"0x{bloco_cache:08X}"
                    output.write(f"{idx:03d} 1 {bloco_formatado}\n")
                if len(line) < tamanho_grupo:
                    for _ in range(tamanho_grupo - len(line)):
                        output.write(f"{idx:03d} 0\n")

        # Resultados finais
        output.write(f"#hits: {hits}\n")
        output.write(f"#miss: {misses}\n")

if __name__ == "__main__":
    main()