from django.shortcuts import render, redirect, get_object_or_404

from amirsoy.settings import HOST_URL
from contract.models import Contract
from contract.utils import form_save
from paycomuz import Paycom
from .functions import *


def contract_create(request):
    if request.method == 'POST':
        form = request.POST
        print(form)
        contract = form_save(form)
        slug = contract.slug
        return redirect('contract_payment', slug)
    else:
        return render(request, 'contract/contract_create.html')


def contract_payment(request, slug):
    contract = get_object_or_404(Contract, slug=slug)
    paycom = Paycom()
    amount = int(contract.policy_insurancePremium) * 100
    order_id = contract.id + 1000
    return_url = HOST_URL + "contract/contract_detail/" + str(contract.slug) + "/"
    # payme_url = paycom.create_initialization(amount=amount, order_id=order_id, return_url=return_url)
    payme_url = ""
    print(payme_url)
    context = {
        "payme_url": payme_url,
        "contract": contract
    }
    return render(request, 'contract/contract_payment.html', context)


def contract_list(request):
    contracts = Contract.objects.all()

    context = {
        "contracts": contracts
    }
    return render(request, 'contract/contract_list.html', context)


def contract_detail(request, slug):
    current_contract = get_object_or_404(Contract, slug=slug)

    if (current_contract.qr_code is None) and (current_contract.policy_pdf is None):
        filename = current_contract.policy_seria + str(current_contract.policy_number)
        print(filename)

        # QR-CODE generation
        # detail_url = "http://" + request.headers['Host'] + "/detail/" + current_contract.id + "/"  # local
        detail_url = HOST_URL + "contract/contract_detail/" + str(current_contract.slug) + "/"  # global
        qr_url = generate_qrcode(url=detail_url)
        qr_url.save('media/qrcode/' + filename + '.png', 'png')
        qrcode = os.path.relpath(filename + '.png')
        # contract.qr_code = "http://" + request.headers['Host'] + MEDIA_URL + "qrcode/" + filename + ".png" # local
        current_contract.qr_code = HOST_URL + "media/" + "qrcode/" + filename + ".png"  # global

        # DOC generation
        doc = generate_doc(filename=filename, policy_number=current_contract.policy_number)  # Generate doc

        # pdf_url = "http://" + request.headers['Host'] + MEDIA_URL + "pdf/" + cur_polis + ".pdf" # local
        pdf_url = HOST_URL + "media/" + "pdf/" + filename + ".pdf"  # global
        generate_pdf(filename)  # generate pdf
        current_contract.policy_pdf = pdf_url
        current_contract.save()
        # END GENERATE qrcode/word/pdf
        context = {
            "contract": current_contract
        }
        return render(request, 'contract/contract_detail.html', context)
    else:
        context = {
            "contract": current_contract
        }
        return render(request, 'contract/contract_detail.html', context)
