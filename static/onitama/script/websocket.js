var websocket = null;
var lockReconnect = false;//避免重复连接
var wsUrl = "ws://"+location.host+"/onitama/client";

createWebSocket(wsUrl);
//check_state();

function createWebSocket(url) {
    try {
        if ('WebSocket' in window) {
            websocket = new WebSocket(url);
        } else if ('MozWebSocket' in window) {
            ws = new MozWebSocket(url);
        } else {
            url = "http://"+location.host+"/onitama/client";
            websocket = new SockJS(url);
        }
        initEventHandle();
    }
    catch (ex) {
        reconnect(url);
        $('#tip').text(ex.message);
    }
}
function initEventHandle() {
    websocket.onclose = function (evnt) {
        reconnect(wsUrl);
    };
    websocket.onerror = function (evnt) {
        reconnect(wsUrl);
    };
    websocket.onopen = function (evnt) {
        websocket.send('#!connect=my_id!#');
    };
    websocket.onmessage = function (evnt) {
        var result = JSON.parse(evnt.data);
        for (key in result) {
            if (key == 'code') {
                if (result['code'] == '0') {
                    $('#tip>p').text('不登录还想玩游戏？');
                } else if (result['code'] == '110') {
                    $('#tip>p').text('在？话这么多？')
                } else if (result['code'] == '001') {
                    $('#tip>p').text('对方不在线哦！')
                } else if (result['code'] == '010') {
                    $('#tip>p').text('和自己说话很棒？')
                }
                setTimeout(function () { $('#tip').text('') }, 3000);  // 打印服务端返回的数据
            } else if (key == 'message') {
                if (result['message']=='hall'){
                    var users=result['user_id'];
                    var names=result['user_name'];
                    var cover=result['user_portrait'];
                    var htmlData="";
                    for (var i=0;i<users.length;i++){
                        data+=$("#cont>ul>li").html()+"<li><a href='"+users[i]+"'>"+names[i]+"</a></li>"
                    }
                    $("#cont>ul>li").eq(2).html(htmlData);
                }
            }
        }
    }
    //收到消息推送
}

//监听窗口关闭事件，当窗口关闭时，主动去关闭websocket连接，防止连接还没断开就关闭窗口，server端会抛异常。  
window.onbeforeunload = function () {
    closeWebSocket();
}

//关闭WebSocket连接  
function closeWebSocket() {
    $('#tip').text("服务器已经关闭");
    websocket.close();
    reconnect(wsUrl);
}

//重新连接
function reconnect() {
    if (lockReconnect) return;
    lockReconnect = true;
    //没连接上会一直重连，设置延迟避免请求过多
    setTimeout(function () {
        createWebSocket(wsUrl);
        lockReconnect = false;
    }, 5000);//每5秒重连一次
}

//每隔10秒去调用一次
setInterval(function(){
    switch (websocket.readyState){
        case 0: $('#tip').text('正在与服务器建立连接...'); break;
        case 1: $('#tip').text('连接成功建立，可以进行通信'); break;
        case 2: $('#tip').text('连接正在进行关闭握手，即将关闭'); reconnect(); break;
        case 3: $('#tip').text('连接已经关闭'); break;
        default: break;
    }
    // setTimeout(function() { $('#tip').text('') }, 3000);
}, 10000);
