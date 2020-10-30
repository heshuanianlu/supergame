var choosedPiece=null,choosedCard=null,turn=false;
var zhanShi="⊙";

function chooseCard(websocket){
    $(".card."+self).children("img:lt(2)").click(function(){
        if(turn){
            $(".card>img").css("border-color","black").css("box-shadow","0px 0px 6px black");
            $(this).css("border-color","gold").css("box-shadow","0px 0px 6px gold");
            choosedCard=room.getCard($(this).attr("name"));
            action(websocket);
        }
    });
}

function choosePiece(websocket){
    $(".piece."+self).click(function(){
        if(turn){
            $("td").css("border-color","black");
            $(this).css("border-color","gold");
            choosedPiece=d($(this));
            action(websocket);
        }
    })
}

function remove(){
    $("td").each(function(){
        if ($(this).text()==zhanShi){
            $(this).text("").css("color","transparent").removeClass(self).removeClass("target");
        }
    })
}

function action(websocket){
    if(choosedPiece && choosedCard){
        remove();
        choosedCard.showMove(choosedPiece);
        move(websocket);
    }
}

function choose(websocket){
    $("#cont #xian>ul>li").click(function(){
        var message='#!choose='+$(this).attr("id")+'!#';
        websocket.send(message);
    });
}

function agref(websocket, tiv_id){
    $("#alert>button").click(function(){
        var message='#!'+$(this).attr("id")+"="+tiv_id+'!#';
        websocket.send(message);
    })
}

function move(websocket){
    $(".target").click(function(){
        var position=d($(this))
        if ($(this).hasClass("target")&&choosedCard&&choosedPiece){
            var po=ref(choosedPiece),pn=ref(position);
            var message="#!action="
                        +room.id+"&"
                        +po[0]+""+po[1]+"&"
                        +pn[0]+""+pn[1]+"&"
                        +choosedCard.name+"!#";
            websocket.send(message);
            // if(turn){turn=false}else{turn=true}
            choosedPiece=null;choosedCard=null;
        }
    })
}

function ref(position){
    if(self=='red'){return [6-position[0],6-position[1]]}
    else if(self=='blue'){return position}
}

function yuan(){
    $(".card>img").css("border-color","black").css("box-shadow","0px 0px 6px black");
    $("tr>td").css("border-color","black").removeClass("target");
}
