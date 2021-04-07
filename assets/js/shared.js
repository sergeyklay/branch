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

var trumbowygConfig = {
    lang: 'en',
    btnsDef: {
        image: {
            dropdown: ['insertImage', 'upload'],
            ico: 'insertImage'
        },
    },
    btns: [
        ['viewHTML'],
        ['undo', 'redo'], // Only supported in Blink browsers
        ['formatting'],
        ['strong', 'em', 'del'],
        ['superscript', 'subscript'],
        ['link'],
        ['justifyLeft', 'justifyCenter', 'justifyRight', 'justifyFull'],
        ['unorderedList', 'orderedList'],
        ['horizontalRule'],
        ['removeformat'],
        ['fullscreen']
    ],
    semantic: {
        'b': 'strong',
        'i': 'em',
        's': 'del',
        'strike': 'del',
        'div': 'p'
    },
    minimalLinks: true,
    removeformatPasted: true,
    svgPath: '/static/vendor/trumbowyg/ui/icons.svg',
    plugins: {
        /* TODO: implement me */
        upload: {
            serverPath: '/upload/',
            fileFieldName: 'image'
        }
    },
    defaultLinkTarget: '_blank',
}
