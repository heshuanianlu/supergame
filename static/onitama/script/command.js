var choosedPiece=null,chooseDCard=null;


function chooseCard(){
    $(".card").last().children("img").click(function(){
        if(true){
            $(".card>img").css("border-color","black").css("box-shadow","0px 0px 6px black");
            $(this).css("border-color","gold").css("box-shadow","0px 0px 6px gold");
            chooseDCard=room.getCard($(this).attr("name"));
            action();
        }
    });
}

function choosePiece(){
    $("#cont>table>tbody td").click(function(){
        if(true){
            $("td").css("border-color","black");
            $(this).css("border-color","gold");
            choosedPiece=d($(this));
            action();
        }
    })
}

function action(){
    if(choosedPiece && choosedCard){
        var tr=choosedPiece[0],td=choosedPiece[1];
        choosedCard.showMove(tr, td);
    }
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
