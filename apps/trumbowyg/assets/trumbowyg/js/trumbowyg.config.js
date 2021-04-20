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

let trumbowygConfig = {
    /* TODO: get language from branch-data */
    lang: 'en',
    btns: [
        ['undo', 'redo'], // Only supported in Blink browsers
        ['formatting'],
        ['highlight'],
        ['strong', 'em', 'del'],
        ['superscript', 'subscript'],
        ['unorderedList', 'orderedList'],
        ['link'],
        ['horizontalRule'],
        ['removeformat'],
    ],
    semantic: {
        'b': 'strong',
        'i': 'em',
        's': 'del',
        'strike': 'del',
        'div': 'p',
    },
    // Reduce the link overlay to use only 'url' and 'text' fields,
    // omitting 'title' and 'target'
    minimalLinks: true,
    removeformatPasted: true,
    svgPath: '/static/trumbowyg/dist/ui/icons.svg',
    // Allow to set link target attribute value to what you want,
    // even if the 'minimalLinks' option is set to true.
    defaultLinkTarget: '_blank',
};
