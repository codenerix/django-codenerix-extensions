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

from django.views.generic.edit import CreateView, UpdateView
from django.db import transaction
from django.forms.utils import ErrorList

from codenerix.views import GenBase, GenModify
from codenerix.exceptions import CodenerixException

from codenerix_extensions.helpers import get_external_model


class GenCreateBridge(GenModify, GenBase, CreateView):
    def form_valid_bridge(self, form, field, model, related_field, error_message):
        """
        call from form_valid.
        @form: it is form of form_valid (type: form)
        @field: name of the form field referring to the brigde (type: string)
        @model: form's model (type class)
        @related_field: name of the related_name of the brigde (type: string)
        @error_message: list of message errors (type list)
            two items, example:
            ["The selected entry is already a storage, select another entry!",
            "The selected entry is not available anymore, please, try again!"]
        """
        # get instance of selected external object
        external = form.cleaned_data[field]
        related_object = get_external_model(model).objects.filter(pk=external.pk).first()
        if related_object:
            # form valid
            try:
                with transaction.atomic():
                    result = super(GenCreateBridge, self).form_valid(form)
                    if get_external_model(model).objects.filter(**{
                            "pk": external.pk,
                            "{}__isnull".format(related_field): False
                    }).exists():
                        errors = form._errors.setdefault(field, ErrorList())
                        errors.append(error_message[0])
                        raise CodenerixException()
                    else:
                        setattr(related_object, related_field, form.instance)
                        related_object.save()
                        return result
            except CodenerixException:
                return super(GenCreateBridge, self).form_invalid(form)
        else:
            errors = form._errors.setdefault(field, ErrorList())
            errors.append(error_message[1])
            return super(GenCreateBridge, self).form_invalid(form)


class GenUpdateBridge(GenModify, GenBase, UpdateView):
    def form_valid_bridge(self, form, field, model, related_field, error_message):
        """
        call from form_valid.
        @form: it is form of form_valid (type: form)
        @field: name of the form field referring to the brigde (type: string)
        @model: form's model (type class)
        @related_field: name of the related_name of the brigde (type: string)
        @error_message: list of message errors (type list)
            one item, example:
            ["The selected entry is not available anymore, please, try again!", ]
        """
        # get instance of selected external object
        external = form.cleaned_data[field]
        object_edit = model.objects.get(pk=form.instance.pk)
        if object_edit.external == external:
            return super(GenUpdateBridge, self).form_valid(form)
        else:
            related_object = get_external_model(model).objects.filter(**{
                "pk": external.pk,
                "{}__isnull".format(related_field): False
            }).exclude(**{
                "{}".format(related_field): form.instance,
            }).first()
            if not related_object:
                # form valid
                try:
                    with transaction.atomic():
                        result = super(GenUpdateBridge, self).form_valid(form)
                        field = object_edit.external
                        setattr(field, related_field, None)
                        field.save()
                        setattr(external, related_field, form.instance)
                        external.save()
                        return result
                except CodenerixException:
                    return super(GenUpdateBridge, self).form_invalid(form)
            else:
                errors = form._errors.setdefault(field, ErrorList())
                errors.append(error_message[0])
                return super(GenUpdateBridge, self).form_invalid(form)
