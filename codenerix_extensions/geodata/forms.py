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

from django.conf import settings
from django.utils.translation import ugettext_lazy as _

from codenerix.forms import GenModelForm

from .models import Continent, Country, Region, Province, TimeZone, City, MODELS


class ContinentForm(GenModelForm):
    class Meta:
        model = Continent
        exclude = []

    def __groups__(self):
        g = [
            (
                _('Details'), 12,
                ['code', 6],
            )
        ]
        return g


class CountryForm(GenModelForm):
    class Meta:
        model = Country
        exclude = []

    def __groups__(self):
        return [
            (
                _('Details'), 12,
                ['continent', 6],
                ['code', 6],
            )
        ]


class RegionForm(GenModelForm):
    class Meta:
        model = Region
        exclude = []

    def __groups__(self):
        return [
            (
                _('Details'), 12,
                ['country', 6],
                ['code', 6],
            )
        ]


class ProvinceForm(GenModelForm):
    class Meta:
        model = Province
        exclude = []

    def __groups__(self):
        return [
            (
                _('Details'), 12,
                ['region', 6],
                ['code', 6],
            )
        ]


class TimeZoneForm(GenModelForm):
    class Meta:
        model = TimeZone
        exclude = []

    def __groups__(self):
        return [
            (
                _('Details'), 12,
                ['name', 6],
            )
        ]


class CityForm(GenModelForm):
    class Meta:
        model = City
        exclude = []

    def __groups__(self):
        return [
            (
                _('Details'), 12,
                ['country', 6],
                ['region', 6],
                ['province', 6],
                ['time_zone', 6],
            )
        ]


# MODELS
query = ""
forms_dyn = []
for info in MODELS:
    field = info[0]
    model = info[1]
    for lang_code in settings.LANGUAGES_DATABASES:
        query = "from .models import {}GeoName{}\n".format(model, lang_code)
        exec(query)
        query = """
class {model}TextForm{lang}(GenModelForm):\n
    class Meta:\n
        model={model}GeoName{lang}\n
        exclude = []\n
    def __groups__(self):\n
        return [(_('Details'),12,"""
        if lang_code == settings.LANGUAGES_DATABASES[0]:
            query += """
                ['name', 12, None, None, None, None, None, ["ng-blur=refresh_lang_field('name', '{model}TextForm', [{languages}])"]],
            )]\n"""
        else:
            query += """
                ['name', 12],
            )]\n"""

        exec(query.format(model=model, lang=lang_code, languages="'{}'".format("','".join(settings.LANGUAGES_DATABASES))))
