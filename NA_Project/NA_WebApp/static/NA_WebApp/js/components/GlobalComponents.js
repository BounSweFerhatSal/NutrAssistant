(function ($) {


    /*
        MakeSearcher plugin can be applied to an input ,
        converts it to an auto complete ,
        if the result of a search is null , it provides a create new  item in the auto complete section  and if user selects it it send an ajax post
        if user select an item , plugin adds the item to a list ( a div with spans as items) , and they can be removed by a button

        usage ( min opt ) :

         <input type="text"  id="txDis"  selectorDiv="divSelectDiseases">

        $('#txDis').makeSearcher({
            searchUrl: 'urltosearch',
            addUrl: 'urltoaddnewitems',
            addNewText: "Click here to create this disease"

        });


     */
    $.fn.makeSearcher = function (opts) {

        let options = {

            searchUrl: "",
            addUrl: "",
            addNewText: "Click here to create",
            badgeStyle: 'warning',
            selectedListComponent: $('#' + $(this).attr('selectorDiv')),
            addToSelectedListFunction: function addToSelectedList(val, label) {

                //debugger

                const remove_btn = '<button type="button" class="close"  aria-label="Close">\n' +
                    '    <span aria-hidden="true">×</span>\n' +
                    '  </button>';


                let new_item = '<span class="badge  badge-' + options.badgeStyle + '" makeSelectorItem  data-itemval="' + val + '" data-itemlabel="' + label + '" >' + label + ' ' +
                    '  <button type="button" class="close" aria-label="Dismiss">' +
                    '    <span aria-hidden="true">x</span>' +
                    '  </button>' +
                    '</span>'

                options.selectedListComponent.append(new_item);


                options.selectedListComponent.find('.close').unbind("click").click(function () {
                    $(this).parent().remove();

                });

            }
        };
        options = $.extend({}, options, opts);


        //for django get the token :
        //use this :
        //<script src="https://cdn.jsdelivr.net/npm/js-cookie@rc/dist/js.cookie.min.js"></script>
        const my_csrf_token = Cookies.get('csrftoken');

        //for chrome debuugger
        // debugger


        //apply auto complete
        $(this).autocomplete({
            source: function (request, response) {
                //our source is a server side api
                $.ajax({
                    method: "POST",
                    url: options.searchUrl,
                    headers: {'X-CSRFToken': my_csrf_token},
                    dataType: "json",
                    cache: false,
                    data: {term: request.term},
                    success: function (data) {
                        //If there is no corresponding result from the source data with the entered search term
                        //return an item for the select which says click here to "add a new record"
                        if (data.length === 0) {
                            data = [{'label': options.addNewText, "value": -1}];
                        }
                        //  debugger

                        response(data);
                    }
                });
            },
            minLength: 1,
            select: function (event, ui) {

                //if the user selected "add a new record "(which we added if no match )
                //post an ajax for creating a new record
                //if post is succeed , add the item to the selected items list
                if (ui.item.value === -1) {


                    $.ajax({
                        url: options.addUrl,
                        type: 'POST',
                        headers: {'X-CSRFToken': my_csrf_token},
                        dataType: "json",
                        cache: false,
                        data: {
                            term: $(this).val()
                        },
                        success: function (data) {
                            if (data.value !== 0) {
                                //if everything ok , add the newly created item to the "list of selected items"
                                options.addToSelectedListFunction(data.value, data.label);

                            }
                        }
                    });

                    //clear the search text
                    $(this).val('');
                    return false;

                } else {

                    //if user selected a record already in the list , just add it to  "list of selected items"
                    options.addToSelectedListFunction(ui.item.value, ui.item.label);

                    //clear the search text
                    $(this).val('');
                    return false;
                }
            },
            response: function (event, ui) {

            }
        }).data("ui-autocomplete")._renderItem = function (ul, item) {

            return $("<li></li>")
                .data("ui-autocomplete-item", item)
                .append("<a>" + item.label + "</a>")
                .appendTo(ul);
        };


        //allow chaining !
        return this;
    }

    //this plugin is to get the selected item from a makeselector plugin
    $.fn.getSelectedItems = function () {

        //   debugger;

        const selDiv = $('#' + $(this).attr('selectorDiv'));
        // items : [ {'id' : 1 , 'value' : 'xxxx' }, {'id' : 2 , 'value' : 'yyyyy' }...]

        const items = selDiv.find('[makeSelectorItem]');
        let retData = [];

        $.each(items, function (index, item) {

            const val = $(this).data('itemval');
            const label = $(this).data('itemlabel');
            retData.push({'value': val, 'label': label});

            //console.log("item label : " +  label + " item value : " + val);

        });

        // console.log(retData);
        return retData;
    }

    //this plugin is to get the selected item values and return them as an array
    $.fn.getSelectedItemsVals = function () {


        let sels = $(this).getSelectedItems();
        let dataArray = [];
        $.each(sels, function (idx, item) {
            dataArray.push(item.value);
        });


        return dataArray;
    }

}(jQuery));