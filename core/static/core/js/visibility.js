setTimeout("getNovasMensagens()", 1);
setInterval("getNovasMensagens()", 2000);

$(document).keypress(function(e) {
    if(e.which == 13){
        if ($("#campo").val() !== "" && $("#checkenter").is(':checked')) {
            console.log("Botão enter foi apertado");
        }

    };
});

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
                $('#newmessage').append("<p style='color: red;'>"+ json[i][0] +"</p>");
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
                    $('#newmessage').append("<p style='color: blue;'>(eu) - "+ json +"</p>");
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
