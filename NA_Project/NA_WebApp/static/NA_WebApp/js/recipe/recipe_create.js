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
                url: '../api/getFoods/',
                headers: {'X-CSRFToken': my_csrf_token},
                dataType: "json",
                cache: false,
                data: {term: request.term},
                success: function (data) {
                    $('#apiErrors').html('');
                    response(data);
                }
            }).fail(function (jqXHR, textStatus) {
                $('#apiErrors').html('<span>' + jqXHR.status + ': ' + jqXHR.statusText + '</span><p class="text-danger">' + jqXHR.responseJSON.error + '</p>').css('display', 'block');
            });

        },
        minLength: 1,
        select: function (event, ui) {

            $(this).data("value", ui.item.value);
            $(this).data("name", ui.item.label);

            //set searchtext manually ( otherwise it sets value to text !)
            $(this).val(ui.item.label);

            //send the selected ingredient to our api
            $.ajax({
                method: "POST",
                url: '../api/getNutrients/',
                headers: {'X-CSRFToken': my_csrf_token},
                dataType: "json",
                cache: false,
                data: {'ingredientIdddddd': ui.item.value},
                success: function (data) {

                    //we have now the portions , set them to select element


                }
            }).fail(function (jqXHR, textStatus) {
                $('#apiErrors').html('<span>' + jqXHR.status + ': ' + jqXHR.statusText + '</span><p class="text-danger">' + jqXHR.responseJSON.error + '</p>').css('display', 'block');
            });

            return false;

        },
        response: function (event, ui) {

        }
    });


    //add new ingredient :
    $('#btn_addIngredient').click(function () {

        let quantity = $('#txQuantity').val();

        let ingr = new Ingredient();
        ingr.getFrom_TextBox();

        let uni = new Unit();
        uni.getFrom_TextBox();

        let rec_ing = new Recipe_Ingredient(ingr, uni, quantity);
        let iManager = new IngredientManager();
        iManager.addNewIngredient(rec_ing);


    });


});


class Ingredient {

    getFrom_TextBox() {
        this.id = $('#txIngredient').data("value");
        this.text = $('#txIngredient').data("name");
    }

    getfrom_Table(table_row) {
        //gte the first td and pull data for ingredient
        const td = table_row.find('td:first');
        this.id = td.data('ingredient');
        this.text = td.text();
    }
}

class Unit {


    getFrom_TextBox() {
        this.id = $('#txUnit').val();
        this.text = $('#txUnit option:selected').text();
    }

}

class Recipe_Ingredient {

    constructor(_ingredient, _unit, _quantity) {
        this.recipeId = $('#recipeId').text();
        this.ingredient = _ingredient;
        this.unit = _unit;
        this.quantity = _quantity;
        this.calcGrams = 100;
    }
}

class IngredientManager {


    addNewIngredient(recipe_ingredient) {

        let r = recipe_ingredient;


        if (r.ingredient.id > 0 && r.quantity > 0 && r.unit.id > 0) {

            let new_ingredient = {
                recipeId: r.recipeId,
                ingredientId: r.ingredient.id,
                amount: r.calcGrams
            };

            //first send to back end for adding to db
            const csrftoken = Cookies.get('csrftoken');
            const manager = this;

            $.ajax({
                headers: {'X-CSRFToken': csrftoken},
                method: "POST",
                url: 'recipeAddIngredient',
                data: {'new_ingredient': JSON.stringify(new_ingredient)},
            }).done(function (data) {

                //post is successfull add a row to the table :
                manager.addToTable(r);

            }).fail(function (jqXHR, textStatus) {


                // alert(jqXHR.status); // the status code
                alert(jqXHR.responseJSON.error); // the message

                $('#p_error').html('<span>' + jqXHR.status + ': ' + jqXHR.statusText + '</span><p class="text-danger">' + jqXHR.responseJSON.error + '</p>').css('display', 'block');

            });


        }

    }

    addToTable(recipe_ingredient) {

        let r = recipe_ingredient;
        let manager = this;

        //add a new tr to table
        $('#Tbl_Ingredients > tbody').append(
            "<tr>" +
            "<td data-ingredient='" + r.ingredient.id + "'>" + r.ingredient.text + "</td>" +
            "<td>" + r.quantity + "</td>" +
            "<td data-unit='" + r.unit.id + "'>" + r.unit.text + "</td>" +
            "<td>" + r.calcGrams + "</td>" +
            "<td><a class='btn btn-danger btn-sm text-white'>x</a></td>" +
            "</tr>"
        );

        $('#txIngredient').data("value", "0").data("name", "").val("");
        $('txQuantity').val(0);

        //set click events of delete buttons
        $('#Tbl_Ingredients a').unbind("click").click(function () {

            const table_row = $(this).parent().parent();
            manager.deleteIngredient(table_row);

        });


    }

    deleteIngredient(tblrow) {

        //get ingredient to del
        let del_ing = new Ingredient()
        del_ing.getfrom_Table(tblrow);

        //crate recipe_ingredient obj
        let recipe_ing = new Recipe_Ingredient(del_ing, null, null);
        //send ajax call to delete from db

        let del_ingredient = {
            recipeId: recipe_ing.recipeId,
            ingredientId: recipe_ing.ingredient.id
        }
        const csrftoken = Cookies.get('csrftoken');

        $.ajax({
            headers: {'X-CSRFToken': csrftoken},
            method: "POST",
            url: 'recipeDeleteIngredient',
            data: {'del_ingredient': JSON.stringify(del_ingredient)},
        }).done(function (data) {

            //post is successfull remove the row to the table :
            tblrow.remove();

        }).fail(function (jqXHR, textStatus) {

            // alert(jqXHR.status); // the status code
            alert(jqXHR.responseJSON.error); // the message
            $('#p_error').html('<span>' + jqXHR.status + ': ' + jqXHR.statusText + '</span><p class="text-danger">' + jqXHR.responseJSON.error + '</p>').css('display', 'block');

        });


    }
}