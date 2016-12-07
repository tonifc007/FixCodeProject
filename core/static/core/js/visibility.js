setTimeout("getNovasMensagens()", 1);
setInterval("getNovasMensagens()", 2000);
setTimeout("verificadispo()", 1);
setInterval("verificadispo()", 5000);


//Comando para quando o enter for apertado no Bate-papo
$(document).keypress(function(e) {
    if(e.which == 13){
        if ($("#campo").val() !== "" && $("#checkenter").is(':checked')) {
            mandaMensagem();
        }

    };
});

function verificadispo() {
    //console.log("função para saber se existe uma relaçao de seguidor");
    console.log(a);
    $.ajax({

        url : "/verificadispo/", // the endpoint
        type : "POST", // http method
        data : { 
            id : a,
             }, // data sent with the post request
             
        // handle a successful response
        success : function(json) {
            if (json == "Online") {
                $("#on").html("<p style='color: #FFD700'; text-align: center; >Online</p>");
            }
            else{
              $("#on").html(json);  
            }
            
            console.log("Tempo de diferença: " + json);
        },

        // handle a non-successful response
        error : function(xhr,errmsg,err) {
            console.log(xhr.status + ": " + xhr.responseText);
           

        }
    });
}

function getNovasMensagens(){

    $.ajax({
        url : "notview/", // the endpoint
        type : "GET", // http method

        success : function(json) {
            console.log(json); // log the returned json to the console
            console.log("success"); // another sanity check
            console.log('muda');
            for (var i = 0; i < json.length; i++) {
                console.log(json[i][0])
                $('#newmessage').append("<p class='msg-receptor'>"+ json[i][0] +"</p>");
                goToFinal();
            }
            leMensagens();

        },

        // handle a non-successful response
        error : function(xhr,errmsg,err) {
            console.log(xhr.status + ": " + xhr.responseText);
            console.log('offline');

        }
    });

}

function leMensagens(){

    $.ajax({
        url : "read/", // the endpoint
        type : "GET", // http method

        success : function(json) {
            console.log(json); // log the returned json to the console

        },

        // handle a non-successful response
        error : function(xhr,errmsg,err) {
            console.log(xhr.status + ": " + xhr.responseText);
            console.log('offline');

        }
    });

}

function mandaMensagem(){
    var campo = $("#campo").val();
    if (campo !== ""){
        $.ajax({
            url : "send/", // the endpoint
            type : "POST", // http method
            data : {
                id : campo,
                 }, // data sent with the post request

            // handle a successful response
            success : function(json) {
                if (json != false){
                    $('#newmessage').append("<div class='col-xs-12'><p class='msg-emissor pull-right'>"+ json +"</p></div>");
                    goToFinal();
                    $("#campo").val('');
                }
                else{
                    alert("Não foi possivel enviar mensagem")
                }
                

            },

            // handle a non-successful response
            error : function(xhr,errmsg,err) {
                console.log(xhr.status + ": " + xhr.responseText);
               alert("deu errado");

            }
        
        });
    }


}

function goToFinal(){
    $(".nano").nanoScroller({ flash: true });
    $(".nano").nanoScroller({ scroll: 'bottom' });
}

//Cookies globais padrões para utilização do AJAX

function getCookie(name) {
        var cookieValue = null;
        var i = 0;
        if (document.cookie && document.cookie !== '') {
            var cookies = document.cookie.split(';');
            for (i; i < cookies.length; i++) {
                var cookie = jQuery.trim(cookies[i]);
                // Does this cookie string begin with the name we want?
                if (cookie.substring(0, name.length + 1) === (name + '=')) {
                    cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
                    break;
                }
            }
        }
        return cookieValue;
    }
    var csrftoken = getCookie('csrftoken');

    function csrfSafeMethod(method) {
        // these HTTP methods do not require CSRF protection
        return (/^(GET|HEAD|OPTIONS|TRACE)$/.test(method));
    }
    $.ajaxSetup({
        crossDomain: false, // obviates need for sameOrigin test
        beforeSend: function(xhr, settings) {
            if (!csrfSafeMethod(settings.type)) {
                xhr.setRequestHeader("X-CSRFToken", csrftoken);
            }
        }
    });

$(".nano").nanoScroller({ scroll: 'bottom' });