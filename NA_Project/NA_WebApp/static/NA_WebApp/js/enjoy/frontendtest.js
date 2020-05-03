$(document).ready(function () {


    $('#btnJQuery').click(function () {

        alert("selam");
        $('#p1').html('This is the proof that we can use jQuery in this page! And this is an external js file.');

    });

    $('#btnAjaxget').click(function () {


        $.ajax({
            method: "GET",
            url: 'ajaxget',
            data: '',
            success: function (data) {
                //alert ("ajax ok , result is : " + data  )
            },
            error: function (jqXHR, textStatus, errorThrown) {
                $('#p_error').html(jqXHR);
            }
        }).done(function (data) {
            alert("ajax  get is ok , result is : " + data)
        }).fail(function (jqXHR, textStatus) {

            $('#p_error').html(jqXHR.statusText + ' ' + textStatus);
        });
    });


    $('#btnAjaxpost').click(function () {

        var csrftoken = Cookies.get('csrftoken');

        $.ajax({
            headers: {'X-CSRFToken': csrftoken},
            method: "POST",
            url: 'ajaxpost',
            data: {'data': JSON.stringify({'key1': 'value1', 'key2' : 'value2'})},
        }).done(function (data) {

            alert("ajax  post is ok , result is : " + data)

        }).fail(function (jqXHR, textStatus) {

            $('#p_error').html(jqXHR.statusText + ' ' + textStatus);
        });
    });

});