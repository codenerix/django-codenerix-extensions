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

""" Populate geographic data using the free database provided by MaxMind.

Two different databases were used:
    - GeoLite2 City: http://geolite.maxmind.com/download/geoip/database/GeoLite2-City-CSV.zip
    - GeoLite2 Country: http://geolite.maxmind.com/download/geoip/database/GeoLite2-Country-CSV.zip
"""

from os.path import dirname, join
from bz2 import BZ2File
from csv import reader

from django.conf import settings
from django.core.management.base import BaseCommand
from django.utils.translation import ugettext as _
from django.core.exceptions import ObjectDoesNotExist

from codenerix_extensions.geodata.models import Continent, Country, Region, Province, City, TimeZone


BASE_LANGUAGE = 'EN'

COUNTRY_DATA_FILES = {
    'ES': 'GeoLite2-Country-Locations-es.csv.bz2',
    'EN': 'GeoLite2-Country-Locations-en.csv.bz2',
}

CITY_DATA_FILES = {
    'ES': 'GeoLite2-City-Locations-es.csv.bz2',
    'EN': 'GeoLite2-City-Locations-en.csv.bz2',
}

LANGUAGES = set([code for code in settings.LANGUAGES_DATABASES if code in COUNTRY_DATA_FILES])


def clean(name):
    if name:
        name = name.decode('utf-8')
        if name[0] == '"' and name[-1] == '"':
            return name[1:-1]
    return name


def populate_missing_names(data):
    for lang in LANGUAGES:
        for d in data.values():
            if lang not in d or d[lang] == '':
                for other_lang in LANGUAGES - {lang}:
                    if d[other_lang] != '':
                        d[lang] = d[other_lang]
                        break


def continents_lines(filename):
    with BZ2File(filename, 'rU') as data_file:
        csv_file = reader(data_file, delimiter=',', quotechar='"')

        first = True
        for line in csv_file:
            if first:
                first = False
                continue

            _, _, continent_code, continent_name, _, _ = line
            if continent_code.strip() != '' and continent_name.strip() != '':
                yield continent_code, clean(continent_name)


def country_lines(filename):
    with BZ2File(filename, 'rU') as data_file:
        csv_file = reader(data_file, delimiter=',', quotechar='"')

        first = True
        for line in csv_file:
            if first:
                first = False
                continue

            geoid, _, continent_code, _, country_code, country_name = line
            if continent_code.strip() != '' and country_code.strip() != '' and country_name.strip() != '':
                yield int(geoid), continent_code, country_code, clean(country_name)


def region_lines(filename):
    with BZ2File(filename, 'rU') as data_file:
        csv_file = reader(data_file, delimiter=',', quotechar='"')

        first = True
        for line in csv_file:
            if first:
                first = False
                continue

            geoid, _, _, _, country_code, _, region_code, region_name, province_code, province_name, city_name, _, _ = line
            if country_code != '' and region_code != '' and region_name.strip() != '':
                yield int(geoid), country_code, region_code, clean(region_name)


def province_lines(filename):
    with BZ2File(filename, 'rU') as data_file:
        csv_file = reader(data_file, delimiter=',', quotechar='"')

        first = True
        for line in csv_file:
            if first:
                first = False
                continue

            geoid, _, _, _, country_code, _, region_code, _, province_code, province_name, _, _, _ = line
            if country_code != '' and region_code != '' and province_code != '' and province_name != '':
                yield int(geoid), country_code, region_code, province_code, clean(province_name)


def city_lines(filename):
    with BZ2File(filename, 'rU') as data_file:
        csv_file = reader(data_file, delimiter=',', quotechar='"')

        first = True
        for line in csv_file:
            if first:
                first = False
                continue

            geoid, _, _, _, country_code, _, region_code, _, province_code, _, city_name, _, time_zone = line
            if geoid != '' and city_name.strip() != '' and time_zone != '':
                yield int(geoid), country_code, region_code, province_code, clean(city_name), clean(time_zone)


class Command(BaseCommand):
    help = _('Populates Continent, Country and City models')

    def handle(self, *args, **options):
        # print('Erasing existing data ...')
        # City.objects.all().delete()
        # TimeZone.objects.all().delete()
        # Province.objects.all().delete()
        # Region.objects.all().delete()
        # Country.objects.all().delete()
        # Continent.objects.all().delete()

        print('Importing new data ... This action may take some minutes.')
        print('')
        data_path = join(dirname(dirname(dirname(__file__))), 'geodata/data')

        # Importing language generated models
        for lang in LANGUAGES:
            exec('from codenerix_extensions.geodata.models import ContinentGeoName{}'.format(lang))
            exec('from codenerix_extensions.geodata.models import CountryGeoName{}'.format(lang))
            exec('from codenerix_extensions.geodata.models import RegionGeoName{}'.format(lang))
            exec('from codenerix_extensions.geodata.models import ProvinceGeoName{}'.format(lang))
            exec('from codenerix_extensions.geodata.models import CityGeoName{}'.format(lang))

        print('Importing continents ... ',)
        continents = {}
        for lang in LANGUAGES:
            filename = join(data_path, COUNTRY_DATA_FILES[lang])
            for code, name in continents_lines(filename):
                if code not in continents:
                    continents[code] = {
                        'model': Continent(code=code)
                    }
                continents[code][lang] = name

        for code, continent in continents.items():
            try:
                model = Continent.objects.get(code=code)
                continent['model'] = model
            except ObjectDoesNotExist:
                continent['model'].save()

        for lang in LANGUAGES:
            model_type = eval('ContinentGeoName{}'.format(lang))
            for continent in continents.values():
                try:
                    model = model_type.objects.get(continent=continent['model'])
                except ObjectDoesNotExist:
                    model = model_type()
                    model.continent = continent['model']
                model.name = continent[lang]
                model.save()
        print('Ok')

        print('Importing countries ... ',)
        countries = {}
        for lang in LANGUAGES:
            filename = join(data_path, COUNTRY_DATA_FILES[lang])
            for geoid, continent, code, name in country_lines(filename):
                if code not in countries:
                    countries[code] = {
                        'model': Country(
                            pk=geoid,
                            code=code,
                            continent=continents[continent]['model']
                        )
                    }
                countries[code][lang] = name

        for country in countries.values():
            try:
                model = Country.objects.get(code=country['model'].code)
                country['model'] = model
            except ObjectDoesNotExist:
                country['model'].save()

        for lang in LANGUAGES:
            model_type = eval('CountryGeoName{}'.format(lang))
            for country in countries.values():
                try:
                    model = model_type.objects.get(country=country['model'])
                except ObjectDoesNotExist:
                    model = model_type()
                    model.country = country['model']
                model.name = country[lang]
                model.save()
        print('Ok')

        print('Importing regions ... ',)
        regions = {}
        for lang in LANGUAGES:
            filename = join(data_path, CITY_DATA_FILES[lang])
            for geoid, country_code, region_code, region_name in region_lines(filename):
                region_key = '{}_{}'.format(country_code, region_code)
                if region_key not in regions:
                    regions[region_key] = {
                        'model': Region(
                            pk=geoid,
                            code=region_code,
                            country=countries[country_code]['model']
                        )
                    }
                regions[region_key][lang] = region_name

        for region in regions.values():
            try:
                model = Region.objects.get(pk=region['model'].pk)
                region['model'] = model
            except ObjectDoesNotExist:
                region['model'].save()

        populate_missing_names(regions)

        for lang in LANGUAGES:
            model_type = eval('RegionGeoName{}'.format(lang))
            for region in regions.values():
                try:
                    model = model_type.objects.get(region=region['model'])
                except ObjectDoesNotExist:
                    model = model_type()
                    model.region = region['model']
                model.name = region[lang]
                model.save()
        print('Ok')

        print('Importing provinces ... ',)
        provinces = {}
        for lang in LANGUAGES:
            filename = join(data_path, CITY_DATA_FILES[lang])
            for geoid, country_code, region_code, province_code, province_name in province_lines(filename):
                region_key = '{}_{}'.format(country_code, region_code)
                province_key = '{}_{}_{}'.format(country_code, region_code, province_code)
                if province_key not in provinces:
                    provinces[province_key] = {
                        'model': Province(
                            pk=geoid,
                            code=province_code,
                            region=regions[region_key]['model']
                        )
                    }
                provinces[province_key][lang] = province_name

        for province in provinces.values():
            try:
                model = Province.objects.get(pk=province['model'].pk)
                province['model'] = model
            except ObjectDoesNotExist:
                province['model'].save()

        populate_missing_names(provinces)

        for lang in LANGUAGES:
            model_type = eval('ProvinceGeoName{}'.format(lang))
            for province in provinces.values():
                try:
                    model = model_type.objects.get(province=province['model'])
                except ObjectDoesNotExist:
                    model = model_type()
                    model.province = province['model']
                model.name = province[lang]
                model.save()
        print('Ok')

        print('Importing cities ... ',)
        cities = {}
        timezones = {}
        for lang in LANGUAGES:
            filename = join(data_path, CITY_DATA_FILES[lang])
            for city_id, country_code, region_code, province_code, city_name, time_zone in city_lines(filename):
                if time_zone not in timezones:
                    try:
                        model = TimeZone.objects.get(name=time_zone)
                        timezones[time_zone] = model
                    except ObjectDoesNotExist:
                        timezones[time_zone] = TimeZone(name=time_zone)
                        timezones[time_zone].save()

                if city_id not in cities:
                    city = City(
                        pk=city_id,
                        country=countries[country_code]['model'],
                        time_zone=timezones[time_zone]
                    )
                    if region_code != '':
                        region_key = '{}_{}'.format(country_code, region_code)
                        city.region = regions[region_key]['model']

                    if province_code != '':
                        province_key = '{}_{}_{}'.format(country_code, region_code, province_code)
                        city.province = provinces[province_key]['model']

                    cities[city_id] = {
                        'model': city
                    }

                cities[city_id][lang] = city_name

        for city in cities.values():
            try:
                model = City.objects.get(pk=city['model'].pk)
                city['model'] = model
            except ObjectDoesNotExist:
                city['model'].save()

        populate_missing_names(cities)

        for lang in LANGUAGES:
            model_type = eval('CityGeoName{}'.format(lang))
            for city in cities.values():
                try:
                    model = model_type.objects.get(city=city['model'])
                except ObjectDoesNotExist:
                    model = model_type()
                    model.city = city['model']
                model.name = city[lang]
                model.save()
        print('Ok')

        print('Removing regions without cities ...',)
        for region in Region.objects.all():
            if region.cities.count() == 0:
                region.delete()
        print('Ok')

        print('Removing provinces without cities ...',)
        for province in Province.objects.all():
            if province.cities.count() == 0:
                province.delete()
        print('Ok')

        print('All done!!!')
