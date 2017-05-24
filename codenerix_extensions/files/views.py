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
from django.views.generic import View


class DocumentFileView(View):
    def form_valid(self, form, forms=None):
        if 'doc_path' in json.loads(self.request.body) and 'filename' in json.loads(self.request.body)['doc_path']:
            name_file = json.loads(self.request.body)['doc_path']['filename']
            self.request.name_file = name_file
            form.instance.name_file = name_file
        if forms:
            return super(DocumentFileView, self).form_valid(form, forms)
        else:
            return super(DocumentFileView, self).form_valid(form)


class ImageFileView(View):
    def form_valid(self, form, forms=None):
        if 'image' in json.loads(self.request.body) and 'filename' in json.loads(self.request.body)['image']:
            name_file = json.loads(self.request.body)['image']['filename']
            self.request.name_file = name_file
            form.instance.name_file = name_file
        else:
            # compatibility with multiforms
            field_image = "{}_image".format(str(self.form_class).split('.')[-1].replace("'", '').replace('>', ''))
            if field_image in json.loads(self.request.body) and 'filename' in json.loads(self.request.body)[field_image]:
                name_file = json.loads(self.request.body)[field_image]['filename']
                self.request.name_file = name_file
                form.instance.name_file = name_file
        if forms:
            return super(ImageFileView, self).form_valid(form, forms)
        else:
            return super(ImageFileView, self).form_valid(form)
