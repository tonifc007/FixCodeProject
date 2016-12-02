setTimeout("getNovasMensagens()", 1);
setInterval("getNovasMensagens()", 2000);

function getNovasMensagens(){

    $.ajax({
        url : "notview/", // the endpoint
        type : "GET", // http method

        success : function(json) {
            console.log(json); // log the returned json to the console
            console.log("success"); // another sanity check
            console.log('muda');
            for (var i = 0; i < json.length; i++) {
                $('#newmessage').html("<p>"+ json[i].message +"</p>");
            }
   
        },

        // handle a non-successful response
        error : function(xhr,errmsg,err) {
            console.log(xhr.status + ": " + xhr.responseText);
            console.log('offline');

        }
    });

}