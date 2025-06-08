import * as mod from "orderReception.js";

function Product(id, name, sell_price, quantity, p_stock_id) {
    // Propiedades
    this.id = id;
    this.name = name;
    this.sell_price = sell_price;
    this.quantity = quantity || 0; // Valor por defecto
    this.p_stock_id = p_stock_id;
    
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
            this.quantity++;
            this.updateUI();
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
