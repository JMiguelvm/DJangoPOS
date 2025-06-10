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

    // Método para crear el elemento (sin insertarlo en el DOM)
    this.createElement = function() {
        const html = `
            <div class="d-flex align-items-stretch border-secondary border-top border-bottom p-1 mb-2 mt-2" id="${this.t_product}">
                <div class="flex-fill">
                    <b class="m-1 fs-6">${this.name}</b>
                    <div class="p-2" style="height: 50px;">
                        <div class="input-group">
                            <button type="button" class="btn btn-outline-secondary p-subtract">-</button>
                            <input type="number" id="${this.t_quantity}" class="form-control" value="${this.quantity}" readonly>
                            <button type="button" class="btn btn-outline-secondary p-add">+</button>
                        </div>
                    </div>
                </div>
                <div style="width: 150px;">
                    <div class="text-center h-100 align-content-center">
                        <h4>$ <span id="${this.t_total}">${this.sell_price * this.quantity}</span></h4>
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

        return $element;
    };

    // Método para actualizar la UI
    this.updateUI = function() {
        $(`#${this.t_quantity}`).val(this.quantity);
        $(`#${this.t_total}`).text(this.sell_price * this.quantity); // .text() en lugar de .val()
    };

    // Método para renderizar en el DOM
    this.render = function(container = '#cart_product') {
        if (!document.getElementById(this.t_product)) {
            this.$element = this.createElement();
            $(container).prepend(this.$element);
            this.updateUI(); // Actualiza valores iniciales
        }
    };
}

// Representación en UI de lista completa de productos
$(document).ready(function() {

    // Diccionario en donde ira la id de el product stock, ligado a X instancia de product card
    var products = new Map();

    dt = createTable(["id","Nombre", "Precio", "Categoria", "Inventario"], $("#product_list"), '/pos/get_stock');
    $("#product_list > .dt-container").css("width", "100%");
    $("#product_list > .dt-container").css("margin", "0");
    $("#product_list > .dt-container").attr("class", "dt-container border p-3 display table table-striped table-bordered table-hover dataTable");
    dt.on('click', 'tbody tr', function () {
        let data = dt.row(this).data();
        if (products.get(data[0][0])) {
            product = products.get(data[0][0]);
            if ((product.quantity > 0) && (product.quantity+1 <= product.stock)) {
                product.quantity++;
                product.updateUI();
            }
            
        }
        else {
            let product = new Product(data[0][0], data[1], data[2], data[4], data[0][1]);
            if (product.stock > 0) {
                products.set(data[0][0], product);
                product.render();
            }
            else {
                showError("Este producto no tiene inventario.");
            }
        }
    });
});

