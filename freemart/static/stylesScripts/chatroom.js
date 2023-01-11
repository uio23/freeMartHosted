$(document).ready(function(){


    $('#messages').scrollTop($('#messages')[0].scrollHeight);


    var socket = io.connect("https://" + document.domain + ':' + location.port);

    socket.on('connect', function(){
        socket.send({'msg':"I am connected!", 'username': userUsername, 'auth': true});
    });

    socket.on('message', function(data){
        $("#messages").append($('<p>').text(data.msg).prepend($('<span/>').text(`@${data.username} `)));
        $('#messages').scrollTop($('#messages')[0].scrollHeight);
    });


    $("#sendBtn").on("click", function(){
        socket.send({'msg':$(messageContent).val(), 'username': userUsername, 'auth': false});
        $('#messageContent').val('');
    })


});
