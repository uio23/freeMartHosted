$(document).ready(function(){


    $('.messages').scrollTop($('.messages')[0].scrollHeight);


    var socket = io.connect("https://" + document.domain + ':' + location.port);

    socket.on('connect', function(){
        socket.send({'msg':"I am connected!", 'username': userUsername, 'auth': true});
    });

    socket.on('message', function(data){
        $(".messages").append($('<p class="message">').text(data.msg).prepend($('<span class="username"/>').text(`@${data.username} `)));
        $('.messages').scrollTop($('.messages')[0].scrollHeight);
    });


    $(".message-input-btn").on("click", function(){
        socket.send({'msg':$('.message-input-feild').val(), 'username': userUsername, 'auth': false});
        $('.message-input-feild').val('');
    });

});
