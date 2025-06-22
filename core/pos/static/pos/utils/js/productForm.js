// Diccionario en donde ira la id de el product stock, ligado a X instancia de product card
var products = new Map();

/* =========================
   FUNCIONES DE PRODUCTO
   ========================= */

// Constructor de producto
function Product(id, name, sell_price, stock, p_stock_id) {
    // Propiedades
    this.id = id;
    this.name = name;
    this.sell_price = sell_price;
    this.quantity = 1; // Valor por defecto
    this.p_stock_id = p_stock_id;
    this.stock = stock;
    
    // IDs dinámicos
    this.t_quantity = 'q' + this.id;
    this.t_total = 't' + this.id;
    this.t_product = 'p' + this.id;
    this.t_delete = 'd' + this.id;

    // Método para crear el elemento (sin insertarlo en el DOM)
    this.createElement = function() {
        const html = `
            <div class="p-2 border-bottom" id="${this.t_product}">
                <div class="card-header modal-header d-flex justify-content-between mb-2">
                    <h5 class="modal-title">${this.name}</h5>
                    <button type="button" class="btn-close" id="${this.t_delete}" aria-label="Close"></button>
                </div>
                <div class="flex-fill d-flex justify-content-center align-items-center">
                    <div style="width: 300px;">
                        <div class="input-group">
                            <button type="button" class="btn btn-outline-secondary p-subtract">-</button>
                            <input type="number" id="${this.t_quantity}" class="form-control" value="${this.quantity}" readonly>
                            <button type="button" class="btn btn-outline-secondary p-add">+</button>
                        </div>
                    </div>
                    <div style="width: 150px;">
                        <div class="text-center align-content-center">
                            <h4><span id="${this.t_total}" class="p_card_price">${this.sell_price * this.quantity}</span></h4>
                        </div>
                    </div>
                </div>
            </div>
        `;

        const element = document.createRange().createContextualFragment(html);
        const $element = $(element);

        // Eventos con arrow functions (para mantener `this`)
        $element.find('.p-subtract').click((e) => {
            e.preventDefault();
            if (this.quantity > 0) {
                this.quantity--;
                this.updateUI();
            }
        });

        $element.find('.p-add').click((e) => {
            e.preventDefault();
            if (this.quantity > 0 && this.quantity+1 <= this.stock) {
                this.quantity++;
                this.updateUI();
            }
        });
        $element.find('#'+this.t_delete).click((e) => {
            let product = this;
            e.preventDefault();
            $.confirm({
                title: 'Advertencia',
                content: "¿Estás seguro de eliminar este producto de la orden de venta?",
                type: 'red',
                typeAnimated: true,
                buttons: {
                    confirmar: function () {
                        product.delete();
                    },
                    cancelar: function () {
                        
                    }
                }
            });
        });

        return $element;
    };

    // Método para actualizar la UI
    this.updateUI = function() {
        if ($("#sTotal").text() == 0 || $("#sTotal").text() == "$0") {
            $("#btnDraft").prop("disabled", false);
            $("#makeOrder").prop("disabled", false);
        }

        $(`#${this.t_quantity}`).val(this.quantity);
        $(`#${this.t_total}`).text(this.sell_price * this.quantity);
        $(`#${this.t_total}`).priceFormat({
            allowNegative: true,
            centsLimit: 0,
            prefix: '$'
        });

        let total = 0;

        $(".p_card_price").each(function(key, value) {
            let raw = $(this).text().replace(/[^0-9.-]+/g, ""); // Si tiene priceformat, lo quita
            let amount = parseFloat(raw);
            total += amount;
        });
        
        $("#sTotal").text(total.toFixed());
        $("#sTotal").priceFormat({
            allowNegative: true,
            centsLimit: 0,
            prefix: '$'
        });
    };

    // Método para renderizar en el DOM
    this.render = function(container = '#cart_product') {
        if (!document.getElementById(this.t_product)) {
            this.$element = this.createElement();
            $(container).prepend(this.$element);
            this.updateUI(); // Actualiza valores iniciales
        }
    };
    // Método para eliminar el producto del resumen de venta
    this.delete = function() {
        $("#"+this.t_product).remove();
        products.delete(this.id);
        this.updateUI();
        if ($("#sTotal").unmask() == 0) {
            $("#btnDraft").prop( "disabled", true );
            $("#makeOrder").prop( "disabled", true );
        }
    };
}

// Verifica y agrega producto a la orden
function verifyProductInOrder(id, name, sell_price, stock, p_stock_id) {
    if (products.has(id)) {
        let selectedProduct = products.get(id);
        if ((selectedProduct.quantity > 0) && (selectedProduct.quantity+1 <= selectedProduct.stock)) {
            selectedProduct.quantity++;
            selectedProduct.updateUI();
        }
    }
    else {
        let selectedProduct = new Product(id, name, sell_price, stock, p_stock_id);
        if (selectedProduct.stock > 0) {
            products.set(id, selectedProduct);
            selectedProduct.render();
            $(products).each(function( key, value ) {
                console.log(key)
                console.log(value)
            });
        }
        else {
            showError("Este producto no tiene inventario.");
        }
    }
}

// Limpia todos los productos de la orden
function clearProducts() {
    $("#sSubtotal").text('$0');
    $("#sTotal").text('$0');
    $("#btnDraft").prop("disabled", true);
    $("#makeOrder").prop("disabled", true);

    products.forEach(product => {
        product.delete();
    });
    products.clear();
}

/* =========================
   FUNCIONES DE TABLA Y ORDEN
   ========================= */

// Crea una tabla de productos
function pCreateTable (name_fields, element, ajax = null, data = null) {
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
        paging: true,
        searching: true,
        responsive: true,
        columnDefs: [
            { targets: [0], visible: false},
            { targets: '_all', visible: true },
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

// Realiza la orden de venta
function makeOrder(type) {
    if (products.size > 0) {
        let data = [type, []];
        products.forEach((value, key) => {
            data[1].push({
                "stock_id": key,
                "quantity": value.quantity,
                "sell_price": value.sell_price
            });
        });

        $.ajax({
            type: "POST",
            url: "/pos/make_order",
            contentType: 'application/json',
            data: JSON.stringify(data),
            headers: { 'X-CSRFTOKEN': CSRF_TOKEN },
            success: function (response) {
                if (response.status === 'success') {
                    $.notify("Venta realizada con éxito.", "success");
                    clearProducts();
                    order_list.ajax.reload();
                } else {
                    $.notify(response.message || "Ocurrió un error desconocido.", "error");
                }
            },
            error: function (xhr) {
                let message = "Error del servidor.";
                if (xhr.responseJSON && xhr.responseJSON.message) {
                    message = xhr.responseJSON.message;
                }
                $.notify(message, "error");
            }
        });

    } else {
        $.notify("Debe haber productos en la orden de venta.", "warn");
    }
}

/* =========================
   FUNCIONES DE UI Y EVENTOS
   ========================= */

$(document).ready(function() {
    // Tabla de productos
    productTable = pCreateTable(["id","Nombre", "Precio", "Categoria", "Inventario"], $("#product_list"), '/pos/get_stock');
    $("#product_list > .dt-container").css("width", "100%");
    $("#product_list > .dt-container").css("margin", "0");
    $("#product_list > .dt-container").attr("class", "dt-container border p-3 display table table-striped table-bordered table-hover dataTable");
    productTable.on('click', 'tbody tr', function () {
        let data = productTable.row(this).data();
        verifyProductInOrder(data[0][0], data[1], data[2], data[4], data[0][1], data[5]);
    });

    // Código de barras
    $('#btnBarCode').click(function() {
        $('#inputBarCode').toggle("slow");
        setTimeout(() => $('#bar-code').focus(), 100);
    });
    function submitBarcode() {
        let bar_code = $('#bar-code').val();
        if (bar_code == "") {
            showError("Ingrese un código de barras.")
            setTimeout(() => $('#bar-code').focus(), 100);
        }
        else {
            $.ajax({
                type: "POST",
                url: "/pos/get_product_by_barcode",
                contentType: 'application/json',
                data: JSON.stringify({barcode: bar_code}),
                headers: {'X-CSRFTOKEN': CSRF_TOKEN},
                success: function (response) {
                    if (response.status == 'success') {
                        verifyProductInOrder(response.product.id, response.product.name, response.product.price, response.product.stock, response.product.stock_id);
                        $('#bar-code').val('');
                        setTimeout(() => $('#bar-code').focus(), 100);
                    }
                    else if (response.status == 'error') {
                        showError(response.message);
                    }
                }
            });
        }
    }
    $('#bar-code').on('keydown', function(event) {
        if (event.keyCode === 13) {
            submitBarcode();
        }
    });

    // Botón para realizar orden
    $('#makeOrder').on('click', function(e) {
        makeOrder(2);
    });

    // Renderizar detalle de orden
    function renderOrder(id) {
        $.ajax({
            type: "POST",
            url: "/pos/get_specific_order",
            contentType: 'application/json',
            data: JSON.stringify({"id": id}),
            headers: {'X-CSRFTOKEN': CSRF_TOKEN},
            success: function (response) {
                let items = ``;
                let i = 1;
                let total = 0;
                response.items.forEach(item => {
                    items += `
                    <tr>
                        <td>${i}</td>
                        <td><strong>${item.order_item.product_name}</strong></td>
                        <td class="text-center">${item.order_item.quantity}</td>
                        <td class="text-center order_sumary_price">${parseInt(item.order_item.sell_price)}</td>
                        <td class="text-right order_sumary_price">${parseInt(item.order_item.total)}</td>
                    </tr>
                    `;
                    total += parseInt(item.order_item.total);
                    i++;
                });
                let status = "";
                switch (response.order.status) {
                    case 1: status = 'Borrador';
                    break;
                    case 2: status = 'Publicada';
                    break;
                    case 3: status = 'Anulada';
                    break;
                    default: status = 'Desconocido';
                }
                let html = `
                    <div class="container">
                    <!-- BEGIN INVOICE -->
                    <div class="invoice grid">
                        <div class="grid-body">
                        <div class="invoice-title">
                            <h2>Orden de venta<br><span class="small">#${response.order.id}</span></h2>
                        </div>
                        <hr>
                        <div class="d-flex justify-content-between">
                            <address class="text-right">
                            <strong>Fecha de orden:</strong><br>
                            ${response.order.date}
                            </address>
                            <address class="text-right">
                            <strong>Estado:</strong><br>
                            ${status}
                            </address>
                        </div>
                        <table class="table table-striped mt-3">
                            <thead>
                            <tr class="line">
                                <td><strong>#</strong></td>
                                <td class="text-center"><strong>PRODUCTO</strong></td>
                                <td class="text-center"><strong>CANTIDAD</strong></td>
                                <td class="text-right"><strong>(C/U)</strong></td>
                                <td class="text-right"><strong>SUBTOTAL</strong></td>
                            </tr>
                            </thead>
                            <tbody>
                            ${items}
                            <tr>
                                <td colspan="3"></td>
                                <td class="text-right"><strong>Total</strong></td>
                                <td class="text-right"><strong class="order_sumary_price">${total}</strong></td>
                            </tr>
                            </tbody>
                        </table>
                        </div>
                    </div>
                    <!-- END INVOICE -->
                    </div>
                    `;
                $.confirm({
                    backgroundDismiss: true,
                    columnClass: 'col-md-10',
                    title: false,
                    content: html,
                    onOpenBefore: function () {
                        $('.order_sumary_price').priceFormat({
                            allowNegative: true,
                            centsLimit: 0,
                            prefix: '$'
                        });
                    },
                    buttons: {
                        confirmar: function() {

                        }
                    }
                });
            }
        });
    }

    // Tabla de órdenes
    const order_list = $('#ordersTable').DataTable({
        ajax: {
            url: '/pos/get_orders',
            dataSrc: 'data'
        },
        columns: [
            { data: 'id', title: '# Orden' },
            { data: 'date', title: 'Fecha' },
            {
                data: 'status',
                title: 'Estado',
                render: function(data, type, row) {
                    switch (data) {
                        case 1: return 'Borrador';
                        case 2: return 'Publicada';
                        case 3: return 'Anulada';
                        default: return 'Desconocido';
                    }
                }
            }
        ],
        rowCallback: function(row, data) {
            if (data.status == 1) {
                $(row).addClass("table-warning");
            } else if (data.status == 2) {
                $(row).addClass("table-success");
            } else if (data.status == 3) {
                $(row).addClass("table-secondary");
            }
        },
        lengthChange: false,
        info: false,
        responsive: true,
        columnDefs: [
            { className: 'pointer', targets: "_all" }
        ]
    });
    order_list.on('click', 'tbody tr', function () {
        let data = order_list.row(this).data();
        renderOrder(data.id);
    });

});