function ShowMessage(title, text) {

    let dialog = '<div id="dialog-message" title="' + title + '">' +
    '  <p>' + text + '</p>' +
    '</div>';

    $('body').append(dialog);


    $( "#dialog-message" ).dialog({
      modal: true,
      width: 500,
      buttons: {
        Ok: function() {
          $( this ).dialog( "close" );
          $( this ).remove();
        }
      }
    });



}
