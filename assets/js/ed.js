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
