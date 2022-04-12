from django.db import models
from django.urls import reverse
import random


class Contract(models.Model):
    slug = models.SlugField(max_length=512, blank=True, null=True, )
    person_pinfl = models.CharField(max_length=512, blank=True, null=True)
    person_passportSeries = models.CharField(max_length=512, blank=True, null=True)
    person_passportNumber = models.CharField(max_length=512, blank=True, null=True)

    person_firstname = models.CharField(max_length=512, blank=True, null=True)
    person_lastname = models.CharField(max_length=512, blank=True, null=True)
    person_middlename = models.CharField(max_length=512, blank=True, null=True)
    person_phoneNumber = models.CharField(max_length=512, blank=True, null=True)
    person_gender = models.CharField(max_length=512, blank=True, null=True)
    person_birthDate = models.CharField(max_length=512, blank=True, null=True)

    address = models.CharField(max_length=512, blank=True, null=True)
    email = models.CharField(max_length=512, blank=True, null=True, default="default@agros.uz")
    payment_type = models.CharField(max_length=512, blank=True, null=True)
    person_data = models.JSONField(blank=True, null=True)

    policy_title = models.CharField(max_length=1024, null=True, blank=True, default="Baxtsiz hodisa")
    policy_start_date = models.DateField(blank=True, null=True)
    policy_end_date = models.DateField(blank=True, null=True)
    policy_seria = models.CharField(max_length=100, null=True, blank=True, default="UZIN-BH")
    policy_number = models.IntegerField(null=True, blank=True)
    policy_insurancePremium = models.IntegerField(blank=True, null=True, default=10000)
    policy_insurancePremium_word = models.CharField(verbose_name="Страховая премия с прописью", max_length=512,
                                                    blank=True,
                                                    null=True)
    policy_sumInsured = models.IntegerField(blank=True, null=True, default=10000000)
    policy_sumInsured_word = models.CharField(verbose_name="Страховая ответственность с прописью", max_length=512,
                                              blank=True, null=True)
    qr_code = models.URLField(verbose_name="QRCODE url", blank=True, null=True)
    policy_pdf = models.URLField(null=True, blank=True)

    created_at = models.DateTimeField(auto_now_add=True, blank=True, null=True)
    updated_at = models.DateTimeField(auto_now=True, blank=True, null=True)

    def __str__(self):
        return f"{self.person_passportSeries} {self.person_passportNumber}"

    def get_absolute_url(self):
        return reverse('contract_detail', kwargs={'slug': self.slug})

    def save(self, *args, **kwargs):  # new
        if not self.slug:
            self.slug = self.person_lastname.lower() + "_" + self.person_firstname.lower() + str(random.randint(1, 1000))

        if not self.policy_number:
            last_id = Contract.objects.values('id').last()
            if last_id is None:
                last_id = 1
                self.policy_number = last_id
            else:
                self.policy_number = last_id['id'] + 1
        return super().save(*args, **kwargs)
