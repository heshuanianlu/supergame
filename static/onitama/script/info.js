// import '/static/tools/jquery.js'

function p(position){
    return $("#cont>table>tbody")
    .children("tr").eq(position[0])
    .children("td").eq(position[1])
}

function Card(name, method, color){
    var card=new Object;
    card.name=name;
    card.method=method;
    card.color=color;
    card.getResult=function(tr, td){
        var result=[];
        for(var i=0;i<this.method;i++){
            this.result.append((tr+this.method[i][0],td+this.method[i][1]));
        }
        return result
    }
    card.showMove=function(tr, td){
        var result=this.getResult(tr, td);
        for(var i=0;i<result;i++){
            p(result[i]).html("<p class='circle'>+</p>");
        }
    }
    card.check=function(tr, td, position){
        if(position in this.getResult(tr, td))return True;
    }
    card.show=function(imgEle){
        $(imgEle).setAttr("src","/static/onitama/card/"+this.name+".jpg").setAttr("name",this.name)
    }
    return card;
}

function Piece(position, color, boss=false){
    var piece=new Object;
    piece.position=position;
    piece.color=color;
    piece.boss=boss;
    piece.move=function(position){
        p(position).html(p(this.position).html());
        p(this.position).html("");
        this.position=position;
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

function Room(pr,pb){
    var room=new Object;
    room.pr=pr;
    room.pb=pb;
    room.start=function(cardNameList){
        function getCard(cardName){
            for(var i=0;i<LI.length;i++){
                if (cardName==LI[i].name){
                    return LI[i]
                }
            }
        }
        function runPiece(color, r){
            var pieceList=[]
            for (var i=0;i<5;i++){
                var piece=Piece((r,i),color)
                if(i==2){
                    piece.boss=true;
                }
                pieceList.append(piece)
            }
            return pieceList
        }
        var cardList=[];
        for(i in cardNameList){cardList.append(getCard(i))};
        pr.piece=runPiece('red', 1);
        pb.piece=runPiece('blue', 5)
    }
    return room;
}



