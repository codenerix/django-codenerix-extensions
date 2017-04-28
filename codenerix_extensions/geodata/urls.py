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

from django.conf.urls import url

from .views import ContinentList, ContinentCreate, ContinentCreateModal, ContinentUpdate, ContinentUpdateModal, ContinentDelete
from .views import CountryList, CountryCreate, CountryCreateModal, CountryUpdate, CountryUpdateModal, CountryDelete, CountryForeign
from .views import RegionList, RegionCreate, RegionCreateModal, RegionUpdate, RegionUpdateModal, RegionDelete, RegionForeign
from .views import ProvinceList, ProvinceCreate, ProvinceCreateModal, ProvinceUpdate, ProvinceUpdateModal, ProvinceDelete, ProvinceForeign
from .views import TimeZoneList, TimeZoneCreate, TimeZoneCreateModal, TimeZoneUpdate, TimeZoneUpdateModal, TimeZoneDelete
from .views import CityList, CityCreate, CityCreateModal, CityUpdate, CityUpdateModal, CityDelete, CityForeign


urlpatterns = [
    url(r'^continents$', ContinentList.as_view(), name='CDNX_geodata_continents_list'),
    url(r'^continents/add$', ContinentCreate.as_view(), name='CDNX_geodata_continents_add'),
    url(r'^continents/addmodal$', ContinentCreateModal.as_view(), name='CDNX_geodata_continents_addmodal'),
    url(r'^continents/(?P<pk>\w+)/edit$', ContinentUpdate.as_view(), name='CDNX_geodata_continents_edit'),
    url(r'^continents/(?P<pk>\w+)/editmodal$', ContinentUpdateModal.as_view(), name='CDNX_geodata_continents_editmodal'),
    url(r'^continents/(?P<pk>\w+)/delete$', ContinentDelete.as_view(), name='CDNX_geodata_continents_delete'),

    url(r'^countries$', CountryList.as_view(), name='CDNX_geodata_countries_list'),
    url(r'^countries/add$', CountryCreate.as_view(), name='CDNX_geodata_countries_add'),
    url(r'^countries/addmodal$', CountryCreateModal.as_view(), name='CDNX_geodata_countries_addmodal'),
    url(r'^countries/(?P<pk>\w+)/edit$', CountryUpdate.as_view(), name='CDNX_geodata_countries_edit'),
    url(r'^countries/(?P<pk>\w+)/editmodal$', CountryUpdateModal.as_view(), name='CDNX_geodata_countries_editmodal'),
    url(r'^countries/(?P<pk>\w+)/delete$', CountryDelete.as_view(), name='CDNX_geodata_countries_delete'),
    url(r'^countries/foreign/(?P<search>[\w\W]+|\*)$', CountryForeign.as_view(), name='CDNX_ext_location_country_foreign'),

    url(r'^regions$', RegionList.as_view(), name='CDNX_geodata_regions_list'),
    url(r'^regions/add$', RegionCreate.as_view(), name='CDNX_geodata_regions_add'),
    url(r'^regions/addmodal$', RegionCreateModal.as_view(), name='CDNX_geodata_regions_addmodal'),
    url(r'^regions/(?P<pk>\w+)/edit$', RegionUpdate.as_view(), name='CDNX_geodata_regions_edit'),
    url(r'^regions/(?P<pk>\w+)/editmodal$', RegionUpdateModal.as_view(), name='CDNX_geodata_regions_editmodal'),
    url(r'^regions/(?P<pk>\w+)/delete$', RegionDelete.as_view(), name='CDNX_geodata_regions_delete'),
    url(r'^regions/foreign/(?P<search>[\w\W]+|\*)$', RegionForeign.as_view(), name='CDNX_ext_location_regions_foreign'),

    url(r'^provinces$', ProvinceList.as_view(), name='CDNX_geodata_provinces_list'),
    url(r'^provinces/add$', ProvinceCreate.as_view(), name='CDNX_geodata_provinces_add'),
    url(r'^provinces/addmodal$', ProvinceCreateModal.as_view(), name='CDNX_geodata_provinces_addmodal'),
    url(r'^provinces/(?P<pk>\w+)/edit$', ProvinceUpdate.as_view(), name='CDNX_geodata_provinces_edit'),
    url(r'^provinces/(?P<pk>\w+)/editmodal$', ProvinceUpdateModal.as_view(), name='CDNX_geodata_provinces_editmodal'),
    url(r'^provinces/(?P<pk>\w+)/delete$', ProvinceDelete.as_view(), name='CDNX_geodata_provinces_delete'),
    url(r'^provinces/foreign/(?P<search>[\w\W]+|\*)$', ProvinceForeign.as_view(), name='CDNX_ext_location_provinces_foreign'),

    url(r'^timezones$', TimeZoneList.as_view(), name='CDNX_geodata_timezones_list'),
    url(r'^timezones/add$', TimeZoneCreate.as_view(), name='CDNX_geodata_timezones_add'),
    url(r'^timezones/addmodal$', TimeZoneCreateModal.as_view(), name='CDNX_geodata_timezones_addmodal'),
    url(r'^timezones/(?P<pk>\w+)/edit$', TimeZoneUpdate.as_view(), name='CDNX_geodata_timezones_edit'),
    url(r'^timezones/(?P<pk>\w+)/editmodal$', TimeZoneUpdateModal.as_view(), name='CDNX_geodata_timezones_editmodal'),
    url(r'^timezones/(?P<pk>\w+)/delete$', TimeZoneDelete.as_view(), name='CDNX_geodata_timezones_delete'),

    url(r'^cities$', CityList.as_view(), name='CDNX_geodata_cities_list'),
    url(r'^cities/add$', CityCreate.as_view(), name='CDNX_geodata_cities_add'),
    url(r'^cities/addmodal$', CityCreateModal.as_view(), name='CDNX_geodata_cities_addmodal'),
    url(r'^cities/(?P<pk>\w+)/edit$', CityUpdate.as_view(), name='CDNX_geodata_cities_edit'),
    url(r'^cities/(?P<pk>\w+)/editmodal$', CityUpdateModal.as_view(), name='CDNX_geodata_cities_editmodal'),
    url(r'^cities/(?P<pk>\w+)/delete$', CityDelete.as_view(), name='CDNX_geodata_cities_delete'),
    url(r'^cities/foreign/(?P<search>[\w\W]+|\*)$', CityForeign.as_view(), name='CDNX_ext_location_citys_foreign'),
]
