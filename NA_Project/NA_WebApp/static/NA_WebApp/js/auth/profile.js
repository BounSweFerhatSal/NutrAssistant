$(document).ready(function () {


    $('#img_Avatar').click(function () {

        alert("hi from profile !");
        //add upload profile avatar image codes here

    });

    //here how to add google maps API key :
    //add this :
    //<script src="https://maps.googleapis.com/maps/api/jskey=YOUR_API_KEY&callback=initMap"async defer></script>
    //and get the API key from :
    //https://developers.google.com/maps/documentation/javascript/get-api-key

    $('#Map_Geo').locationpicker({
        location: {
            latitude: 41.086203 ,
            longitude: 29.044378
        },
        radius: 300,
        inputBinding: {
            latitudeInput: $('#Map-lat'), // Boğaziçi Kuzey Kampus
            longitudeInput: $('#Map-lon'),
            //radiusInput: $('#us3-radius'),
            //locationNameInput: $('#us3-address')
        },
        enableAutocomplete: true,
        onchanged: function (currentLocation, radius, isMarkerDropped) {
            // Uncomment line below to show alert on each Location Changed event
            //alert("Location changed. New location (" + currentLocation.latitude + ", " + currentLocation.longitude + ")");
        }
    });


    $("form[name='login']").validate({
        // Specify validation rules
        rules: {
            // The key name on the left side is the name attribute
            // of an input field. Validation rules are defined
            // on the right side
            //firstname: "required",
            //lastname: "required",
            email: {
                required: true,
                // Specify that email should be validated
                // by the built-in "email" rule
                email: true
            },
            password: {
                required: true,
                minlength: 8
            }
        },
        // Specify validation error messages
        messages: {
            //firstname: "Please enter your firstname",
            //lastname: "Please enter your lastname",
            password: {
                required: "Please provide a password",
                minlength: "Your password must be at least 5 characters long"
            },
            email: "Please enter a valid email address"
        },
        // Make sure the form is submitted to the destination defined
        // in the "action" attribute of the form when valid
        submitHandler: function (form) {
            //alert('valid form submitted'); // for demo

            form.submit();
        }
    });


});