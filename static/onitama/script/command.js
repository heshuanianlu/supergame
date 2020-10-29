function chooseCard(){
    $(".me>img").click(function(){
        if(true){
            $(".card>img").css("border-color","black").css("box-shadow","0px 0px 6px black");
            $(this).css("border-color","gold").css("box-shadow","0px 0px 6px gold");
        }
    });
}

function choosePiece(){
    $("#cont>table>tbody td").click(function(){
        if(true){
            $("td").css("color","black");
            $(this).css("color","gold");
        }
    })
}

function choose(websocket){
    $("#cont #xian>ul>li").click(function(){
        message='#!choose='+$(this).attr("id")+'!#';
        websocket.send(message);
    });
}

function agref(websocket, tiv_id){
    $("#alert>button").click(function(){
        message='#!'+$(this).attr("id")+"="+tiv_id+'!#';
        websocket.send(message);
    })
}