var websocket = null;
var lockReconnect = false;//避免重复连接
var wsUrl = "ws://"+location.host+"/onitama/client";

createWebSocket(wsUrl);

function createWebSocket(url) {
    try {
        if ('WebSocket' in window) {
            websocket = new WebSocket(url);
        } else if ('MozWebSocket' in window) {
            websocket = new MozWebSocket(url);
        } else {
            url = "http://"+location.host+"/onitama/client";
            websocket = new SockJS(url);
        }
        initEventHandle();
    }
    catch (ex) {
        reconnect(url);
        $('#tip>p').text(ex.message);
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
        console.log(result);
        console.log(123);
        for (key in result) {
            if (key == 'error') {
                var error=result['error'];
                $('#tip>p').text(error);
                setTimeout(function () { $('#tip>p').text('') }, 3000);  // 打印服务端返回的数据
            } else if (key == 'message') {
                var message=result['message'];
                var command=message['command'];
                console.log(command);
                if (command=='change'){
                    var users=message['user_id'];
                    var names=message['user_name'];
                    var cover=message['user_portrait'];
                    var htmlData="";
                    console.log(users,names,cover);
                    for (var i=0;i<users.length;i++){
                        data+=$("#cont>ul>li").html()
                            +"<li><a href='"+users[i]+"'><p>"+names[i]+"</p><img src='/media/portrait/"+cover[i]+"'></a></li>"
                    }
                    console.log(htmlData);
                    $("#cont>ul>li").eq(2).html(htmlData);
                }else if (command=='choose'){

                }else if (command=='agree'){

                }else if (command=='refuse'){

                }else if (command=='action'){

                }else if (command=='error'){
                    alert(result['error']);
                }
            }
        }
        console.log(231)
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

//心跳检测
// var heartCheck = {
//     timeout: 10000,//10秒发送一次心跳
//     timeoutObj: null,
//     serverTimeoutObj: null,
//     reset: function () {
//         clearTimeout(this.timeoutObj);
//         clearTimeout(this.serverTimeoutObj);
//         return this;
//     },
//     start: function () {
//         var self = this;
//         this.timeoutObj = setTimeout(function () {
//             //这里发送一个心跳，后端收到后，返回一个心跳消息，
//             //onmessage拿到返回的心跳就说明连接正常
//             websocket.send("#!check=my_id!#");
//             self.serverTimeoutObj = setTimeout(function () {
//                 //如果超过一定时间还没重置，说明后端主动断开了
//                 websocket.close();
//                 //如果onclose会执行reconnect，我们执行ws.close()就行了.如果直接执行reconnect 会触发onclose导致重连两次
//             }, self.timeout)
//         }, this.timeout)
//     }
// }

//每隔10秒去调用一次
setInterval(function(){
    switch (websocket.readyState){
        case 0: $('#tip').text('正在与服务器建立连接...'); break;
        case 1: $('#tip').text('连接成功建立，可以进行通信'); break;
        case 2: $('#tip').text('连接正在进行关闭握手，即将关闭'); reconnect(); break;
        case 3: $('#tip').text('连接已经关闭'); break;
        default: break;
    }
    setTimeout(function() { $('#tip').text('') }, 3000);
}, 10000);
