setTimeout("alterTL()", 1);
setInterval("alterTL()", 5000);

function alterTL(){

    $.ajax({
        url : "/timeline/", // the endpoint
        type : "GET", // http method

        success : function(json) {
            console.log("Posts antigos: "+pantigo)
            console.log("Posts da timeline: "+ json);
            if (json > pantigo) {
                var sub = json - pantigo;
                $('#recarrega').html("<a class='btn btn-default btn-block' style='margin-bottom: 6px;' href='/'>"+sub+" novos posts. Recarregue a página.</a>");
            }
            
        },

        // handle a non-successful response
        error : function(xhr,errmsg,err) {
            console.log(xhr.status + ": " + xhr.responseText);
            console.log('offline');

        }
    });

}