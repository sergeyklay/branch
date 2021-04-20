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

(function ($) {
    'use strict';

    $(document).ready(function () {
        trumbowygConfig.btnsDef = {
            image: {
                dropdown: ['insertImage', 'upload'],
                    ico: 'insertImage'
            },
        };

        trumbowygConfig.btns = [
            ['viewHTML'],
            ['undo', 'redo'], // Only supported in Blink browsers
            ['formatting'],
            ['highlight'],
            ['strong', 'em', 'del'],
            ['justifyLeft', 'justifyCenter', 'justifyRight', 'justifyFull'],
            ['superscript', 'subscript'],
            ['unorderedList', 'orderedList'],
            ['link'],
            ['image'],
            ['horizontalRule'],
            ['removeformat'],
            ['fullscreen']
        ];

        trumbowygConfig.minimalLinks = false;
        trumbowygConfig.defaultLinkTarget = '';

        // Editor does nothing on div
        trumbowygConfig.semantic['div'] = 'div';

        trumbowygConfig.plugins = {
            /* TODO: implement me */
            upload: {
                serverPath: '/upload/',
                    fileFieldName: 'image'
            }
        };

        $('textarea.textarea-wysiwyg').trumbowyg(trumbowygConfig);
    });
}($ || django.jQuery));
