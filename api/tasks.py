from celery import shared_task
from pyboleto.bank.bradesco import BoletoBradesco
from pyboleto.pdf import BoletoPDF
import datetime
from django.conf import settings
from django.core.mail import EmailMultiAlternatives


@shared_task
def process_csv_lote(lote):
    for line in lote:
        boleto = generate_boleto(line.decode("utf-8"))
        send_mail(boleto, line)


def generate_boleto(row):
    government_id = row["governmentId"]
    debt_amount = row["debtAmount"]
    debt_due_date = row["debtDueDate"]
    debt_id = row["debtID"]
    listaDadosBradesco = []

    for i in range(2):
        new_boleto = BoletoBradesco()
        new_boleto.carteira = "06"  # dado do bradesco
        new_boleto.cedente = "Kanastra"
        new_boleto.cedente_documento = government_id
        new_boleto.cedente_endereco = (
            "Rua Acme, 123 - Centro - Sao Paulo/SP - " + "CEP: 12345-678"
        )
        new_boleto.agencia_cedente = "0278-0"
        new_boleto.conta_cedente = "43905-3"

        new_boleto.data_vencimento = datetime.date(debt_due_date)
        new_boleto.data_documento = datetime.date(2010, 2, 12)
        new_boleto.data_processamento = datetime.date(2010, 2, 12)

        new_boleto.instrucoes = [
            "- Linha 1",
            "- Sr Caixa, cobrar multa de 2% após o vencimento",
            "- Receber até 10 dias após o vencimento",
        ]
        new_boleto.demonstrativo = [
            "- Serviço Teste R$ 5,00",
            "- Total R$ 5,00",
        ]
        new_boleto.valor_documento = debt_amount

        new_boleto.nosso_numero = debt_id
        new_boleto.numero_documento = debt_id
        new_boleto.sacado = [
            "Cliente Teste %d" % (i + 1),
            "Rua Desconhecida, 00/0000 - Não Sei - Cidade - Cep. 00000-000",
            "",
        ]
        listaDadosBradesco.append(new_boleto)

    boleto = BoletoPDF("boleto-bradesco-formato-normal-teste.pdf")
    for i in range(len(listaDadosBradesco)):
        boleto.drawBoleto(listaDadosBradesco[i])
        boleto.nextPage()
    boleto.save()
    return boleto


def send_mail(boleto, row):
    name = row["name"]
    email = row["email"]

    subject = f"Email de cobrança para {name}"
    body = "Pague seu boleto e evite cobranças"
    sendmail = EmailMultiAlternatives(
        subject, body, settings.DEFAULT_FROM_EMAIL, to=[email]
    )
    sendmail.attach("emailpdf_{}".format(name) + ".pdf", boleto, "application/pdf")
    sendmail.content_subtype = "pdf"
    sendmail.decode = "utf-8"
    return sendmail.send()


# get results of all tasks, its important to do in the future:
# def combine_results(results):
#     combined_result = []

#     for result in results:
#         combined_result.extend(result)

#     return combined_result
