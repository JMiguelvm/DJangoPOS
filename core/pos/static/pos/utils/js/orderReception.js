
function showError(text) {
    $.confirm({
        title: 'Error',
        content: text,
        type: 'red',
        typeAnimated: true,
        buttons: {
            confirmar: function () {
            }
        }
    });
}
// Create a data table with name_fields array, element where dt must place and ajax to fill data
function createTable (name_fields, element, ajax = null, data = null) {
    const table = document.createElement("table");
    table.classList = "display compact"
    table.style.width = "100%";
    const tr = document.createElement("tr");
    // Write the title fields of the table
    name_fields.forEach(name => {
        const th = document.createElement("th");
        th.textContent = name;
        tr.append(th);
    });
    const thead = document.createElement("thead");
    const tfoot = document.createElement("tfoot");
    const tbody = document.createElement("tbody");
    thead.appendChild(tr.cloneNode(true));
    table.appendChild(thead);
    table.appendChild(tbody);
    config = {
        lengthChange: false,
        pageLength: 5, 
        info: false,
        paging: true,
        searching: true,
        responsive: true,
        columnDefs: [
            { visible: false, targets: 0 },
            { className: 'pointer', targets: "_all" }
        ]
    }
    if (ajax) {
        config.ajax = ajax;
    }
    else {
        config.data = data;
    }
    element.append(table);
    let dt = new DataTable(table, config);
    // Usuful to get data form dt
    return dt
}

function scanBarCode(content) {
    const container = document.createElement('div');
    container.style.marginBottom = '20px';
    
    let input = document.createElement('input');
    input.type = 'text';
    input.placeholder = 'Seleccione para ingresar código de barras.';
    input.className = 'form-control mb-3';
    
    container.appendChild(input);
    content.append(container);
    setTimeout(() => input.focus(), 100);
    $(input).on('keydown', function(event) {
        if (event.keyCode === 13) {
            let bar_code = $(input).val();
            $.ajax({
                type: "POST",
                url: "/pos/get_product_by_barcode",
                contentType: 'application/json',
                data: JSON.stringify({barcode: bar_code}),
                headers: {'X-CSRFTOKEN': CSRF_TOKEN},
                success: function (response) {
                    if (response.status == 'success') {
                        receiveProduct(response.product.id, response.product.name);
                        $(input).val('')
                    }
                    else if (response.status == 'error') {
                        showError(response.message);
                    }
                }
                
            });
        }
    });
}

function receiveProduct(id, name) {
    dialog = $.confirm({
        title: 'Recibir producto: '+name+'',
        content: `
        <input type="number" min="0" name="amount" placeholder="Cantidad" class="form-control" required>
        <input type="number" min="0" name="price" placeholder="Precio de compra por unidad (Sin IVA)" class="form-control" required>
        `,
        buttons: {
            confirmar: function() {
                let context = {
                    id: id,
                    amount: this.$content.find('input[name="amount"]').val(),
                    price: this.$content.find('input[name="price"]').val()
                };
                $.ajax({
                    type: "POST",
                    url: "/pos/add_stock",
                    contentType: 'application/json',
                    data: JSON.stringify(context),
                    headers: {'X-CSRFTOKEN': CSRF_TOKEN},
                    success: function (response) {
                        if (response.status == 'success') {
                            $.alert("Inventario añadido con éxito.");
                        }
                        else {
                            showError("No fue posible añadir el inventario.");
                        }
                    }
                    
                });
            },
            cancelar: function () {
            }
        }
    });
}

function productList(response) {
    dialog_product = $.confirm({
        title: 'Recibir un pedido',
        content: 'Seleccione el producto a recibir:<br><small><i>Si no lo ve aquí debe crear un seguimiento de ese producto</i></small>',
        onContentReady: function () {
            dt = createTable (["id", "Nombre", "Precio", "Inventario"], this.$content[0], null, response)
            dt.on('click', 'tbody tr', function () {
                let data = dt.row(this).data();
                let product = dt.row(this).data();
                dialog_product.close();
                receiveProduct(product[0], product[1]);
            });
        },
        buttons: {
            cancelar: function () {
            }
        }
    });
}

$(document).ready(function() {
  $("#recieve").click(function () {
    dialog = $.confirm({
        title: 'Recibir un pedido',
        content: 'Seleccione el vendedor del producto que desea recibir:',
        onContentReady: function () {
            scanBarCode(this.$content[0]);
            dt = createTable (["id", "Nombre", "Número"], this.$content[0], '/pos/get_vendor')
            dt.on('click', 'tbody tr', function () { 
                let data = dt.row(this).data();
                let context = {id: dt.row(this).data()[0] /*ID form VENDOR ROW*/}
                $.ajax({
                    type: "POST",
                    url: "/pos/get_products",
                    contentType: 'application/json',
                    data: JSON.stringify(context),
                    headers: {'X-CSRFTOKEN': CSRF_TOKEN},
                    success: function (response) {
                        if (response.status == 'success') {
                            productList(response.data);
                        }
                        else {
                            showError("No se encontraron productos con seguimiento de inventario para ese vendedor.");
                        }
                    }
                    
                });
                dialog.close()
            });
        },
        buttons: {
            cancelar: function () {
            }
        }
    });
});
});



