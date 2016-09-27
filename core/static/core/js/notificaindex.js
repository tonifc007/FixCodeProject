//AJAX para notificar automaticamente

var indice = 0;
var indicePart = 0;
var indicePost = 0;

setTimeout("notificaIndex()", 1);
setInterval("notificaIndex()", 2000);
setTimeout("notificaIndexParticipation()", 1);
setInterval("notificaIndexParticipation()", 2000);

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
                $('#notifica').html("<a href='/myfixies/'><h4 style='background-color: blue; color: white;'>Você tem "+json+" fixies respondidos</h4></a>");
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
                $('#notificaParticipacao').html("<a href='participations/'><h4 style='background-color: green; color: white;'>"+json+" das suas participações tem novas respostas</h4></a>");
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
        url : "notificaIndexPosts/", // the endpoint
        type : "GET", // http method

        success : function(json) {
            console.log(json); // log the returned json to the console
            console.log("success"); // another sanity check
            if (json != indicePost && json != 0){
                console.log('muda');
                indicePost = json;
                $('#notificaPosts').html("<a href='myposts/'><h4 style='background-color: yellow; color: white;'>"+json+" de seus posts tem novos respostas</h4></a>");
            }
        },

        // handle a non-successful response
        error : function(xhr,errmsg,err) {
            console.log(xhr.status + ": " + xhr.responseText);
            console.log('offline');

        }
    });

}