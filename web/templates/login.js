function getData(){
        document.getElementById('action').src = "/static/images/ruedita.gif";
        var username = $('#username').val();
        var password = $('#password').val();
        var message = JSON.stringify({
                "username": username,
                "password": password
            });

        $.ajax({
            url:'/authenticate',
            type:'POST',
            contentType: 'application/json',
            data : message,
            dataType:'json',
            success: function(response){
                //alert(JSON.stringify(response));

            },
            error: function(response){
                //alert(JSON.stringify(response));
                if (response['status']==401){
                document.getElementById('action').src = "/static/images/dislike.png";
                }else{
                document.getElementById('action').src = "/static/images/ok.png";
                var a=username;
                var c="http://127.0.0.1:8081/chat/"+a;
                window.location=c;
                }
            }
        });
    }