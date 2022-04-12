import json

from num2words import num2words
from .models import Contract


def form_save(form):
    gender = ""
    if not form['personData'] == "":
        personData = json.loads(form['personData'])
        if str(personData['gender']) == '1':
            gender = 'm'
        elif str(personData['gender']) == '0':
            gender = 'f'
    else:
        gender = "No data"
        personData = "No PersonData"
        print('PUSTOY')

    form_phone = form['phone']
    person_phoneNumber = "".join(c for c in form_phone if c.isdecimal())
    policy_sumInsured=10000000


    contract = Contract(
        person_pinfl=form['pinfl'],
        person_passportSeries=form['passportSeries'].upper(),
        person_passportNumber=form['passportNumber'],

        person_firstname=form['firstNameLatin'],
        person_lastname=form['lastNameLatin'],
        person_middlename=form['middleNameLatin'],
        person_phoneNumber=person_phoneNumber,
        person_gender=gender,
        person_birthDate=form['birthDate'],

        address=form['address'],
        email=form['email'],
        payment_type=form['payment_type'],
        policy_insurancePremium=form['policy_insurancePremium'],
        policy_insurancePremium_word=num2words(int(form['policy_insurancePremium']), lang='ru'),
        policy_sumInsured=policy_sumInsured,
        policy_sumInsured_word=num2words(policy_sumInsured, lang='ru'),
        policy_start_date=form['policy_start_date'],
        policy_end_date=form['policy_end_date'],

        person_data=personData

    )
    contract.save()
    return contract




'''CODE'''

