from celery import shared_task
from pyboleto.bank.bradesco import BoletoBradesco
from pyboleto.pdf import BoletoPDF
from datetime import date
from django.conf import settings
from django.core.mail import EmailMultiAlternatives
from celery.utils.log import get_task_logger

logger = get_task_logger(__name__)


@shared_task
def process_csv_lote(lote):
    customers = []
    for line in lote:
        data = line.decode("utf-8").strip().split(",")
        name = data[0]
        government_id = data[1]
        email = data[2]
        debt_amount = float(data[3])
        debt_due_date = data[4]
        debt_id = data[5]

        boleto_data = {
            "name": name,
            "government_id": government_id,
            "email": email,
            "debt_amount": debt_amount,
            "debt_due_date": debt_due_date,
            "debt_id": debt_id,
        }
        customers.append(email)
        boleto = generate_boleto(boleto_data)
        send_mail(boleto, boleto_data)

    return customers


def generate_boleto(data):

    government_id = (data["government_id"],)
    debt_amount = (data["debt_amount"],)
    debt_due_date = (data["debt_due_date"],)
    debt_id = (data["debt_id"],)
    name = data["name"]

    tup = debt_due_date
    str = ""
    for element in tup:
        str += element

    data_str = str.split("-")
    date_formated = [int(num) for num in data_str]
    year = date_formated[0]
    month = date_formated[1]
    day = date_formated[2]

    listaDadosBradesco = []

    for i in range(2):

        new_boleto = BoletoBradesco()
        new_boleto.carteira = "06"  # Contrato firmado com o Banco Bradesco
        new_boleto.cedente = "Empresa ACME LTDA"
        new_boleto.cedente_documento = "102.323.777-01"
        new_boleto.cedente_endereco = (
            "Rua Acme, 123 - Centro - Sao Paulo/SP - " + "CEP: 12345-678"
        )
        new_boleto.agencia_cedente = "0278-0"
        new_boleto.conta_cedente = "43905-3"

        new_boleto.data_vencimento = date(year, month, day)
        new_boleto.data_documento = date(2024, 2, 12)
        new_boleto.data_processamento = date(2014, 2, 12)

        new_boleto.instrucoes = [
            "- Linha 1",
            "- Sr Caixa, cobrar multa de 2% após o vencimento",
            "- Receber até 10 dias após o vencimento",
        ]
        new_boleto.demonstrativo = [
            f"- Debito {debt_id} valor R$ {debt_amount}",
            f"- Total R$ {debt_amount}",
        ]
        new_boleto.valor_documento = 2158.41

        new_boleto.nosso_numero = "1112011668"
        new_boleto.numero_documento = "1112011668"
        new_boleto.sacado = [
            f"Cliente {government_id} %d" % (i + 1),
            "Rua Desconhecida, 00/0000 - Não Sei - Cidade - Cep. 00000-000",
            "",
        ]
        listaDadosBradesco.append(new_boleto)

    boleto = BoletoPDF(f"boleto-bradesco-{name}.pdf")
    for i in range(len(listaDadosBradesco)):
        boleto.drawBoleto(listaDadosBradesco[i])
        boleto.nextPage()
    boleto.save()
    return boleto


def send_mail(boleto, data):

    email = data["email"]
    name = data["name"]

    subject = f"Email de cobrança para {name}"
    body = "Pague seu boleto e evite cobranças"
    sendmail = EmailMultiAlternatives(
        subject, body, settings.DEFAULT_FROM_EMAIL, to=[email]
    )
    sendmail.attach("emailpdf_{}".format(name) + ".pdf", boleto, "application/pdf")
    sendmail.content_subtype = "pdf"
    sendmail.decode = "utf-8"
    return sendmail.send()
