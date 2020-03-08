$(document).ready(function () {
    mostrarTienda();
    mostrarProducto();
});
function mostrarTienda() {
    $.ajax({
        url: '/mostrarTiendas',
        data: {},
        type: 'POST',
        dataType: 'json',
        success: function (response) {
            var i;
            for (i = 0; i < response.length; i++) {
                $('#listaTienda').append('<option value="' + response[i].id + '">' + response[i].nombre + '</option>');
            }

        }
    });
}
function mostrarProducto() {
    $.ajax({
        url: '/mostrarProducto',
        data: {},
        type: 'POST',
        dataType: 'json',
        success: function (response) {
            var i;
            for (i = 0; i < response.length; i++) {
                $('#listaProducto').append('<option value="' + response[i].id + '">' + response[i].nombre + '</option>');
            }

        }
    });
}
$('#formTienda').submit(function (e) {
    e.preventDefault();
    $.ajax({
        url: '/guardarTienda',
        data: $('#formTienda').serialize(),
        type: 'POST',
        dataType: 'json',
        success: function (response) {
            alert(response.estado);
        }
    });
});

$('#formProducto').submit(function (e) {
    e.preventDefault();
    $.ajax({
        url: '/guardar_producto',
        data: $('#formProducto').serialize(),
        type: 'POST',
        dataType: 'json',
        success: function (response) {
            $('#formProducto').reset();
            var i;
            for (i = 0; i < response.length; i++) {
                $('#galeria').append(`
                <div class="col-6 col-sm-6 col-md-4 col-lg-3 mt-2 elemento">
                <div class="card shadow">
                <div class="card-header p-1">
                    <div class="text-center lead small">
                        <p>`+ response[i].nombre + `</p>
                    </div>
                </div>
                    <div class="card-body" data-toggle="modal" data-target="#exampleModalLong">
                        <img src='`+ response[i].imagen + `' alt="" class="img-fluid rounded" id='` + response[i].id + `'>
                    </div>
                <div class="card-footer text-center bg-white">
                    <div class="font-weight-bold d-inline">
                        Precio :
                    </div>
                    `+ response[i].precio + ` C$
                    <span class="icon-manitaArriba" id="`+ response[i].id + `" name="` + response[i].likes + `"><span id="likes">` + response[i].likes + `</span></span>
                </div>
            </div>
        </div>
        </div>`);
            }
        }
    });
});
$('#formTiendaProducto').submit(function (e) {
    e.preventDefault();
    $.ajax({
        url:'/guardarProductoTienda',
        data:$('#formTiendaProducto').serialize(),
        type:'POST',
        dataType:'json',
        success: function (response) {
            alert(response.status);
        }
    });
});