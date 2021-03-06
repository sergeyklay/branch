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

function isDoNotTrackEnabled() {
    if (typeof window === 'undefined') return false
    const {doNotTrack, navigator} = window

    // Do Not Track Settings across browsers
    const dnt = (doNotTrack || navigator.doNotTrack || navigator.msDoNotTrack)

    if (!dnt) return false

    return dnt === true ||
        dnt === 1 ||
        dnt === 'yes' ||
        (typeof dnt === 'string' && dnt.charAt(0) === '1');
}

if (isDoNotTrackEnabled()) {
    // Skip analytics for users with Do Not Track enabled
    console.info('[TRACKING]: Respecting DNT with respect to analytics...')
} else {
    // Known DNT values not set, so we will assume it's off.
    const data = JSON.parse(document.getElementById('branch-data').innerHTML)

    if (typeof data !== 'undefined' && data.analytics_code) {
        (function () {
            // New Google Site Tag (gtag.js) tagging/analytics framework
            // See: https://developers.google.com/gtagjs
            const base_url = 'https://www.googletagmanager.com'
            let script = document.createElement("script");

            script.src = base_url + "/gtag/js?id=" + data.analytics_code;
            script.type = "text/javascript";
            script.async = true;

            document.getElementsByTagName("head")[0].appendChild(script);
        }())

        window.dataLayer = window.dataLayer || [];

        function gtag() {
            dataLayer.push(arguments);
        }

        gtag('js', new Date());

        // Setup the project analytics code and send a pageview
        gtag('config', data.analytics_code, {
            'anonymize_ip': true,
            'cookie_expires': 30 * 24 * 60 * 60  // 30 days
        })
    }
}
