// Diccionario en donde ira la id de el product stock, ligado a X instancia de product card
var products = new Map();

// Create a data table with name_fields array, element where dt must place and ajax to fill data
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
            { targets: [0, 5], visible: false},
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

function Product(id, name, sell_price, stock, p_stock_id, iva) {
    // Propiedades
    this.id = id;
    this.name = name;
    this.sell_price = sell_price;
    this.quantity = 1; // Valor por defecto
    this.p_stock_id = p_stock_id;
    this.stock = stock;
    this.iva = iva;
    
    // IDs dinámicos
    this.t_quantity = 'q' + this.id;
    this.t_total = 't' + this.id;
    this.t_product = 'p' + this.id;

    // Método para crear el elemento (sin insertarlo en el DOM)
    this.createElement = function() {
        const html = `
            <div class="p-2 border-bottom" id="${this.t_product}">
                <div class="card-header modal-header d-flex justify-content-between mb-2">
                    <h5 class="modal-title">${this.name}</h5>
                    <button type="button" class="btn-close productDelete" data-bs-dismiss="${this.id}" aria-label="Close"></button>
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
                            <h4><span id="${this.t_total}" class="p_card_price `+(this.iva ? "":"noIVA")+`">${this.sell_price * this.quantity}</span></h4>
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
        contextProduct = this;
        $element.find('.productDelete').click((e) => {
            e.preventDefault();
            $.confirm({
                title: 'Advertencia',
                content: "¿Estás seguro de eliminar este producto de la orden de venta?",
                type: 'red',
                typeAnimated: true,
                buttons: {
                    confirmar: function () {
                        contextProduct.delete();
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
        if ($("#sTotal").text() == 0) {
            $("#btnDraft").prop( "disabled", false );
            $("#makeOrder").prop( "disabled", false );
        }
        $(`#${this.t_quantity}`).val(this.quantity);
        $(`#${this.t_total}`).text((this.sell_price * this.quantity)); // .text() en lugar de .val()
        $(`#${this.t_total}`).priceFormat({
            allowNegative: true,
            centsLimit: 0,
            prefix: '$'
        });
        let subtotal = 0;
        let iva = 0;
        $(".p_card_price").each(function( key, value ) {
            subtotal += parseInt($(".p_card_price").eq(key).unmask());
            if(!($(".p_card_price").eq(key).hasClass('noIVA'))) {
                iva += parseInt($(".p_card_price").eq(key).unmask());
            }
        });
        iva = (iva/100)*19;
        let total = subtotal + iva;
        $("#sSubtotal").text(subtotal);
        $("#sSubtotal").priceFormat({
            allowNegative: true,
            centsLimit: 0,
            prefix: '$'
        });
        $("#sIva").text(iva);
        $("#sIva").priceFormat({
            allowNegative: true,
            centsLimit: 0,
            prefix: '$'
        });
        $("#sTotal").text(total);
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

function verifyProductInOrder(id, name, sell_price, stock, p_stock_id, iva) {
    if (products.has(id)) {
        let selectedProduct = products.get(id);
        if ((selectedProduct.quantity > 0) && (selectedProduct.quantity+1 <= selectedProduct.stock)) {
            selectedProduct.quantity++;
            selectedProduct.updateUI();
        }
    }
    else {
        let selectedProduct = new Product(id, name, sell_price, stock, p_stock_id, iva);
        if (selectedProduct.stock > 0) {
            products.set(id, selectedProduct);
            selectedProduct.render();
        }
        else {
            showError("Este producto no tiene inventario.");
        }
    }
}

// Representación en UI de lista completa de productos
$(document).ready(function() {
    productTable = pCreateTable(["id","Nombre", "Precio", "Categoria", "Inventario", "iva"], $("#product_list"), '/pos/get_stock');
    $("#product_list > .dt-container").css("width", "100%");
    $("#product_list > .dt-container").css("margin", "0");
    $("#product_list > .dt-container").attr("class", "dt-container border p-3 display table table-striped table-bordered table-hover dataTable");
    productTable.on('click', 'tbody tr', function () {
        let data = productTable.row(this).data();
        verifyProductInOrder(data[0][0], data[1], data[2], data[4], data[0][1], data[5]);
    });
    $('#btnBarCode').click(function() {
        $('#inputBarCode').toggle();
    });
    function submitBarcode() {
        let bar_code = $('#bar-code').val();
        $.ajax({
            type: "POST",
            url: "/pos/get_product_by_barcode",
            contentType: 'application/json',
            data: JSON.stringify({barcode: bar_code}),
            headers: {'X-CSRFTOKEN': CSRF_TOKEN},
            success: function (response) {
                if (response.status == 'success') {
                    verifyProductInOrder(response.product.id, response.product.name, response.product.price, response.product.stock, response.product.stock_id, response.product.iva);
                    $('#bar-code').val('');
                    setTimeout(() => $('#bar-code').focus(), 100);
                }
                else if (response.status == 'error') {
                    showError(response.message);
                }
            }
        });
    }
    $('#bar-code').on('keydown', function(event) {
        if (event.keyCode === 13) {
            submitBarcode();
        }
    });

    $('#submitBC').on('click', function(e) {
        e.preventDefault();
        submitBarcode();
    });

});

