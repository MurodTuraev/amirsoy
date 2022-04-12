import os
import shutil
import subprocess

import qrcode as qrcode
from docx.shared import Mm
from docxtpl import DocxTemplate, InlineImage

from .models import Contract
from amirsoy.settings import BASE_DIR, MEDIA_URL
from num2words import num2words


def generate_doc(filename, policy_number):
    doc = DocxTemplate(BASE_DIR / "templates/word/policy.docx")
    filename = filename
    contract = Contract.objects.get(policy_number=policy_number)
    qrcode_file = str(BASE_DIR) + "/media/qrcode/" + filename + ".png"
    qrcode_img = InlineImage(doc, image_descriptor=qrcode_file, width=Mm(25))
    # print(str(BASE_DIR)+f"/media/qrcode/{filename}.png")

    policy_start_date = contract.policy_start_date.strftime("%d.%m.%Y"),
    policy_end_date = contract.policy_end_date.strftime("%d.%m.%Y"),
    created_at = contract.created_at.strftime("%d.%m.%Y"),

    print(type(policy_start_date))
    print(policy_end_date)
    print(created_at)


    context = {
        'policy_title': contract.policy_title,
        'policy_start_date': policy_start_date[0],
        'policy_end_date': policy_end_date[0],
        'policy_seria': contract.policy_seria,
        'policy_number': contract.policy_number,
        'policy_insurancePremium': contract.policy_insurancePremium,
        'policy_insurancePremium_word': contract.policy_insurancePremium_word,
        'policy_sumInsured': contract.policy_sumInsured,
        'created_at': created_at[0],
        'policy_sumInsured_word': contract.policy_sumInsured_word,
        'person_passportSeries': contract.person_passportSeries,
        'person_passportNumber': contract.person_passportNumber,
        'person_firstname': contract.person_firstname,
        'person_lastname': contract.person_lastname,
        'person_middlename': contract.person_middlename,
        'person_phoneNumber': contract.person_phoneNumber,
        'address': contract.address,
        'qrcode': qrcode_img
    }

    doc.render(context)

    doc.save(BASE_DIR / f"media/word/{filename}.docx")

    return filename


# Generate pdf
def generate_pdf(cur_polis):
    file_name = cur_polis
    docx = BASE_DIR / f"media/word/{file_name}.docx"
    pdf = BASE_DIR / f"media/pdf/{file_name}.pdf"
    pdf_root = BASE_DIR / f"{file_name}.pdf"
    doc2pdf_linux(docx)
    shutil.copyfile(pdf_root, pdf)
    os.remove(pdf_root)
    return 'OK'


try:
    from comtypes import client
except ImportError:
    client = None


def doc2pdf(doc):
    """
    convert a doc/docx document to pdf format
    :param doc: path to document
    """
    doc = os.path.abspath(doc)  # bugfix - searching files in windows/system32
    if client is None:
        return doc2pdf_linux(doc)
    name, ext = os.path.splitext(doc)
    try:
        word = client.CreateObject('Word.Application')
        worddoc = word.Documents.Open(doc)
        worddoc.SaveAs(name + '.pdf', FileFormat=17)
    except Exception:
        raise
    finally:
        worddoc.Close()
        word.Quit()


def doc2pdf_linux(doc):
    """
    convert a doc/docx document to pdf format (linux only, requires libreoffice)
    :param doc: path to document
    """
    cmd = 'libreoffice --convert-to pdf'.split() + [doc]
    p = subprocess.Popen(cmd, stderr=subprocess.PIPE, stdout=subprocess.PIPE)
    p.wait(timeout=10)
    stdout, stderr = p.communicate()
    if stderr:
        raise subprocess.SubprocessError(stderr)


# QR-CODE generation
def generate_qrcode(url):
    qr = qrcode.QRCode(
        version=1,
        error_correction=qrcode.constants.ERROR_CORRECT_L,
        box_size=10,
        border=4,
    )

    qr.add_data(url)
    qr.make(fit=True)
    qr_img = qr.make_image(fill_color="black", back_color="white")

    # img = qrcode.make(url)
    # type(img)  # qrcode.image.pil.PilImage

    return qr_img
