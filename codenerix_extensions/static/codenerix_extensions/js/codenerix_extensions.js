/*
 *
 * django-codenerix-extensions
 *
 * Copyright 2017 Centrologic Computational Logistic Center S.L.
 *
 * Project URL : http://www.codenerix.com
 *
 * Licensed under the Apache License, Version 2.0 (the "License");
 * you may not use this file except in compliance with the License.
 * You may obtain a copy of the License at
 *
 * http://www.apache.org/licenses/LICENSE-2.0
 *
 * Unless required by applicable law or agreed to in writing, software
 * distributed under the License is distributed on an "AS IS" BASIS,
 * WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
 * See the License for the specific language governing permissions and
 * limitations under the License.
 */

 function codenerix_extensions(scope, $timeout){
    /*
     * copy the content between fields of the same form
     */
    scope.refresh_lang_field_memory=Array();
    scope.refresh_lang_field = function(field_name, model_name, languages){
        var basefield = model_name+languages[0]+"_"+field_name;
        var otherlangs = languages.slice(1);
        if (scope.refresh_lang_field_memory[basefield] == undefined){
            scope.refresh_lang_field_memory[basefield] = "";
        }
        angular.forEach(otherlangs, function (lang, key) {
            var newfield = model_name+lang+'_'+field_name;
            var value = scope[scope.form_name][newfield].$viewValue;
            if (value == undefined || value==scope.refresh_lang_field_memory[basefield]) {
                $timeout(function () {
                    scope[scope.form_name][newfield].$setViewValue(scope[scope.form_name][basefield].$viewValue);
                    scope[scope.form_name][newfield].$render();
                },500);
            }
        });
        scope.refresh_lang_field_memory[basefield]=scope[scope.form_name][basefield].$viewValue;
    };
}
