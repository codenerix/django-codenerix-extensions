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
from django.db import models

from codenerix.lib.helpers import upload_path
from codenerix.fields import FileAngularField, ImageAngularField


# ##################################
# #### Documentos e imagenes #######
# ##################################
class GenDocumentFile(models.Model):  # META: Abstract class
    doc_path = FileAngularField(_("Doc Path"), upload_to=upload_path, max_length=200, blank=False, null=False)
    name_file = models.CharField(_("Name"), max_length=254, blank=False, null=False)

    class Meta:
        abstract = True


class GenDocumentFileNull(models.Model):  # META: Abstract class
    doc_path = FileAngularField(_("Doc Path"), upload_to=upload_path, max_length=200, blank=True, null=True)
    name_file = models.CharField(_("Name"), max_length=254, blank=True, null=True)

    class Meta:
        abstract = True


class GenImageFile(models.Model):  # META: Abstract class
    image = ImageAngularField(_("Image"), upload_to=upload_path, max_length=200, blank=False, null=False)
    name_file = models.CharField(_("Name"), max_length=254, blank=True, null=True)

    class Meta:
        abstract = True


class GenImageFileNull(models.Model):  # META: Abstract class
    image = ImageAngularField(_("Image"), upload_to=upload_path, max_length=200, blank=True, null=True)
    name_file = models.CharField(_("Name"), max_length=254, blank=True, null=True)

    class Meta:
        abstract = True
