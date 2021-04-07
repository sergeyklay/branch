// Copyright (C) 2021 Serghei Iakovlev <egrep@protonmail.ch>
//
// This file is free software; you can redistribute it and/or
// modify it under the terms of the GNU General Public License
// as published by the Free Software Foundation; either version 3
// of the License, or (at your option) any later version.
//
// This file is distributed in the hope that it will be useful,
// but WITHOUT ANY WARRANTY; without even the implied warranty of
// MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
// GNU General Public License for more details.
//
// You should have received a copy of the GNU General Public License
// along with this file.  If not, see <https://www.gnu.org/licenses/>.

/**
 * This is an override of django's default `jquery.init.js` file.
 *
 * By default, the django admin loads jquery in a custom `django.jQuery`
 * namespace so the `$` and `jQuery` variables are not populated.
 *
 * This does not suit us since we are using plugins (Trumbowyg, notabl) that
 * rely on the `jQuery` variable being populated.
 *
 * Therefore, we have two choices:
 *  1) loading a duplicate version of jquery to populate the `jQuery`
 *     variable or…
 *  2) preventing Django to override it in the first place.
 *
 * See jQuery's api for more info:
 * https://api.jquery.com/jQuery.noConflict/
 */

var django = django || {};
django.jQuery = jQuery.noConflict(false);
