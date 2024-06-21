var Toast = Swal.mixin({
    toast: true,
    position: "top-end",
    showConfirmButton: false,
    timer: 3000,
  });

$('#loginBtn').click(function(){
    let username = $('#username').val();
    let password = $('#password').val();

    $.ajax({
        url: 'token',
        type: 'POST',
        headers: {
            "Content-Type": "application/json"
          },
        data: JSON.stringify({'username': username, 'password': password}),
        success: function(res){
            window.location.href='/';
        },
        error: function(xhr, status, error){
            Toast.fire({
                icon: "error",
                title: "Đăng nhập thất bại",
              });
        }
    });
});