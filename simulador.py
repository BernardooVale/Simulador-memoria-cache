import sys

def main():
    if len(sys.argv) != 5:
        print("Uso: python3 simulador.py <tamanho_cache> <tamanho_linha> <tamanho_grupo> <arquivo_entrada>")
        return

    tamCache = int(sys.argv[1])
    tamLinha = int(sys.argv[2])
    tamGrupo = int(sys.argv[3])
    arquivo_entrada = sys.argv[4]

    # Verificações básicas
    if tamCache % tamLinha != 0:
        print("Erro: O tamanho da cache deve ser múltiplo do tamanho de cada linha.")
        return

    if tamGrupo <= 0:
        print("Erro: O tamanho do grupo deve ser maior que zero.")
        return

    # Configurações da cache
    numLinhas = tamCache // tamLinha
    numConjuntos = numLinhas // tamGrupo

    # Inicializa a cache como uma lista de listas
    cache = [[None] * tamGrupo for _ in range(numConjuntos)]
    ponteiros = [0] * numConjuntos  # Ponteiros para substituição circular

    # Estatísticas
    hits = 0
    misses = 0

    try:
        with open(arquivo_entrada, 'r') as fonte:
            dados = [int(linha.strip(), 16) for linha in fonte]
    except FileNotFoundError:
        print(f"Erro: Arquivo {arquivo_entrada} não encontrado.")
        return
    except ValueError:
        print("Erro: O arquivo de entrada deve conter apenas endereços hexadecimais válidos no formato 0xXXXXXXXX.")
        return

    # Abrir o arquivo de saída
    with open("output.txt", "w") as saida:
        for endereco in dados:
            bloco = endereco // tamLinha
            conjunto_id = bloco % numConjuntos
            enderecoMEM = bloco // numConjuntos
            conjunto = cache[conjunto_id]

            if enderecoMEM in conjunto:
                hits += 1
            else:
                misses += 1
                posicao = ponteiros[conjunto_id]
                conjunto[posicao] = enderecoMEM  # Substitui na posição do ponteiro
                ponteiros[conjunto_id] = (posicao + 1) % tamGrupo  # Avança o ponteiro circular

            # Estado atual da cache
            saida.write("================\n")
            saida.write("IDX V * ADDR *\n")
            for idx, linha in enumerate(cache):
                for i in range(tamGrupo):
                    bloco_cache = linha[i]
                    if bloco_cache is not None:
                        bloco_formatado = f"0x{bloco_cache:08X}"
                        saida.write(f"{idx * tamGrupo + i:03d} 1 {bloco_formatado}\n")
                    else:
                        saida.write(f"{idx * tamGrupo + i:03d} 0\n")

        # Resultados finais
        saida.write("\n")
        saida.write(f"#hits: {hits}\n")
        saida.write(f"#miss: {misses}\n")

if __name__ == "__main__":
    main()