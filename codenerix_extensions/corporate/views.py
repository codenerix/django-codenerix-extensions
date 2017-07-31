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
import json

from django.utils.translation import ugettext as _
from codenerix.views import GenList, GenCreate, GenCreateModal, GenUpdate, GenUpdateModal, GenDelete

from codenerix_extensions.corporate.models import CorporateImage
from codenerix_extensions.corporate.forms import CorporateImageForm


# ###########################################
# Corporate Image
class CorporateImageList(GenList):
    model = CorporateImage
    default_ordering = ['-public', ]
    extra_context = {'menu': ['CDNX_CorporateImage', 'CDNX_CorporateImage'], 'bread': [_('CorporateImage'), _('CorporateImage')]}
    gentranslate = {
        'image_not_selected': _("Image not selected")
    }


class CorporateImageCreate(GenCreate):
    model = CorporateImage
    form_class = CorporateImageForm

    def form_valid(self, form):
        # Get body
        body = json.loads(self.request.body.decode('utf-8'))

        # Get digital_sign
        digital_sign = body.get('digital_sign', None)
        if isinstance(digital_sign, dict):
            name_file_sign = digital_sign.get('filename', None)
            if name_file_sign is not None:
                self.request.name_file_sign = name_file_sign
                form.instance.name_file_sign = name_file_sign

        # Get company seal
        company_seal = body.get('company_seal', None)
        if isinstance(company_seal, dict):
            name_file_seal = company_seal.get('filename', None)
            if name_file_seal is not None:
                self.request.name_file_seal = name_file_seal
                form.instance.name_file_seal = name_file_seal

        # Get company logo
        company_logo = body.get('company_logo', None)
        if isinstance(company_logo, dict):
            name_file_logo = company_logo.get('filename', None)
            if name_file_logo is not None:
                self.request.name_file_logo = name_file_logo
                form.instance.name_file_logo = name_file_logo

        # Return result
        return super(CorporateImageCreate, self).form_valid(form)


class CorporateImageCreateModal(GenCreateModal, CorporateImageCreate):
    pass


class CorporateImageUpdate(GenUpdate):
    model = CorporateImage
    form_class = CorporateImageForm

    def form_valid(self, form):
        # Get body
        body = json.loads(self.request.body.decode('utf-8'))

        # Get digital_sign
        digital_sign = body.get('digital_sign', None)
        if isinstance(digital_sign, dict):
            name_file_sign = digital_sign.get('filename', None)
            if name_file_sign is not None:
                self.request.name_file_sign = name_file_sign
                form.instance.name_file_sign = name_file_sign

        # Get company seal
        company_seal = body.get('company_seal', None)
        if isinstance(company_seal, dict):
            name_file_seal = company_seal.get('filename', None)
            if name_file_seal is not None:
                self.request.name_file_seal = name_file_seal
                form.instance.name_file_seal = name_file_seal

        # Get company logo
        company_logo = body.get('company_logo', None)
        if isinstance(company_logo, dict):
            name_file_logo = company_logo.get('filename', None)
            if name_file_logo is not None:
                self.request.name_file_logo = name_file_logo
                form.instance.name_file_logo = name_file_logo

        # Return result
        return super(CorporateImageUpdate, self).form_valid(form)


class CorporateImageUpdateModal(GenUpdateModal):
    pass


class CorporateImageDelete(GenDelete):
    model = CorporateImage
