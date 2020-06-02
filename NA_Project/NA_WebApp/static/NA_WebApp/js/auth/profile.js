$(document).ready(function () {


    $('#img_Avatar').click(function () {

        alert("hi from profile !");
        //add upload profile avatar image codes here

    });


    //hide original form inputs for lat and lng :
    // $('#div_id_lat').hide();
    //  $('#div_id_lng').hide();

    //set their value to the visible mock ones ,  if they changed
    $("[name='lat']").change(function () {
        $('#txLat').val($(this).val());
    });

    $("[name='lng']").change(function () {
        $('#txLng').val($(this).val());
    });


    //here how to add google maps API key :
    //add this :
    //<script src="https://maps.googleapis.com/maps/api/jskey=YOUR_API_KEY&callback=initMap"async defer></script>
    //and get the API key from :
    //https://developers.google.com/maps/documentation/javascript/get-api-key


    var deflat = $('#id_lat').val();// 41.086203 // Boğaziçi Kuzey Kampus
    var deflng = $('#id_lng').val();//29.044378 // Boğaziçi Kuzey Kampus
    $('#Map_Geo').locationpicker({
        location: {
            latitude: deflat,
            longitude: deflng
        },
        radius: 300,
        inputBinding: {
            latitudeInput: $('#id_lat'),
            longitudeInput: $('#id_lng'),
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

//------------------------------------------------------------------- my prefrences -------------------------------------

    //make searcher test :
    $('#txDis').makeSearcher({
        searchUrl: 'diseaseSearch',
        addUrl: 'diseaseAddNew',
        addNewText: "Click here to create this disease",
        selectedListComponent: $('#divSelectDiseases'),
        returnSelectedItemsCallBack: function (items) {

            //this callback will be fired from the this plugin and items are selected item objects will be :
            // items : [ {'id' : 1 , 'value' : 'xxxx' }, {'id' : 2 , 'value' : 'yyyyy' }...]

            $.each(items, function (index, item) {
                alert("item id : " + item.id + " item value : " + item.value);
            });

        }
    });

    $('#btnsaveme').click(function () {

        $('#txDis').getSelectedItems();

    });


});