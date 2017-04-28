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

from django.utils.translation import ugettext_lazy as _
from codenerix.forms import GenModelForm
from codenerix_extensions.corporate.models import CorporateImage


class CorporateImageForm(GenModelForm):
    class Meta:
        model = CorporateImage
        exclude = ['name_file_sign', 'name_file_seal', 'name_file_logo', ]

    def __groups__(self):
        g = [
            (
                _('Details'), 12,
                ['business_name', 6],
                ['nid', 4],
                ['public', 2],
                ['digital_sign', 4],
                ['company_seal', 4],
                ['company_logo', 4],
            )
        ]
        return g

    @staticmethod
    def __groups_details__():
        g = [
            (_('Details'), 12,
                ['business_name', 6],
                ['nid', 4],
                ['digital_sign', 6],
                ['name_file_sign', 6],
                ['company_seal', 6],
                ['name_file_seal', 6],
                ['company_logo', 6],
                ['name_file_logo', 6],
                ['public', 6],)
        ]
        return g
