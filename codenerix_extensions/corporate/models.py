# -*- coding: utf-8 -*-
#
# django-codenerix-extensions
#
# Copyright 2017 Centrologic Computational Logistic Center S.L.
#
# Project URL : http://www.codenerix.com
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
# http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

from django.db import models, transaction
from django.utils.translation import ugettext_lazy as _

from codenerix.models import CodenerixModel
from codenerix.exceptions import CodenerixException
from codenerix.lib.helpers import upload_path
from codenerix.fields import ImageAngularField


class CorporateImage(CodenerixModel):

    nid = models.CharField(_("NID"), max_length=20, blank=True)
    business_name = models.CharField(_("Business name"), max_length=254, blank=True, null=True)
    digital_sign = ImageAngularField(_("Digital sign"), upload_to=upload_path, max_length=200, blank=True, null=True)
    name_file_sign = models.CharField(_("Name file digital sign"), max_length=254, blank=True, null=True)
    company_seal = ImageAngularField(_("Company seal"), upload_to=upload_path, max_length=200, blank=True, null=True)
    name_file_seal = models.CharField(_("Name file company seal"), max_length=254, blank=True, null=True)
    company_logo = ImageAngularField(_("Company logo"), upload_to=upload_path, max_length=200, blank=True, null=True)
    name_file_logo = models.CharField(_("Name file company logo"), max_length=254, blank=True, null=True)
    public = models.BooleanField(_("Public"), default=False)

    def __unicode__(self):
        return u"{}".format(self.digital_sign)

    def __str__(self):
        return self.__unicode__

    def __fields__(self, info):
        fields = []
        fields.append(('nid', _('NID'), 100))
        fields.append(('business_name', _('Business name'), 100))
        fields.append(('digital_sign', _('Digital sign'), 15))
        fields.append(('name_file_sign', _('Name file digital sign'), 15))
        fields.append(('company_seal', _('Company seal'), 15))
        fields.append(('name_file_seal', _('Name file company seal'), 15))
        fields.append(('company_logo', _('Company logo'), 15))
        fields.append(('name_file_logo', _('Name file company logo'), 15))
        fields.append(('public', _('Public'), 100))
        fields.append(('updated', _('Last Update'), 100))
        return fields

    def save(self, *args, **kwards):
        """
        Siempre debe haber un registro marcado como público
        There should always be a record marked as public
        """
        try:
            with transaction.atomic():
                if self.public:
                    CorporateImage.objects.exclude(pk=self.pk).update(public=False)
                elif not CorporateImage.objects.exclude(pk=self.pk).filter(public=True).exists():
                    self.public = True

                return super(CorporateImage, self).save(*args, **kwards)
        except CodenerixException:
            return super(CorporateImage, self).save(*args, **kwards)
