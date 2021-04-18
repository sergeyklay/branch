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
    // Override the submit event
    $(document).on('submit', '#contact-form', function (e) {
        // Clear previous classes
        $('.contact-form-item-error')
            .removeClass('contact-form-item-error');

        // Get form elements
        let emailField   = $('.contact-form-input[name="email"]'),
            nameField    = $('.contact-form-input[name="name"]'),
            messageField = $('.contact-form-textarea[name="message"]'),
            gotchaField  = $('.contact-form-gotcha');

        // Validate email
        if (nameField.val().length === 0) {
            nameField
                .closest('.contact-form-item')
                .addClass('contact-form-item-error');
        }

        // Validate name
        if (emailField.val().length === 0) {
            emailField
                .closest('.contact-form-item')
                .addClass('contact-form-item-error');
        }

        // Validate message
        if (messageField.val().length === 0) {
            messageField
                .closest('.contact-form-item')
                .addClass('contact-form-item-error');
        }

        // If all fields are filled, except gotcha
        if (emailField.val().length === 0   ||
            nameField.val().length === 0    ||
            messageField.val().length === 0 ||
            gotchaField.val().length !== 0) {
            e.preventDefault();
        }
    });
}(jQuery));
