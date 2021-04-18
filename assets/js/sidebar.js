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

// Toggle sidebar
(function(document) {
    let toggle = document.querySelector('.sidebar-toggle');
    let sidebar = document.querySelector('#sidebar');
    let checkbox = document.querySelector('#sidebar-checkbox');

    document.addEventListener(
        'click',
        /** @param {MouseEvent} [e] */
        function(e) {
            /** @type {HTMLHtmlElement} */
            const target = e.target;

            // This will work only if DNT is not enabled and GA ID is set
            if (window.gtag && !checkbox.checked && target === toggle) {
                // We are going to show sidebar
                gtag('event', 'show_menu', {
                    'event_label': 'ui_interaction'
                });
            }

            if (!checkbox.checked || !sidebar.contains(target) ||
                (target === checkbox || target === toggle)
            ) {
                return;
            }

            checkbox.checked = false;
        }, false);
})(document);
