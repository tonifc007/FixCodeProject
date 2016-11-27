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
            $('#seguimento').addClass('btn-danger').removeClass('btn-success');
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
            $('#seguimento').addClass('btn-success').removeClass('btn-danger');
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
            $('#seg').addClass('notifix');
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
            $('#seg').removeClass('notifix');// remove the value from the input
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
    $("#best"+ide).removeClass('btn-primary').addClass('btn-default');
    $("#best"+ide).html('<img src="/static/core/imagens/loading.gif" width="15" heigth="15">');
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

//AJAX para desfavoritar fix

function requisicaoFavorite(ide) {
    //console.log("função para saber se existe uma relaçao de seguidor");
    $.ajax({
        url : "getRelationshipFavorite/", // the endpoint
        type : "POST", // http method
        data : { 
            id : ide,
             }, // data sent with the post request
             
        // handle a successful response
        success : function(json) {
            if (json == false){
                console.log('está falso');
                favorite(ide);
            }
            else{
                console.log('está verdadeiro');
                unfavorite(ide);
            }
        },

        // handle a non-successful response
        error : function(xhr,errmsg,err) {
            console.log(xhr.status + ": " + xhr.responseText);
           alert("deu errado");

        }
    });
}

function favorite(ide){
        $.ajax({
        url : "favorite/", // the endpoint
        type : "POST", // http method
        data : { 
            id : ide,
             }, // data sent with the post request
             
        // handle a successful response
        success : function(json) {
            $('#fav').addClass('notifix');
        },

        // handle a non-successful response
        error : function(xhr,errmsg,err) {
            console.log(xhr.status + ": " + xhr.responseText);
           alert("deu errado");

        }
    });
}

function unfavorite(ide){
        $.ajax({
        url : "un_favorite/", // the endpoint
        type : "POST", // http method
        data : { 
            id : ide,
             }, // data sent with the post request
             
        // handle a successful response
        success : function(json) {
            $('#fav').removeClass('notifix');
        },

        // handle a non-successful response
        error : function(xhr,errmsg,err) {
            console.log(xhr.status + ": " + xhr.responseText);
           alert("deu errado");

        }
    });
}

//AJAX para alternar chave de notificação de participação

function requisicaoNotificacaoParticipacao(ide) {
    //console.log("função para saber se existe uma relaçao de seguidor");
    $.ajax({
        url : "getnotifyparticipation/", // the endpoint
        type : "POST", // http method
        data : { 
            id : ide,
             }, // data sent with the post request
             
        // handle a successful response
        success : function(json) {
            if (json == false){
                console.log('está falso');
                ativenotifyparticipate(ide);
            }
            else{
                console.log('está verdadeiro');
                inativenotifyparticipate(ide);
            }
        },

        // handle a non-successful response
        error : function(xhr,errmsg,err) {
            console.log(xhr.status + ": " + xhr.responseText);
           alert("deu errado");

        }
    });
}

function ativenotifyparticipate(ide){
        $.ajax({
        url : "ativenotifyparticipate/", // the endpoint
        type : "POST", // http method
        data : { 
            id : ide,
             }, // data sent with the post request
             
        // handle a successful response
        success : function(json) {
            $('#par').text("Desativar notificação de participação");
        },

        // handle a non-successful response
        error : function(xhr,errmsg,err) {
            console.log(xhr.status + ": " + xhr.responseText);
           alert("deu errado");

        }
    });
}

function inativenotifyparticipate(ide){
        $.ajax({
        url : "inativenotifyparticipate/", // the endpoint
        type : "POST", // http method
        data : { 
            id : ide,
             }, // data sent with the post request
             
        // handle a successful response
        success : function(json) {
            $('#par').text("Ativar notificação de participação");
        },

        // handle a non-successful response
        error : function(xhr,errmsg,err) {
            console.log(xhr.status + ": " + xhr.responseText);
           alert("deu errado");

        }
    });
}

//AJAX para deletar participação

function deleteparticipation(ide){
    console.log("Deletando participação");
    console.log(ide);
    $.ajax({
        url : "deleteparticipation/", // the endpoint
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
           alert("Não foi possível excluir participação");

        }
    });
}

//AJAX para mostrar e ocutar post do perfil

function requisicaoChavePostPerfil(ide) {
    //console.log("função para saber se existe uma relaçao de seguidor");
    $.ajax({
        url : "getkeypostprofile/", // the endpoint
        type : "POST", // http method
        data : { 
            id : ide,
             }, // data sent with the post request
             
        // handle a successful response
        success : function(json) {
            if (json == false){
                console.log('está falso');
                ativepostprofile(ide);
            }
            else{
                console.log('está verdadeiro');
                inativepostprofile(ide);
            }
        },

        // handle a non-successful response
        error : function(xhr,errmsg,err) {
            console.log(xhr.status + ": " + xhr.responseText);
           alert("deu errado");

        }
    });
}

function ativepostprofile(ide){
        $.ajax({
        url : "ativepostprofile/", // the endpoint
        type : "POST", // http method
        data : { 
            id : ide,
             }, // data sent with the post request
             
        // handle a successful response
        success : function(json) {
            $('#req').text("Ocultar post do perfil");
        },

        // handle a non-successful response
        error : function(xhr,errmsg,err) {
            console.log(xhr.status + ": " + xhr.responseText);
           alert("deu errado");

        }
    });
}

function inativepostprofile(ide){
        $.ajax({
        url : "inativepostprofile/", // the endpoint
        type : "POST", // http method
        data : { 
            id : ide,
             }, // data sent with the post request
             
        // handle a successful response
        success : function(json) {
            $('#req').text("Exibir post no perfil");
        },

        // handle a non-successful response
        error : function(xhr,errmsg,err) {
            console.log(xhr.status + ": " + xhr.responseText);
           alert("deu errado");

        }
    });
}

function alertDeletePost(ide){
    decisao = confirm("Deseja excluir este post?");
    if (decisao) {
        console.log("confirmou");
        $.ajax({
        url : "delete_post/", // the endpoint
        type : "POST", // http method
        data : { 
            id : ide,
             }, // data sent with the post request

        // handle a successful response
        success : function(json) {
            window.location.replace("/myposts/");
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


function requisicaoChaveAtivacaoPost(ide) {
    //console.log("função para saber se existe uma relaçao de seguidor");
    $.ajax({
        url : "getkeyactivepost/", // the endpoint
        type : "POST", // http method
        data : { 
            id : ide,
             }, // data sent with the post request
             
        // handle a successful response
        success : function(json) {
            if (json == false){
                console.log('está falso');
                ativenotifypost(ide)
            }
            else{
                console.log('está verdadeiro');
                inativenotifypost(ide)
            }
        },

        // handle a non-successful response
        error : function(xhr,errmsg,err) {
            console.log(xhr.status + ": " + xhr.responseText);
           alert("deu errado");

        }
    });
}

function ativenotifypost(ide){
        $.ajax({
        url : "activenotifypost/", // the endpoint
        type : "POST", // http method
        data : { 
            id : ide,
             }, // data sent with the post request
             
        // handle a successful response
        success : function(json) {
            $('#reqP').text("Desativar notificações deste post");
        },

        // handle a non-successful response
        error : function(xhr,errmsg,err) {
            console.log(xhr.status + ": " + xhr.responseText);
           alert("deu errado");

        }
    });
}

function inativenotifypost(ide){
        $.ajax({
        url : "inactivenotifypost/", // the endpoint
        type : "POST", // http method
        data : { 
            id : ide,
             }, // data sent with the post request
             
        // handle a successful response
        success : function(json) {
            $('#reqP').text("Ativar notificações deste post");
        },

        // handle a non-successful response
        error : function(xhr,errmsg,err) {
            console.log(xhr.status + ": " + xhr.responseText);
           alert("deu errado");

        }
    });
}

function report_coment_post(ide){
    console.log("Reportando comentário");
    console.log(ide);
    decisao = confirm("Deseja excluir esta comentário?");
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