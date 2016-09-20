function requisicao(ide){
	console.log("função para saber se existe uma realçao de seguidor");
	$.ajax({
        url : "getrelationship/", // the endpoint
        type : "POST", // http method
        data : { 
        	id : ide,
        	 }, // data sent with the post request

        // handle a successful response
        success : function(json) {
            if (json == false){
            	friend(ide);
            }
            else{
            	unfriend(ide);
            }
        },

        // handle a non-successful response
        error : function(xhr,errmsg,err) {
        	console.log(xhr.status + ": " + xhr.responseText);
           alert("deu errado")

        }
    });
}

function friend(ide) {
	console.log("solicitação de amizade enviada");
	console.log(ide);
	$.ajax({
        url : "follower/", // the endpoint
        type : "POST", // http method
        data : { 
        	id : ide,
        	 }, // data sent with the post request

        // handle a successful response
        success : function(json) {
            $('#seguimento').text("Parar de seguir");// remove the value from the input
            console.log(json); // log the returned json to the console
            console.log("success"); // another sanity check
        },

        // handle a non-successful response
        error : function(xhr,errmsg,err) {
        	console.log(xhr.status + ": " + xhr.responseText);
           alert("deu errado")

        }
    });
}

function unfriend(ide) {
	console.log("amizade desfeita");
	console.log(ide);
	$.ajax({
        url : "unfollower/", // the endpoint
        type : "POST", // http method
        data : { 
        	id : ide,
        	 }, // data sent with the post request

        // handle a successful response
        success : function(json) {
            $('#seguimento').text("Seguir"); // remove the value from the input
            console.log(json); // log the returned json to the console
            console.log("success"); // another sanity check
        },

        // handle a non-successful response
        error : function(xhr,errmsg,err) {
        	console.log(xhr.status + ": " + xhr.responseText);
           alert("deu errado")

        }
    });
}


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