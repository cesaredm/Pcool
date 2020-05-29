class LoginPropietarios
{
    
    validacion(nombre, password)
    {
        $.ajax(
            {
                url:'/validarSesion',
                type:'POST',
                dataType:'json',
                data:{
                    nombre:nombre,
                    password:password
                },
                succes:function (response) {
                    
                }
            }
        );
    }
}
$('#Login').submit(function (e)
{
    e.preventDefault();
    var nombre = $('#nombrePropietario').val();
    var password = $('#passwordPropietario').val();
    var validar = new LoginPropietarios();
    validar.validacion(nombre,password);
});