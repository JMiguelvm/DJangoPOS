document.addEventListener('DOMContentLoaded', function () {
    var addProduct = document.getElementById('addProduct');
    var divProduct = document.getElementById('addProductModal');
    var productBackground = document.getElementById('productBackground');
    var buttonCloseAddProduct = document.getElementById('closeAddProduct');
    var bEditCustomer = document.querySelectorAll('.bEditCustomer');
    

    function openAddProduct() {
        divProduct.style.display = 'block';
        productBackground.style.display = 'block';
    }

    function closeAddProduct() {
        divProduct.style.display = 'none';
        productBackground.style.display = 'none';
    }

    if (addProduct && buttonCloseAddProduct) {
        addProduct.addEventListener("click", openAddProduct);
        buttonCloseAddProduct.addEventListener("click", closeAddProduct);
    }
    
    if (bEditCustomer) {
        bEditCustomer.forEach(button => {
            button.addEventListener("click", () => {
                let bDataTarget = button.getAttribute('data-target');
                let divCustomer = document.getElementById(bDataTarget);
    
                divCustomer.style.display = 'flex';
                button.style.display = 'none';
            });
        });
    }

    
});