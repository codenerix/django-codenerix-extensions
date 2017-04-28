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
from codenerix_extensions.corporate.views import CorporateImageList, CorporateImageCreate, CorporateImageCreateModal, CorporateImageUpdate, CorporateImageUpdateModal, CorporateImageDelete


urlpatterns = [
    url(r'^corporateimages$', CorporateImageList.as_view(), name='CDNX_EXT_corporateimages_list'),
    url(r'^corporateimages/add$', CorporateImageCreate.as_view(), name='CDNX_EXT_corporateimages_add'),
    url(r'^corporateimages/addmodal$', CorporateImageCreateModal.as_view(), name='CDNX_EXT_corporateimages_addmodal'),
    url(r'^corporateimages/(?P<pk>\w+)/edit$', CorporateImageUpdate.as_view(), name='CDNX_EXT_corporateimages_edit'),
    url(r'^corporateimages/(?P<pk>\w+)/editmodal$', CorporateImageUpdateModal.as_view(), name='CDNX_EXT_corporateimages_editmodal'),
    url(r'^corporateimages/(?P<pk>\w+)/delete$', CorporateImageDelete.as_view(), name='CDNX_EXT_corporateimages_delete'),
]
