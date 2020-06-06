/*$(document).ready(function () {
    mostrarProductoKamell();
});

function mostrarProductoKamell() {
    $.ajax({
        url: '/productosKamell',
        type: 'POST',
        data: {
            nombreTienda: 'kamell'
        },
        dataType: 'json',
        succes: function (respuesta) {
            var template = "";
            var datos = JSON.parse(respuesta);
            var i;
            for (i = 0; i < datos.length; i++) {
                template += `
                            <div class="col-6 col-sm-6 col-md-4 col-lg-3 mt-2 elemento">
                            <div class="card shadow">
                                <div class="card-header bg-white p-0">
                                    <div class="text-center lead small">
                                        <h1>${datos[i].nombre}</h1>
                                    </div>
                                </div>
                                    <div class="card-body pt-2 pb-2" data-toggle="modal" data-target="#exampleModalLong">
                                        <img src="${datos[i].img}" alt="" class="img-fluid rounded" id='${datos[i].id}'>
                                    </div>
                                <div class="card-footer text-center bg-white p-1">
                                    <span class="icon-manitaArriba" id=""><span id="likes">${datos[i].likes}</span></span>
                                </div>
                            </div>
                        </div>`;
            };
            $('#galeria').html(template);
        }
    });
}*/