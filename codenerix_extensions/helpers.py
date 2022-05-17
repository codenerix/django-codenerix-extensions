# -*- coding: utf-8 -*-
#
# django-codenerix-extensions
#
# Codenerix GNU
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

import bz2
from bz2 import BZ2File
from decimal import Decimal, ROUND_HALF_UP

from django.utils.translation import get_language
from django.conf import settings


def get_external_model(class_object):
    """
    Given a class (class_object), it locates the related model (throught the codenerix abstract class)
    """
    class_abstract = class_object.CodenerixMeta.abstract
    if class_abstract is not None:
        for class_related in class_object._meta.related_objects:
            if issubclass(class_related.related_model, class_abstract):
                return class_related.related_model
    return None


def get_external_method(class_object, method_name, *args, **kwargs):
    """
    Given a class (class_object), a name for a method (method_name) and its arguments,
    it searchs for the method in the related model (throught the codenerix abstract class) and
    it executes that method or return None if no method is found.
    """
    related_model = get_external_model(class_object)
    if related_model is not None:
        f = getattr(related_model, method_name, None)
        if f:
            instance = related_model()
            return f(instance, *args, **kwargs)
        else:
            return None
    return None


def DynamicLanguageForm(modelName, modelConection, exclude=None, nameForm=None):
    listForm = []
    for lang in settings.LANGUAGES:
        lang_code = lang[0].upper()
        name = str(modelName) + "FormText" if nameForm is None else nameForm
        excludes = "["
        if exclude:
            for e in exclude:
                excludes += e + ", "
        excludes += "]"

        string = "class {}{}(GenModelForm):\n".format(name, lang_code)
        string += "  class Meta:\n"
        string += "    model={}{}\n".format(modelConection, lang_code)
        string += "    exclude = {}\n".format(excludes)
        listForm.append(string)

    return listForm


def get_language_database():
    '''
    Return the language to be used to search the database contents
    '''
    lang = None
    language = get_language()
    if language:
        for x in settings.LANGUAGES_DATABASES:
            if x.upper() == language.upper():
                lang = language
                break

    if lang is None:
        lang = settings.LANGUAGES_DATABASES[0]
    return lang.lower()


class FileBZ2(object):
    def __init__(self, filename, mode):
        self.file = None
        if 'r' in mode:
            self.mode = 'r'
        elif 'w' in mode:
            self.mode = 'w'
            raise Exception('This method is not developed')
        else:
            raise Exception('Mode must contain "r" for decompressing or "w" for compressing')
        
        self.binary = 'b' in mode
        self.filename = filename

    def __enter__(self):
        try:
            mode = self.mode
            if self.binary:
                mode += 't'
            self.file = bz2.open(self.filename, mode)
        except AttributeError:
            mode = self.mode
            if self.binary:
                mode += 'U'
            self.file = BZ2File(self.filename, mode)
        return self.file

    def __exit__(self, type, value, traceback):
        if self.file:
            self.file.close()


def round_decimal(number, currency_decimal_places=2, round_type=ROUND_HALF_UP):
    # Round Decimal variable
    number = Decimal(number)
    number_decimal = str(10**(-currency_decimal_places))
    return number.quantize(Decimal(number_decimal), rounding=round_type)
