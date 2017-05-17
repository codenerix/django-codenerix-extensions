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
from django.db import models
from django.db.models import Q
from django.utils.encoding import smart_text
from django.utils.translation import ugettext_lazy as _

from codenerix.models import CodenerixModel


class GenGeoName(CodenerixModel):  # META: Abstract class

    class Meta:
        abstract = True

    name = models.CharField(_('Name'), max_length=100, blank=False)

    def __unicode__(self):
        return u'{}'.format(smart_text(self.name))

    def __str__(self):
        return self.__unicode__()

    def __fields__(self, info):
        return [
            ('name', _('Name'), 100),
        ]


class Continent(CodenerixModel):
    code = models.CharField(_('Code'), max_length=2, unique=True, blank=False)

    def __unicode__(self):
        return u"{}".format(smart_text(self.code))

    def __str__(self):
        return self.__unicode__()

    def __fields__(self, info):
        return [
            ('code', _('Code'), 100),
        ]

    def __searchQ__(self, info, text):
        return {
            'code': models.Q(code__icontains=text),
        }

    def __searchF__(self, info):
        filters = {}
        filters['code'] = (_('Code'), lambda x: Q(code__icontains=x), 'input')
        return filters


class Country(CodenerixModel):
    code = models.CharField(_('Code'), max_length=2, unique=True, blank=False)
    continent = models.ForeignKey(Continent, verbose_name=_('Continent'), related_name='countries', null=False)

    def __unicode__(self):
        return u"{}".format(smart_text(self.code))

    def __str__(self):
        return self.__unicode__()

    def __fields__(self, info):
        return [
            ('code', _('Code'), 100),
            ('continent', _('Continent'), 100),
        ]

    def __searchQ__(self, info, text):
        return {
            'code': models.Q(code__icontains=text),
        }

    def __searchF__(self, info):
        filters = {}
        filters['code'] = (_('Code'), lambda x: Q(code__icontains=x), 'input')
        return filters


class TimeZone(CodenerixModel):
    name = models.CharField(_('Name'), max_length=50, unique=True, blank=False)

    def __unicode__(self):
        return u"{}".format(smart_text(self.name))

    def __str__(self):
        return self.__unicode__()

    def __fields__(self, info):
        return [
            ('name', _('Name'), 100),
        ]

    def __searchQ__(self, info, text):
        return {
            'name': models.Q(name__icontains=text),
        }

    def __searchF__(self, info):
        filters = {}
        filters['name'] = (_('Name'), lambda x: Q(name__icontains=x), 'input')
        return filters


class Region(CodenerixModel):
    country = models.ForeignKey(Country, verbose_name=_('Country'), null=False, related_name='regions')
    code = models.CharField(_('Code'), max_length=3, blank=False)

    def __unicode__(self):
        return u"{} - {}".format(smart_text(self.country), self.code)

    def __str__(self):
        return self.__unicode__()

    def __fields__(self, info):
        return [
            ('country', _('Country'), 100),
            ('code', _('Code'), 100),
        ]

    def __searchQ__(self, info, text):
        return {
            'code': models.Q(code__icontains=text),
        }

    def __searchF__(self, info):
        filters = {}
        filters['code'] = (_('Code'), lambda x: Q(code__icontains=x), 'input')
        return filters


class Province(CodenerixModel):
    region = models.ForeignKey(Region, verbose_name=_('Region'), null=False, related_name='provinces')
    code = models.CharField(_('Code'), max_length=3, blank=False)

    def __unicode__(self):
        return u"{} - {}".format(smart_text(self.region), self.code)

    def __str__(self):
        return self.__unicode__()

    def __fields__(self, info):
        return [
            ('region', _('Region'), 100),
            ('code', _('Code'), 100),
        ]

    def __searchQ__(self, info, text):
        return {
            'code': models.Q(code__icontains=text),
        }

    def __searchF__(self, info):
        filters = {}
        filters['code'] = (_('Code'), lambda x: Q(code__icontains=x), 'input')
        return filters


class City(CodenerixModel):
    country = models.ForeignKey(Country, verbose_name=_('Country'), null=False, related_name='cities')
    region = models.ForeignKey(Region, verbose_name=_('Region'), null=True, related_name='cities')
    province = models.ForeignKey(Province, verbose_name=_('Province'), null=True, related_name='cities')
    time_zone = models.ForeignKey(TimeZone, verbose_name=_('City'), null=False, related_name='cities')

    def __unicode__(self):
        return u"{} - {}".format(smart_text(self.country), smart_text(self.time_zone))

    def __str__(self):
        return self.__unicode__()

    def __fields__(self, info):
        return [
            ('country', _('Country'), 100),
            ('time_zone', _('Time zone'), 100),
        ]


MODELS = (
    ('continent', 'Continent'),
    ('country', 'Country'),
    ('region', 'Region'),
    ('province', 'Province'),
    ('city', 'City'),
)

for field, model in MODELS:
    for lang_code in settings.LANGUAGES_DATABASES:
        query = "class {}GeoName{}(GenGeoName):\n".format(model, lang_code)
        query += "    {} = models.OneToOneField({}, blank=False, null=False, related_name='{}')\n".format(field, model, lang_code.lower())
        exec(query)
