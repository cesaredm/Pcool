$(document).ready(() => {

});

window.addEventListener('hashchange', function () {
    var url = window.location.hash;

    switch (url) {
        case '#/ingresos':
            $('#Ingresos').show(500);
            $('#productos').hide(500);
            break;
        case '#/productos':
            $('#Ingresos').hide(500);
            $('#productos').show(500);
            $.get('/mostrarProducto', {}, (response) => {
                let template = `<table class='table table-striped table-dark table-table-hover'>
                                <thead>
                                    <tr class='text-center'>
                                        <th>Nombre</td>
                                        <th>Nombre</td>
                                        <th>Nombre</td>
                                        <th>Nombre</td>
                                        <th>Nombre</td>
                                        <th>Nombre</td>
                                        <th>Nombre</td>
                                        <th>Nombre</td>
                                        <th>Nombre</td>
                                    </tr>
                                </thead>`
                                ;
                let datos = JSON.parse(response);
                let i;
                for(i= 0; i<datos.length;i++){
                    template += `
                                    <tr>
                                        <td>${datos[i].nombre}</td>
                                        <td>${datos[i].talla}</td>
                                        <td>${datos[i].color}</td>
                                        <td>${datos[i].precio}</td>
                                    </td>`;
                }
                template += "</table>";
                $('#mostrarProductos').html(template);
            });
            break;
        default:
            break;
    }

});