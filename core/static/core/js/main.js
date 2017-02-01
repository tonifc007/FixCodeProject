$(document).ready(function(){
    $('[data-toggle="tooltip"]').tooltip(); 

});


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
            $.notify({
                // options
                icon: 'glyphicon glyphicon-info-sign',
                title: 'Você agora segue este usuário',
            },{
                // settings
                element: 'body',
                position: null,
                type: "info",
                allow_dismiss: true,
                newest_on_top: false,
                showProgressbar: false,
                placement: {
                    from: "bottom",
                    align: "left"
                },
                offset: 20,
                spacing: 10,
                z_index: 1031,
                delay: 5000,
                timer: 1000,
                mouse_over: null,
                animate: {
                    enter: 'animated fadeInDown',
                    exit: 'animated fadeOutUp'
                },
                onShow: null,
                onShown: null,
                onClose: null,
                onClosed: null,
                icon_type: 'class',
                template: '<div data-notify="container" class="col-xs-11 col-sm-3 alert alert-{0}" role="alert">' +
                    '<button type="button" aria-hidden="true" class="close" data-notify="dismiss">×</button>' +
                    '<span data-notify="icon"></span> ' +
                    '<span data-notify="title">{1}</span> ' +
                    
                    '<div class="progress" data-notify="progressbar">' +
                        '<div class="progress-bar progress-bar-{0}" role="progressbar" aria-valuenow="0" aria-valuemin="0" aria-valuemax="100" style="width: 0%;"></div>' +
                    '</div>' +
                    '<a href="{3}" target="{4}" data-notify="url"></a>' +
                '</div>' 
            });
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
            $.notify({
                // options
                icon: 'glyphicon glyphicon-danger-sign',
                title: 'Você não segue mais este usuário',
            },{
                // settings
                element: 'body',
                position: null,
                type: "danger",
                allow_dismiss: true,
                newest_on_top: false,
                showProgressbar: false,
                placement: {
                    from: "bottom",
                    align: "left"
                },
                offset: 20,
                spacing: 10,
                z_index: 1031,
                delay: 5000,
                timer: 1000,
                mouse_over: null,
                animate: {
                    enter: 'animated fadeInDown',
                    exit: 'animated fadeOutUp'
                },
                onShow: null,
                onShown: null,
                onClose: null,
                onClosed: null,
                icon_type: 'class',
                template: '<div data-notify="container" class="col-xs-11 col-sm-3 alert alert-{0}" role="alert">' +
                    '<button type="button" aria-hidden="true" class="close" data-notify="dismiss">×</button>' +
                    '<span data-notify="icon"></span> ' +
                    '<span data-notify="title">{1}</span> ' +
                    
                    '<div class="progress" data-notify="progressbar">' +
                        '<div class="progress-bar progress-bar-{0}" role="progressbar" aria-valuenow="0" aria-valuemin="0" aria-valuemax="100" style="width: 0%;"></div>' +
                    '</div>' +
                    '<a href="{3}" target="{4}" data-notify="url"></a>' +
                '</div>' 
            });
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

		console.log("confirmou");
		$.ajax({
        url : "delete_confirm/", // the endpoint
        type : "POST", // http method
        data : { 
        	id : ide,
        	 }, // data sent with the post request

        // handle a successful response
        success : function(json) {
           	window.location.replace("/fix/myfixies/");
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
            $.notify({
                // options
                icon: 'glyphicon glyphicon-info-sign',
                title: 'Notificações ativadas para este fix',
            },{
                // settings
                element: 'body',
                position: null,
                type: "info",
                allow_dismiss: true,
                newest_on_top: false,
                showProgressbar: false,
                placement: {
                    from: "bottom",
                    align: "left"
                },
                offset: 20,
                spacing: 10,
                z_index: 1031,
                delay: 5000,
                timer: 1000,
                mouse_over: null,
                animate: {
                    enter: 'animated fadeInDown',
                    exit: 'animated fadeOutUp'
                },
                onShow: null,
                onShown: null,
                onClose: null,
                onClosed: null,
                icon_type: 'class',
                template: '<div data-notify="container" class="col-xs-11 col-sm-3 alert alert-{0}" role="alert">' +
                    '<button type="button" aria-hidden="true" class="close" data-notify="dismiss">×</button>' +
                    '<span data-notify="icon"></span> ' +
                    '<span data-notify="title">{1}</span> ' +
                    
                    '<div class="progress" data-notify="progressbar">' +
                        '<div class="progress-bar progress-bar-{0}" role="progressbar" aria-valuenow="0" aria-valuemin="0" aria-valuemax="100" style="width: 0%;"></div>' +
                    '</div>' +
                    '<a href="{3}" target="{4}" data-notify="url"></a>' +
                '</div>' 
            });

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
            $.notify({
                // options
                icon: 'glyphicon glyphicon-danger-sign',
                title: 'Notificações desativadas para este fix',
            },{
                // settings
                element: 'body',
                position: null,
                type: "danger",
                allow_dismiss: true,
                newest_on_top: false,
                showProgressbar: false,
                placement: {
                    from: "bottom",
                    align: "left"
                },
                offset: 20,
                spacing: 10,
                z_index: 1031,
                delay: 5000,
                timer: 1000,
                mouse_over: null,
                animate: {
                    enter: 'animated fadeInDown',
                    exit: 'animated fadeOutUp'
                },
                onShow: null,
                onShown: null,
                onClose: null,
                onClosed: null,
                icon_type: 'class',
                template: '<div data-notify="container" class="col-xs-11 col-sm-3 alert alert-{0}" role="alert">' +
                    '<button type="button" aria-hidden="true" class="close" data-notify="dismiss">×</button>' +
                    '<span data-notify="icon"></span> ' +
                    '<span data-notify="title">{1}</span> ' +
                    
                    '<div class="progress" data-notify="progressbar">' +
                        '<div class="progress-bar progress-bar-{0}" role="progressbar" aria-valuenow="0" aria-valuemin="0" aria-valuemax="100" style="width: 0%;"></div>' +
                    '</div>' +
                    '<a href="{3}" target="{4}" data-notify="url"></a>' +
                '</div>' 
            });
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
            $.notify({
                // options
                icon: 'glyphicon glyphicon-info-sign',
                title: 'Fix favoritado!',
            },{
                // settings
                element: 'body',
                position: null,
                type: "info",
                allow_dismiss: true,
                newest_on_top: false,
                showProgressbar: false,
                placement: {
                    from: "bottom",
                    align: "left"
                },
                offset: 20,
                spacing: 10,
                z_index: 1031,
                delay: 5000,
                timer: 1000,
                mouse_over: null,
                animate: {
                    enter: 'animated fadeInDown',
                    exit: 'animated fadeOutUp'
                },
                onShow: null,
                onShown: null,
                onClose: null,
                onClosed: null,
                icon_type: 'class',
                template: '<div data-notify="container" class="col-xs-11 col-sm-3 alert alert-{0}" role="alert">' +
                    '<button type="button" aria-hidden="true" class="close" data-notify="dismiss">×</button>' +
                    '<span data-notify="icon"></span> ' +
                    '<span data-notify="title">{1}</span> ' +
                    
                    '<div class="progress" data-notify="progressbar">' +
                        '<div class="progress-bar progress-bar-{0}" role="progressbar" aria-valuenow="0" aria-valuemin="0" aria-valuemax="100" style="width: 0%;"></div>' +
                    '</div>' +
                    '<a href="{3}" target="{4}" data-notify="url"></a>' +
                '</div>' 
            });
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
            $.notify({
                // options
                icon: 'glyphicon glyphicon-danger-sign',
                title: 'Fix desfavoritado',
            },{
                // settings
                element: 'body',
                position: null,
                type: "danger",
                allow_dismiss: true,
                newest_on_top: false,
                showProgressbar: false,
                placement: {
                    from: "bottom",
                    align: "left"
                },
                offset: 20,
                spacing: 10,
                z_index: 1031,
                delay: 5000,
                timer: 1000,
                mouse_over: null,
                animate: {
                    enter: 'animated fadeInDown',
                    exit: 'animated fadeOutUp'
                },
                onShow: null,
                onShown: null,
                onClose: null,
                onClosed: null,
                icon_type: 'class',
                template: '<div data-notify="container" class="col-xs-11 col-sm-3 alert alert-{0}" role="alert">' +
                    '<button type="button" aria-hidden="true" class="close" data-notify="dismiss">×</button>' +
                    '<span data-notify="icon"></span> ' +
                    '<span data-notify="title">{1}</span> ' +
                    
                    '<div class="progress" data-notify="progressbar">' +
                        '<div class="progress-bar progress-bar-{0}" role="progressbar" aria-valuenow="0" aria-valuemin="0" aria-valuemax="100" style="width: 0%;"></div>' +
                    '</div>' +
                    '<a href="{3}" target="{4}" data-notify="url"></a>' +
                '</div>' 
            });
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
            $('#par').addClass('notifix');
            $.notify({
                // options
                icon: 'glyphicon glyphicon-info-sign',
                title: 'Você está participando desde fix',
            },{
                // settings
                element: 'body',
                position: null,
                type: "info",
                allow_dismiss: true,
                newest_on_top: false,
                showProgressbar: false,
                placement: {
                    from: "bottom",
                    align: "left"
                },
                offset: 20,
                spacing: 10,
                z_index: 1031,
                delay: 5000,
                timer: 1000,
                mouse_over: null,
                animate: {
                    enter: 'animated fadeInDown',
                    exit: 'animated fadeOutUp'
                },
                onShow: null,
                onShown: null,
                onClose: null,
                onClosed: null,
                icon_type: 'class',
                template: '<div data-notify="container" class="col-xs-11 col-sm-3 alert alert-{0}" role="alert">' +
                    '<button type="button" aria-hidden="true" class="close" data-notify="dismiss">×</button>' +
                    '<span data-notify="icon"></span> ' +
                    '<span data-notify="title">{1}</span> ' +
                    
                    '<div class="progress" data-notify="progressbar">' +
                        '<div class="progress-bar progress-bar-{0}" role="progressbar" aria-valuenow="0" aria-valuemin="0" aria-valuemax="100" style="width: 0%;"></div>' +
                    '</div>' +
                    '<a href="{3}" target="{4}" data-notify="url"></a>' +
                '</div>' 
            });
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
            $('#par').removeClass('notifix');
            $.notify({
                // options
                icon: 'glyphicon glyphicon-danger-sign',
                title: 'Você retirou participação deste fix',
            },{
                // settings
                element: 'body',
                position: null,
                type: "danger",
                allow_dismiss: true,
                newest_on_top: false,
                showProgressbar: false,
                placement: {
                    from: "bottom",
                    align: "left"
                },
                offset: 20,
                spacing: 10,
                z_index: 1031,
                delay: 5000,
                timer: 1000,
                mouse_over: null,
                animate: {
                    enter: 'animated fadeInDown',
                    exit: 'animated fadeOutUp'
                },
                onShow: null,
                onShown: null,
                onClose: null,
                onClosed: null,
                icon_type: 'class',
                template: '<div data-notify="container" class="col-xs-11 col-sm-3 alert alert-{0}" role="alert">' +
                    '<button type="button" aria-hidden="true" class="close" data-notify="dismiss">×</button>' +
                    '<span data-notify="icon"></span> ' +
                    '<span data-notify="title">{1}</span> ' +
                    
                    '<div class="progress" data-notify="progressbar">' +
                        '<div class="progress-bar progress-bar-{0}" role="progressbar" aria-valuenow="0" aria-valuemin="0" aria-valuemax="100" style="width: 0%;"></div>' +
                    '</div>' +
                    '<a href="{3}" target="{4}" data-notify="url"></a>' +
                '</div>' 
            });
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
            $('#req').addClass('notifix');
            $('#req > span').removeClass('glyphicon-unchecked').addClass('glyphicon-check');
            $.notify({
                // options
                icon: 'glyphicon glyphicon-info-sign',
                title: 'Este post agora aparece no seu perfil',
            },{
                // settings
                element: 'body',
                position: null,
                type: "info",
                allow_dismiss: true,
                newest_on_top: false,
                showProgressbar: false,
                placement: {
                    from: "bottom",
                    align: "left"
                },
                offset: 20,
                spacing: 10,
                z_index: 1031,
                delay: 5000,
                timer: 1000,
                mouse_over: null,
                animate: {
                    enter: 'animated fadeInDown',
                    exit: 'animated fadeOutUp'
                },
                onShow: null,
                onShown: null,
                onClose: null,
                onClosed: null,
                icon_type: 'class',
                template: '<div data-notify="container" class="col-xs-11 col-sm-3 alert alert-{0}" role="alert">' +
                    '<button type="button" aria-hidden="true" class="close" data-notify="dismiss">×</button>' +
                    '<span data-notify="icon"></span> ' +
                    '<span data-notify="title">{1}</span> ' +
                    
                    '<div class="progress" data-notify="progressbar">' +
                        '<div class="progress-bar progress-bar-{0}" role="progressbar" aria-valuenow="0" aria-valuemin="0" aria-valuemax="100" style="width: 0%;"></div>' +
                    '</div>' +
                    '<a href="{3}" target="{4}" data-notify="url"></a>' +
                '</div>' 
            });
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
            $('#req').removeClass('notifix');
            $('#req > span').removeClass('glyphicon-check').addClass('glyphicon-unchecked');
            $.notify({
                // options
                icon: 'glyphicon glyphicon-danger-sign',
                title: 'Este post não aparecerá no seu perfil',
            },{
                // settings
                element: 'body',
                position: null,
                type: "danger",
                allow_dismiss: true,
                newest_on_top: false,
                showProgressbar: false,
                placement: {
                    from: "bottom",
                    align: "left"
                },
                offset: 20,
                spacing: 10,
                z_index: 1031,
                delay: 5000,
                timer: 1000,
                mouse_over: null,
                animate: {
                    enter: 'animated fadeInDown',
                    exit: 'animated fadeOutUp'
                },
                onShow: null,
                onShown: null,
                onClose: null,
                onClosed: null,
                icon_type: 'class',
                template: '<div data-notify="container" class="col-xs-11 col-sm-3 alert alert-{0}" role="alert">' +
                    '<button type="button" aria-hidden="true" class="close" data-notify="dismiss">×</button>' +
                    '<span data-notify="icon"></span> ' +
                    '<span data-notify="title">{1}</span> ' +
                    
                    '<div class="progress" data-notify="progressbar">' +
                        '<div class="progress-bar progress-bar-{0}" role="progressbar" aria-valuenow="0" aria-valuemin="0" aria-valuemax="100" style="width: 0%;"></div>' +
                    '</div>' +
                    '<a href="{3}" target="{4}" data-notify="url"></a>' +
                '</div>' 
            });
        },

        // handle a non-successful response
        error : function(xhr,errmsg,err) {
            console.log(xhr.status + ": " + xhr.responseText);
           alert("deu errado");

        }
    });
}

function alertDeletePost(ide){

    console.log("confirmou");
        $.ajax({
        url : "delete_post/", // the endpoint
        type : "POST", // http method
        data : { 
            id : ide,
             }, // data sent with the post request

        // handle a successful response
        success : function(json) {
            window.location.replace("/post/myposts/");
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
                ativenotifypost(ide);
            }
            else{
                console.log('está verdadeiro');
                inativenotifypost(ide);
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
            $('#reqP').addClass('notifix');
            $.notify({
                // options
                icon: 'Notificações ativadas para este post',
                title: 'Fix desfavoritado',
            },{
                // settings
                element: 'body',
                position: null,
                type: "info",
                allow_dismiss: true,
                newest_on_top: false,
                showProgressbar: false,
                placement: {
                    from: "bottom",
                    align: "left"
                },
                offset: 20,
                spacing: 10,
                z_index: 1031,
                delay: 5000,
                timer: 1000,
                mouse_over: null,
                animate: {
                    enter: 'animated fadeInDown',
                    exit: 'animated fadeOutUp'
                },
                onShow: null,
                onShown: null,
                onClose: null,
                onClosed: null,
                icon_type: 'class',
                template: '<div data-notify="container" class="col-xs-11 col-sm-3 alert alert-{0}" role="alert">' +
                    '<button type="button" aria-hidden="true" class="close" data-notify="dismiss">×</button>' +
                    '<span data-notify="icon"></span> ' +
                    '<span data-notify="title">{1}</span> ' +
                    
                    '<div class="progress" data-notify="progressbar">' +
                        '<div class="progress-bar progress-bar-{0}" role="progressbar" aria-valuenow="0" aria-valuemin="0" aria-valuemax="100" style="width: 0%;"></div>' +
                    '</div>' +
                    '<a href="{3}" target="{4}" data-notify="url"></a>' +
                '</div>' 
            });
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
            $('#reqP').removeClass('notifix');
            $.notify({
                // options
                icon: 'glyphicon glyphicon-danger-sign',
                title: 'Notificações desativadas para este post',
            },{
                // settings
                element: 'body',
                position: null,
                type: "danger",
                allow_dismiss: true,
                newest_on_top: false,
                showProgressbar: false,
                placement: {
                    from: "bottom",
                    align: "left"
                },
                offset: 20,
                spacing: 10,
                z_index: 1031,
                delay: 5000,
                timer: 1000,
                mouse_over: null,
                animate: {
                    enter: 'animated fadeInDown',
                    exit: 'animated fadeOutUp'
                },
                onShow: null,
                onShown: null,
                onClose: null,
                onClosed: null,
                icon_type: 'class',
                template: '<div data-notify="container" class="col-xs-11 col-sm-3 alert alert-{0}" role="alert">' +
                    '<button type="button" aria-hidden="true" class="close" data-notify="dismiss">×</button>' +
                    '<span data-notify="icon"></span> ' +
                    '<span data-notify="title">{1}</span> ' +
                    
                    '<div class="progress" data-notify="progressbar">' +
                        '<div class="progress-bar progress-bar-{0}" role="progressbar" aria-valuenow="0" aria-valuemin="0" aria-valuemax="100" style="width: 0%;"></div>' +
                    '</div>' +
                    '<a href="{3}" target="{4}" data-notify="url"></a>' +
                '</div>' 
            });
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

//bloquar usupario

function bloquear(ide) {
    $.ajax({
        url : "/bloquear/", // the endpoint
        type : "POST", // http method
        data : { 
            id : ide,
             }, // data sent with the post request
             
        // handle a successful response
        success : function(json) {
            if (json == true) {
                parent.window.document.location.href = '';
            }else{
                alert("Não foi possível concluir a operação");
            }
        },

        // handle a non-successful response
        error : function(xhr,errmsg,err) {
            console.log(xhr.status + ": " + xhr.responseText);
           alert("deu errado");

        }
    });
}

function desbloquear(ide) {
    $.ajax({
        url : "/desbloquear/", // the endpoint
        type : "POST", // http method
        data : { 
            id : ide,
             }, // data sent with the post request
             
        // handle a successful response
        success : function(json) {
            if (json == true) {
                parent.window.document.location.href = '';
            }else{
                alert("Não foi possível concluir a operação");
            }
        },

        // handle a non-successful response
        error : function(xhr,errmsg,err) {
            console.log(xhr.status + ": " + xhr.responseText);
           alert("deu errado");

        }
    });
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