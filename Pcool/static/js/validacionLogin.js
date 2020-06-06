$(document).ready(function(){
    validarSesion()
});

function validarSesion(params) {
    $('#iconUser').hide();
    nombreUser = $('#nombreUser').text();
    console.log(nombreUser);
    
    if(nombreUser == "")
    {
        $('#iconUser').hide();
        $('#inicioSesion').show();
    }else{
        $('#iconUser').show();
        $('#inicioSesion').hide();
    }
}

$('#nombreUser').click(function(){
    opciones = document.getElementById('opcionSesion');
    if(opciones.style.display == "block"){
        opciones.style.display = 'none';
    }else{
        opciones.style.display = 'block'
    }
    console.log('hola');
});