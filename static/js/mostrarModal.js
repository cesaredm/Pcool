//$(document).ready(likes);
function iniciar(nombre) {

    $.get('/mostrarModal', {nombreP:nombre}, function(datos){
        var p = $.parseJSON(datos);
        $('.modal-title').text(p.nombre);
        
    });
}
//funcion para mostrar lo detalles del producto en modal
$('.card-body').click(function (e) {
    //obtengo valor de id de cada card
    var id = e.target.getAttribute('id');
    //envio en formato json el id con metodo get de ajax
    $.get('/mostrarModal', {idP:id}, function(datos){
        //convertir lo que recibo de python a formato json
        var p = $.parseJSON(datos);
        //agrego la informacion a la card
        //nombre Producto o tienda
        $('.modal-title').text(p.nombre);
        //img para slide de modal
        $('.primerItem').html('<img src="'+p.imagen+'" alt="'+p.nombre+'" class="img-fluid">');
        //descripcion de producto en el modal
        $('#descripcion').text(p.descripcion);
        //nombre de producto en el modal
        $('#nombreProducto').text(p.nombre);
        //precio de producto en el modal
        $('#precio').text(p.precio+" C$");

    });
});

    $('.icon-manitaArriba').click(function(e) {
        var id = parseInt(e.target.getAttribute('id'));
        var valor = e.target.getAttribute('name');
        var likes = parseInt(valor);
        console.log(id, likes);
        
        guardarLike(id,1);
    });

    function guardarLike(id, likes) {
        $.ajax({
            url:'/obtenerLike?idP='+id+'&like='+likes,
            data:{/*
                idProduct:id,
                like:likes*/
                },
            type:'POST',
            dataType:'json',
            success: function (response) {
                console.log(response.status, response.id, response.likes);
                
            }
        });
    }