from celery import shared_task


@shared_task
def my_task(arg1, arg2):
    # teste celery
    result = arg1 + arg2
    return result


@shared_task
def process_csv_chunk(chunk):
    return chunk
    # Processar uma parte do arquivo CSV
    # Retornar o resultado do processamento


def process_large_csv(file):
    # Dividir o arquivo CSV em partes menores
    chunks = divide_file_into_chunks(file)

    # Iniciar processos Celery para processar cada parte em paralelo
    results = [process_csv_chunk.delay(chunk) for chunk in chunks]

    # Aguardar o término de todos os processos Celery
    results = [result.get() for result in results]

    # Recombinar os resultados em um único conjunto de dados
    final_result = combine_results(results)

    return final_result


def divide_file_into_chunks(
    file, chunk_size=1024 * 1024
):  # Chunk size de 1MB (pode ser ajustado conforme necessário)
    chunks = []
    while True:
        chunk = file.read(chunk_size)
        if not chunk:
            break
        chunks.append(chunk)
    return chunks


def combine_results(results):
    # Aqui assumimos que os resultados são listas, você pode ajustar para outros tipos de dados
    combined_result = []

    for result in results:
        combined_result.extend(
            result
        )  # Se os resultados são listas, estendemos a lista combinada com cada resultado

    return combined_result
