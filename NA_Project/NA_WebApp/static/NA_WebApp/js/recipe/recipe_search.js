$(document).ready(function () {



    $('.entry > figure').height($('.entry > figure').first().width());
    $('.entry > figure > img').height($('.entry > figure').first().width());



    $('#btnSearch').click(function () {

        window.location.replace('recipe_search?term=' + $('#txSearch').val())

    });

});