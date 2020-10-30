function p(position){
    return $("#cont>table>tbody")
    .children("tr").eq(5-position[1])
    .children("td").eq(position[0]-1)
}

function d(jqObj){
    for (var i=1;i<6;i++){
        for (var j=1;j<6;j++){
            if (p([i,j]).is(jqObj)){
                return [i,j]
            }
        }
    }
}

function o(position){
    return 1<=position[0]&&position[0]<=5 && 1<=position[1]&&position[1]<=5
}

function showCards(selector,cards){
    var htmlData="";
    for(var i=0;i<cards.length;i++){
        htmlData+="<img src='/static/onitama/card/"+cards[i].name+".jpg' name='"+cards[i].name+"'>";
    }
    $(selector).html(htmlData);
}
function showPieces(pieces){
    $("td").removeClass("red").removeClass("blue").removeClass("piece").text("").css("color","transparent");
    for (var i=0;i<pieces.length;i++){
        p(pieces[i].position).text(pieces[i].boss).css("color",pieces[i].color).addClass(pieces[i].color).addClass("piece");
    }
}

function Card(name, method, color){
    var card=new Object;
    card.name=name;
    card.method=method;
    card.color=color;
    card.getResult=function(position){
        var result=new Array();
        for(var i=0;i<card.method.length;i++){
            var targetP=[position[0]+card.method[i][0],position[1]+card.method[i][1]];
            if (o(targetP)){result.push(targetP);}
        }
        return result
    }
    card.showMove=function(position){
        var result=card.getResult(position);
        for(var i=0;i<result.length;i++){
            if(p(result[i]).text()){}else{p(result[i]).text(zhanShi).css("color",self).addClass(self).addClass("target");}
        }
    }
    card.check=function(pieceP, position){
        if(position in card.getResult(pieceP))return true;
    }
    return card;
}

function Piece(position, color, boss='徒'){
    var piece=new Object;
    piece.position=position;
    piece.color=color;
    piece.boss=boss;
    piece.move=function(position){
        p(position).html(piece.boss);
        p(piece.position).html("");
        piece.position=position;
    }
    return piece;
}

var LI = [
    Card('猿', [[-1, 1], [1, 1], [-1, -1], [1, -1]], 'blue'),
    Card('象', [[1, 0], [-1, 0], [1, 1], [-1, 1]], 'red'),
    Card('蟹', [[0, 1], [2, 0], [-2, 0]], 'blue'),
    Card('猪', [[0, 1], [1, 0], [-1, 0]], 'red'),
    Card('虎', [[0, 2], [0, -1]], 'blue'),
    Card('龙', [[-2, 1], [2, 1], [-1, -1], [1, -1]], 'red'),
    Card('鹅', [[1, 0], [-1, 1], [-1, 0], [1, -1]], 'blue'),
    Card('鸡', [[1, 0], [1, 1], [-1, 0], [-1, -1]], 'red'),
    Card('兔', [[2, 0], [1, 1], [-1, -1]], 'blue'),
    Card('蛙', [[-2, 0], [-1, 1], [1, -1]], 'red'),
    Card('鳗', [[1, 0], [-1, 1], [-1, -1]], 'blue'),
    Card('蛇', [[-1, 0], [1, 1], [1, -1]], 'red'),
    Card('牛', [[0, 1], [0, -1], [1, 0]], 'blue'),
    Card('马', [[0, 1], [0, -1], [-1, 0]], 'red'),
    Card('鹤', [[0, 1], [1, -1], [-1, -1]], 'blue'),
    Card('螳螂', [[0, -1], [1, 1], [-1, 1]], 'red'),
]

function Player(color, user_id){
    var player=new Object;
    player.color=color;
    player.user=user_id;
    return player
}

function Room(r,b,id){
    var room=new Object;
    room.id=id;
    room.pr=r[0];
    room.r_cards=new Array();
    room.r_pieces=new Array();
    room.pb=b[0];
    room.b_cards=new Array();
    room.b_pieces=new Array();
    room.cardList=new Array();
    room.pieceList=new Array();
    room.getCard=function (cardName){
        for(var i=0;i<LI.length;i++){
            if (cardName==LI[i].name){
                return LI[i]
            }
        }
        return null
    }
    room.getPiece=function (position){
        for(var i=0;i<room.pieceList.length;i++){
            if (room.pieceList[i].position.toString()==position.toString()){
                return room.pieceList[i]
            }
        }
        return null
    }
    room.runPiece=function (color, r){
        var pieceList=new Array();
        for (var i=1;i<6;i++){
            var piece=Piece([i,r],color)
            if(i==3){piece.boss='师';}
            pieceList.push(piece);
            room.pieceList.push(piece);
        }
        return pieceList
    }
    room.map=function(){
        $("#cont").html(
            '<figure class="card"></figure><table>'
            +'<tr><td></td><td></td><td></td><td></td><td></td></tr>'
            +'<tr><td></td><td></td><td></td><td></td><td></td></tr>'
            +'<tr><td></td><td></td><td></td><td></td><td></td></tr>'
            +'<tr><td></td><td></td><td></td><td></td><td></td></tr>'
            +'<tr><td></td><td></td><td></td><td></td><td></td></tr>'
            +'</table><figure class="card"></figure>'
        )
    }
    room.start=function(){
        for(i in r[1]){card=room.getCard(r[1][i]);room.cardList.push(card);room.r_cards.push(card);};
        for(i in b[1]){card=room.getCard(b[1][i]);room.cardList.push(card);room.b_cards.push(card);};
        if (self_id==r[0]){
            var red=1,blue=5;
            var me="red",an="blue";
            self='red';
            if(r[1].length==3)turn=true;
        }else if(self_id==b[0]){
            var blue=1,red=5;
            var me="blue",an="red";
            self='blue';
            if(b[1].length==3)turn=true;
        }
        room.r_pieces=room.runPiece('red',red);
        room.b_pieces=room.runPiece('blue',blue);
        $(".card").last().addClass(me);
        $(".card").first().addClass(an);
    }
    room.relCoon=function(cardName,pieceP,position,victory){
        if(turn){turn=false}else{turn=true}
        choosedPiece=null;choosedCard=null;
        var card=room.getCard(cardName);
        var piece=room.getPiece(pieceP);
        var other=room.getPiece(position);
        var oIndex=room.pieceList.indexOf(other);
        if (other){room.pieceList.splice(oIndex,1)}
        piece.move(position);
        if(room.b_cards.includes(card)){
            room.b_cards.splice(room.b_cards.indexOf(card),1);
            room.r_cards.push(card);
            if (other){room.r_pieces.splice(oIndex,1)}
        }else if(room.r_cards.includes(card)){
            room.r_cards.splice(room.r_cards.indexOf(card),1);
            room.b_cards.push(card);
            if (other){room.b_pieces.splice(oIndex,1)}
        }
        if(victory){$("#alert").html(
            "<h2>恭喜</h2><h2 style='color:"+self+"'>"+self+"方</h2><h2>获得胜利！</h2>"
        )}
    }
    room.showMap=function(){
        showCards(".red",room.r_cards);
        showCards(".blue",room.b_cards);
        showPieces(room.pieceList);
    }
    return room;
}



