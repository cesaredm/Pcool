$(document).ready(function(){
    validarSesionUser()
    validarSesionPropietario();
});

function validarSesionUser(params) {
    $('#sesion').hide();
    nombreUser = $('#nombreUser').text();
    if(nombreUser == "")
    {
        $('#sesion').hide();
    }else{
        $('#sesion').show();
    }
}

function validarSesionPropietario()
{
    $('#sesionP').hide();
    nombreUser = $('#nombreUserP').text();
    if(nombreUser == "")
    {
        $('#sesionP').hide();
    }else{
        $('#sesionP').show();
    }
}
