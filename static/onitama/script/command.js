function show(websocket){
    $("#cont #xian>ul>li").click(function(){
        message='#!choose='+$(this).attr("id")+'!#';
        websocket.send(message);
    });
    $(".me>img").click(function(){
        if(true){
            $(".card>img").css("border-color","black").css("box-shadow","0px 0px 6px black");
            $(this).css("border-color","gold").css("box-shadow","0px 0px 6px gold");
        }
    });
}