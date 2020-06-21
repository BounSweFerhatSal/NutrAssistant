$(document).ready(function () {


    $("#Recipe-wizard").steps({
        headerTag: "h3",
        bodyTag: "section",
        transitionEffect: "slideLeft",
        autoFocus: true,

        /* Events */
        onStepChanging: function (event, currentIndex, newIndex) {

            if (currentIndex === 0 && $('#recipeId').text() === "") {
                //if form is not saved yet:
                $("#frmrecipe").submit();
            }


            return true;
        },
        onStepChanged: function (event, currentIndex, priorIndex) {
        }

    });


    //if form is already submitted and the recipe created , just go to next wizard step:
    if ($('#done').val() === "true") {
        $("#Recipe-wizard").steps("next");
    }

    //ingredient auto complete :
    const my_csrf_token = Cookies.get('csrftoken');
    $('#txIngredient').autocomplete({
        source: function (request, response) {
            //our source is a server side api
            $.ajax({
                method: "POST",
                url: '../auth/search_ingredients',
                headers: {'X-CSRFToken': my_csrf_token},
                dataType: "json",
                cache: false,
                data: {term: request.term},
                success: function (data) {

                    response(data);
                }
            });
        },
        minLength: 1,
        select: function (event, ui) {

            $(this).data("value", ui.item.value);
            $(this).data("name", ui.item.label);

            // //clear the search text
            $(this).val(ui.item.label);
            return false;

        },
        response: function (event, ui) {

        }
    });


    $('#btn_addIngredient').click(function () {

        let ing = $('#txIngredient').data("value");
        let ingName = $('#txIngredient').data("name");
        let quantity = $('#txQuantity').val();
        let unit = $('#txUnit').val();
        let unitText = $('#txUnit option:selected').text();
        let calcGrams = 100;

        if (ing > 0 && quantity > 0 && unit > 0) {

            let new_ingredient = {
                recipeId: $('#recipeId').text(),
                ingredientId: ing,
                amount: calcGrams
            };


            //first send to back end for adding to db
            const csrftoken = Cookies.get('csrftoken');
            $.ajax({
                headers: {'X-CSRFToken': csrftoken},
                method: "POST",
                url: 'recipeAddIngredient',
                data: {'new_ingredient': JSON.stringify(new_ingredient)},
            }).done(function (data) {

                //post is successfull add a row to the table :
                $('#Tbl_Ingredients > tbody').append(
                    "<tr>" +
                    "<td data-ingredient='" + ing + "'>" + ingName + "</td>" +
                    "<td>" + quantity + "</td>" +
                    "<td data-unit='" + unit + "'>" + unitText + "</td>" +
                    "<td>" + calcGrams + "</td>" +
                    "<td><a class='btn btn-danger btn-sm text-white'>x</a></td>" +
                    "</tr>"
                );
                $('#txIngredient').data("value", "0").data("name", "").val("");
                $('txQuantity').val(0);

                $('#Tbl_Ingredients a').unbind("click").click(function () {
                    $(this).parent().parent().remove();
                });

            }).fail(function (jqXHR, textStatus) {


                // alert(jqXHR.status); // the status code
                 alert(jqXHR.responseJSON.error); // the message

                $('#p_error').html('<span>' + jqXHR.status + ': ' + jqXHR.statusText + '</span><p class="text-danger">' + jqXHR.responseJSON.error + '</p>').css('display', 'block');

            });


        }

    });


});

