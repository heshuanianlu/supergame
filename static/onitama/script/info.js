function p(position){
    return $("#cont>table>tbody")
    .children("tr").eq(5-position[0])
    .children("td").eq(4-position[1])
}

function d(jqObj){
    for (var i=0;i<5;i++){
        for (var j=0;j<5;j++){
            if (p([i,j])===jqObj){
                return [i,j]
            }
        }
    }
}

function showCards(selector,cards){
    var htmlData="";
    for(var i=0;i<cards.length;i++){
        htmlData+="<img src='/static/onitama/card/"+cards[i].name+".jpg' name='"+cards[i].name+"'>";
    }
    $(selector).html(htmlData);
}
function showPieces(pieces){
    for (var i=0;i<pieces.length;i++){
        console.log(pieces[i]);
        p(pieces[i].position).text(pieces[i].boss).css("color",pieces[i].color).addClass(pieces[i].color);
    }
}

function Card(name, method, color){
    var card=new Object;
    card.name=name;
    card.method=method;
    card.color=color;
    card.getResult=function(tr, td){
        var result=new Array();
        for(var i=0;i<card.method;i++){
            card.result.push((tr+card.method[i][0],td+card.method[i][1]));
        }
        return result
    }
    card.showMove=function(tr, td){
        var result=this.getResult(tr, td);
        for(var i=0;i<result;i++){
            p(result[i]).text("○");
        }
    }
    card.check=function(tr, td, position){
        if(position in card.getResult(tr, td))return True;
    }
    card.show=function(imgEle){
        $(imgEle).setAttr("src","/static/onitama/card/"+card.name+".jpg").setAttr("name",card.name)
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
    Card('猿', [(-1, 1), (1, 1), (-1, -1), (1, -1)], 'blue'),
    Card('象', [(1, 0), (-1, 0), (1, 1), (-1, 1)], 'red'),
    Card('蟹', [(0, 1), (2, 0), (-2, 0)], 'blue'),
    Card('猪', [(0, 1), (1, 0), (-1, 0)], 'red'),
    Card('虎', [(0, 2), (0, -1)], 'blue'),
    Card('龙', [(-2, 1), (2, 1), (-1, -1), (1, -1)], 'red'),
    Card('鹅', [(1, 0), (-1, 1), (-1, 0), (1, -1)], 'blue'),
    Card('鸡', [(1, 0), (1, 1), (-1, 0), (-1, -1)], 'red'),
    Card('兔', [(2, 0), (1, 1), (-1, -1)], 'blue'),
    Card('蛙', [(-2, 0), (-1, 1), (1, -1)], 'red'),
    Card('鳗', [(1, 0), (-1, 1), (-1, -1)], 'blue'),
    Card('蛇', [(-1, 0), (1, 1), (1, -1)], 'red'),
    Card('牛', [(0, 1), (0, -1), (1, 0)], 'blue'),
    Card('马', [(0, 1), (0, -1), (-1, 0)], 'red'),
    Card('鹤', [(0, 1), (1, -1), (-1, -1)], 'blue'),
    Card('螳螂', [(0, -1), (1, 1), (-1, 1)], 'red'),
]

function Player(color, user_id){
    var player=new Object;
    player.color=color;
    player.user=user_id;
    return player
}

function Room(r,b){
    var room=new Object;
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
    }
    room.getPiece=function (position){
        for(var i=0;i<room.pieceList.length;i++){
            if (room.pieceList[i].position=position){
                return room.pieceList[i]
            }
        }
    }
    room.runPiece=function (color, r){
        var pieceList=new Array();
        for (var i=0;i<5;i++){
            var piece=Piece([r,i],color)
            if(i==2){piece.boss='师';}
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
        }else if(self_id==b[0]){
            var blue=1,red=5;
            var me="blue",an="red";
        }
        room.r_pieces=room.runPiece('red',red);
        room.b_pieces=room.runPiece('blue',blue);
        $(".card").last().addClass(me);
        $(".card").first().addClass(an);
    }
    room.ref=function(card_name,pieceP,position,victory){
        var card=room.getCard(card_name);
        var piece=room.getPiece(pieceP);
        var other=room.getPiece(position);
        if (other){room.pieceList.pop(room.pieceList.indexOf(other))}
        piece.move(position);
        if(room.b_cards.includes(card)){
            room.b_cards.pop(room.b_cards.indexOf(card));
            room.r_cards.push(card);
        }else if(room.b_cards.includes(card)){
            room.r_cards.pop(room.r_cards.indexOf(card));
            room.b_cards.push(card);
        }
    }
    room.showMap=function(){
        showCards(".red",room.r_cards);
        showCards(".blue",room.b_cards);
        showPieces(room.pieceList);
    }
    return room;
}

function Action(){
    if(choosedPiece && choosedCard){
        var tr=choosedPiece.position[0],td=choosedPiece.position[1];
        choosedCard.showMove(tr, td);
    }
}


