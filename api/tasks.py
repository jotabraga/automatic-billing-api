from celery import shared_task
from pyboleto.bank.bradesco import BoletoBradesco
from pyboleto.pdf import BoletoPDF
import datetime


@shared_task
def process_csv_lote(lote):
    for line in lote:
        boleto = generate_boleto(line.decode("utf-8"))


def divide_file_into_chunks(file, chunk_size=10000):  # Chunk size de 1MB
    chunks = []
    while True:
        chunk = file.read(chunk_size)
        if not chunk:
            break
        chunks.append(chunk)
    return chunks


def combine_results(results):
    combined_result = []

    for result in results:
        combined_result.extend(result)

    return combined_result


def generate_boleto(row):
    print(row)

    # name = row["name"]
    # government_id = row["governmentId"]
    # email = row["email"]
    # debt_amount = row["debtAmount"]
    # debt_due_date = row["debtDueDate"]
    # debt_id = row["debtID"]
    listaDadosBradesco = []

    for i in range(2):
        d = BoletoBradesco()
        d.carteira = "06"  # dado do bradesco
        d.cedente = "Empresa ACME LTDA"
        d.cedente_documento = "102.323.777-01"
        d.cedente_endereco = (
            "Rua Acme, 123 - Centro - Sao Paulo/SP - " + "CEP: 12345-678"
        )
        d.agencia_cedente = "0278-0"
        d.conta_cedente = "43905-3"

        d.data_vencimento = datetime.date(2011, 1, 25)
        d.data_documento = datetime.date(2010, 2, 12)
        d.data_processamento = datetime.date(2010, 2, 12)

        d.instrucoes = [
            "- Linha 1",
            "- Sr Caixa, cobrar multa de 2% após o vencimento",
            "- Receber até 10 dias após o vencimento",
        ]
        d.demonstrativo = [
            "- Serviço Teste R$ 5,00",
            "- Total R$ 5,00",
        ]
        d.valor_documento = 2158.41

        d.nosso_numero = "1112011668"
        d.numero_documento = "1112011668"
        d.sacado = [
            "Cliente Teste %d" % (i + 1),
            "Rua Desconhecida, 00/0000 - Não Sei - Cidade - Cep. 00000-000",
            "",
        ]
        listaDadosBradesco.append(d)

    boleto = BoletoPDF("boleto-bradesco-formato-normal-teste.pdf")
    for i in range(len(listaDadosBradesco)):
        boleto.drawBoleto(listaDadosBradesco[i])
        boleto.nextPage()
    # boleto.save()
