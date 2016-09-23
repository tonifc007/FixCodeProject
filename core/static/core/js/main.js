//Ajax para seguidores

function requisicao(ide) {
	//console.log("função para saber se existe uma relaçao de seguidor");
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
           alert("deu errado");

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
           alert("deu errado");

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
           alert("deu errado");
        }
    });
}

//AJAX para excluir fix

function alertDelete(ide){
	decisao = confirm("Deseja excluir este fix?");
	if (decisao) {
		console.log("confirmou");
		$.ajax({
        url : "delete_confirm/", // the endpoint
        type : "POST", // http method
        data : { 
        	id : ide,
        	 }, // data sent with the post request

        // handle a successful response
        success : function(json) {
           	window.location.replace("/myfixies/");
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
}

//AJAX para ativar e desativar notificação de fix

function getNotifyMyFix(ide){
	console.log("alternador de notificação de fix");
	$.ajax({
        url : "getnotifymyfix/", // the endpoint
        type : "POST", // http method
        data : { 
        	id : ide,
        	 }, // data sent with the post request

        // handle a successful response
        success : function(json) {
            if (json == false){
            	ativeNotifyMyfix(ide);
            }
            else{
            	inativeNotifyMyfix(ide);
            }
        },

        // handle a non-successful response
        error : function(xhr,errmsg,err) {
        	console.log(xhr.status + ": " + xhr.responseText);
        	alert("deu errado")

        }
    });
}

function ativeNotifyMyfix(ide){
	console.log("ativando notificações");
	console.log(ide);
	$.ajax({
        url : "ativenotifyfix/", // the endpoint
        type : "POST", // http method
        data : { 
        	id : ide,
        	 }, // data sent with the post request

        // handle a successful response
        success : function(json) {
            $('#seg').text("Desativar notificações");// remove the value from the input
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

function inativeNotifyMyfix(ide){
	console.log("desativando notificações");
	console.log(ide);
	$.ajax({
        url : "inativenotifyfix/", // the endpoint
        type : "POST", // http method
        data : { 
        	id : ide,
        	 }, // data sent with the post request

        // handle a successful response
        success : function(json) {
            $('#seg').text("Ativar notificações");// remove the value from the input
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

//AJAX para marcar fix como resolvido

function fixed(ide){
    console.log("Marcando fix como resolvido");
    console.log(ide);
    $.ajax({
        url : "fixed/", // the endpoint
        type : "POST", // http method
        data : { 
            id : ide,
             }, // data sent with the post request

        // handle a successful response
        success : function(json) {
            console.log(json); // log the returned json to the console
            console.log("success"); // another sanity check
            parent.window.document.location.href = '';
        },

        // handle a non-successful response
        error : function(xhr,errmsg,err) {
            console.log(xhr.status + ": " + xhr.responseText);
           alert("deu errado")

        }
    });
}

function restore(ide){
    console.log("Marcando fix como não-resolvido");
    console.log(ide);
    $.ajax({
        url : "restore/", // the endpoint
        type : "POST", // http method
        data : { 
            id : ide,
             }, // data sent with the post request

        // handle a successful response
        success : function(json) {
            console.log(json); // log the returned json to the console
            console.log("success"); // another sanity check
            parent.window.document.location.href = '';
        },

        // handle a non-successful response
        error : function(xhr,errmsg,err) {
            console.log(xhr.status + ": " + xhr.responseText);
           alert("deu errado")

        }
    });
}

//AJAX para escolher melhor solução

function best_answer(ide){
    console.log("Marcando melhor soluçao");
    console.log(ide);
    $("#best"+ide).prepend('<img id="theImg" src="http://i665.photobucket.com/albums/vv15/chuyendoday/Icons/LoadingIcon.gif" />');
    $.ajax({
        url : "best_answer/", // the endpoint
        type : "POST", // http method
        data : { 
            id : ide,
             }, // data sent with the post request

        // handle a successful response

        success : function(json) {
            console.log(json); // log the returned json to the console
            console.log("success"); // another sanity check
            parent.window.document.location.href = '';

        },

        // handle a non-successful response
        error : function(xhr,errmsg,err) {
            console.log(xhr.status + ": " + xhr.responseText);
           alert("deu errado")

        }
    });
}

//AJAX para reportar resposta

function report(ide){
    console.log("Reportando comentário");
    console.log(ide);
    decisao = confirm("Deseja excluir este fix?");
    if (decisao) {
        $.ajax({
            url : "report/", // the endpoint
            type : "POST", // http method
            data : { 
                id : ide,
                 }, // data sent with the post request

            // handle a successful response
            success : function(json) {
                console.log(json); // log the returned json to the console
                console.log("success"); // another sanity check
                parent.window.document.location.href = '';
            },

            // handle a non-successful response
            error : function(xhr,errmsg,err) {
                console.log(xhr.status + ": " + xhr.responseText);
               alert("Não foi possível reportar esta resposta")

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