$(document).ready(function () {

    $('#tx_email').change(function () {


        $('#id_username').val($(this).val());

    });

    $("form[name='register']").validate({
        // Specify validation rules
        rules: {
            // The key name on the left side is the name attribute
            // of an input field. Validation rules are defined
            // on the right side
            first_name: "required",
            last_name: "required",
            email: {
                required: true,
                // Specify that email should be validated
                // by the built-in "email" rule
                email: true,

            },
            username: {
                required: true,
                // Specify that email should be validated
                // by the built-in "email" rule
                equalTo: "#id_username"
            },
            password1: {
                required: true,
                minlength: 8
            },

            password2: {
                required: true,
                minlength: 8,
                 equalTo: "#id_password1"
            }
        },
        // Specify validation error messages
        messages: {
            firs_tname: "Please enter your firstname",
            last_name: "Please enter your lastname",
            email: "Please enter a valid email address",
            password1: {
                required: "Please provide a password",
                minlength: "Your password must be at least 5 characters long"
            },
            password1: {
                required: "Please retype the password",
                equalTo : "Retyped password must be equal to password"
            },

        },
        // Make sure the form is submitted to the destination defined
        // in the "action" attribute of the form when valid
        submitHandler: function (form) {
             //alert('valid form submitted'); // for demo

            form.submit();
        }
    });


});