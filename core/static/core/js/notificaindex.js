//AJAX para notificar automaticamente

var indice = 0;
var indicePart = 0;
var indicePost = 0;

setTimeout("notificaIndex()", 1);
setInterval("notificaIndex()", 2000);
setTimeout("notificaIndexParticipation()", 1);
setInterval("notificaIndexParticipation()", 2000);
setTimeout("notificaIndexPosts()", 1);
setInterval("notificaIndexPosts()", 2000);

//Torna todas as imgs dos posts responsivas
$('.fcc > p > img').addClass('img-responsive').addClass('thumbnail');

function notificaIndex(){

    $.ajax({
        url : "notificaIndex/", // the endpoint
        type : "GET", // http method

        success : function(json) {
            console.log(json); // log the returned json to the console
            console.log("success"); // another sanity check
            if (json != indice && json != 0){
                console.log('muda');
                indice = json;
                $('#notifica').html("<a class='btn btn-primary btn-block' style='margin-bottom: 6px;' href='/fix/myfixies/notify/'>Você tem "+json+" fixie(s) com novas respostas.</a>");

            }
        },

        // handle a non-successful response
        error : function(xhr,errmsg,err) {
            console.log(xhr.status + ": " + xhr.responseText);
            console.log('offline');

        }
    });

}

function notificaIndexParticipation(){
    console.log("Notifica participação");

    $.ajax({
        url : "notificaIndexParticipation/", // the endpoint
        type : "GET", // http method

        success : function(json) {
            console.log(json); // log the returned json to the console
            console.log("success"); // another sanity check
            if (json != indicePart && json != 0){
                console.log('muda');
                indicePart = json;
                $('#notificaParticipacao').html("<a class='btn btn-warning btn-block' style='margin-bottom: 6px;' href='/fix/participations/notify/'>Você tem "+json+" participação(es) com novas respostas.</a>");
            }
        },

        // handle a non-successful response
        error : function(xhr,errmsg,err) {
            console.log(xhr.status + ": " + xhr.responseText);
            console.log('offline');

        }
    });

}

function notificaIndexPosts(){
    console.log("Notifica posts");

    $.ajax({
        url : "notificaIndexPosts/", // the endpoint
        type : "GET", // http method

        success : function(json) {
            console.log(json); // log the returned json to the console
            console.log("success"); // another sanity check
            if (json != indicePost && json != 0){
                console.log('muda');
                indicePost = json;
                $('#notificaPosts').html("<a class='btn btn-success btn-block' style='margin-bottom: 6px;' href='myposts/'>Você tem "+json+" post(s) com novos comentários.</a>");
            }
        },

        // handle a non-successful response
        error : function(xhr,errmsg,err) {
            console.log(xhr.status + ": " + xhr.responseText);
            console.log('offline');

        }
    });

}