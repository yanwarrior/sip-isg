
ko.extenders.validateItemQuantity = function (target, option) {
    target.subscribe(function (newValue) {
        if (option.stock < newValue) {
            target(1);
        }
    });
    return target;
};


function itemIsAvailable(items, product) {
    var find = items.find(function (elem) {
       return elem.product.id === product.id;
    });

    return find;
}

function Category(data) {
    this.id = ko.observable(data.id);
    this.name = ko.observable(data.name);
}

function Product(data) {
    this.id = ko.observable(data.id);
    this.name = ko.observable(data.name);
    this.category = ko.observable(new Category(data.category));
    this.price = ko.observable(data.price);
    this.stock = ko.observable(data.stock);
}

function Item(product) {
    this.product = ko.observable(new Product(product)); // mandatory id nya
    this.price = ko.observable(product.price); // mandatory
    this.quantity = ko.observable(1).extend({validateItemQuantity: product}); // mandatory
    this.subtotal = ko.computed(function () { // mandatory
        return this.quantity() * this.price();
    }, this);
}

function Order() {
    this.total = ko.observable(0); // mandatory
    this.payment = ko.observable(0);
    this.balance = ko.computed(function () {
        let result = this.payment() - this.total();
        if (result <= 0) {
            return 0;
        }

        return result;
    }, this);
}


function Customer(data) {
    this.id = ko.observable(data.id);
    this.name = ko.observable(data.name);
    this.email = ko.observable(data.email);
}


function OrderAddViewModel() {
    let self = this;
    self.categories = ko.observableArray([]);
    self.categoryQuery = ko.observable({});
    self.categoryPaginationNext = ko.observable();
    self.categoryPaginationPrev = ko.observable();

    self.products = ko.observableArray([]);
    self.productQuery = ko.observable({});
    self.productPaginationNext = ko.observable();
    self.productPaginationPrev = ko.observable();

    self.items = ko.observableArray([]);
    self.order = ko.observable(new Order());

    self.customers = ko.observableArray([]);
    self.selectedCustomer = ko.observable(null);
    self.customerQuery = ko.observable({});
    self.customerPaginationNext = ko.observable();
    self.customerPaginationPrev = ko.observable();

    self.errorXHR = ko.observable(null);

    self.getCategories = function () {
        $.ajax({
            url: '{{ url_ajax_category_list }}',
            type: 'GET',
            data: self.categoryQuery(),
            success: function (resp, status, request) {
                let temp = [];
                resp.forEach(function (category) {
                    temp.push(new Category(category));
                });

                self.categoryPaginationNext(JSON.parse(request.getResponseHeader('Link')).next);
                self.categoryPaginationPrev(JSON.parse(request.getResponseHeader('Link')).prev);
                self.categories(temp);
            },
            error: function (resp, status, err) { }
        });
    };

    self.getProducts = function (data, event) {
        $.ajax({
            url: '{{ url_ajax_product_list }}',
            type: 'GET',
            data: self.productQuery(),
            success: function (resp, status, request) {
                let temp = [];
                resp.forEach(function (product) {
                    temp.push(new Product(product));
                });

                self.productPaginationNext(JSON.parse(request.getResponseHeader('Link')).next);
                self.productPaginationPrev(JSON.parse(request.getResponseHeader('Link')).prev);
                self.products(temp);
            },
            error: function (resp, status, err) { }
        });
    };

    self.getCustomers = function (data, event) {
        $.ajax({
            url: '{{ url_ajax_customer_list }}',
            type: 'GET',
            data: self.customerQuery(),
            success: function (resp, status, request) {
               let temp = [];
               resp.forEach(function (customer) {
                  temp.push(new Customer(customer));
               });
               self.customerPaginationNext(JSON.parse(request.getResponseHeader('Link')).next);
               self.customerPaginationPrev(JSON.parse(request.getResponseHeader('Link')).prev);
               self.customers(temp);
            },
            error: function (resp, status, request) {
                
            }
        });
    };

    self.paginateCategories = function (data, event) {
        self.categoryQuery().page = event.target.dataset.page;
        self.getCategories();
    };

    self.paginateProducts = function (data, event) {
        self.productQuery().page = event.target.dataset.page;
        self.getProducts();
    };

    self.paginateCustomers = function (data, event) {
        self.customerQuery().page = event.target.dataset.page;
        self.getCustomers();
    }

    self.searchCategories = function (data, event) {
        if (event.charCode === 13) {
            self.categoryQuery().name = event.target.value;
            self.getCategories();
        }
        return true;
    };

    self.searchProducts = function (data, event) {
        if (event.charCode === 13) {
            self.productQuery().name = event.target.value;
            self.getProducts();
        }
        return true;
    };

    self.searchCustomers = function (data, event) {
        if (event.charCode === 13) {
            self.customerQuery().name = event.target.value;
            self.getCustomers();
        }
        return true;
    };

    self.selectCategory = function (data, event) {
        self.productQuery().category_id = data.id;
        self.getProducts();
    };

    self.selectProduct = function (data, event) {
        if (!itemIsAvailable(ko.toJS(self.items), ko.toJS(data))) {
            self.items.push(new Item(ko.toJS(data)));
        }
    };

    self.selectCustomer = function (data, event) {
        self.selectedCustomer(data);
    };

    self.updateOrder = function () {
        let items = ko.toJS(self.items);
        let total = 0;
        items.forEach(function (elem) {
            total += elem.subtotal;
        });

        self.order().total(total);
    };

    self.removeItem = function (data, event) {
        self.items.remove(data);
    };

    self.showPopupCustomerList = function(data, event) {
        $("#popup_customer_list").modal('show');
        self.getCustomers();
    };

    self.save = function (data, event) {
        console.log(ko.toJS(self.items));
        console.log(ko.toJS(self.selectedCustomer));
        console.log(ko.toJS(self.order));

        let payload = {
            items: ko.toJS(self.items),
            customer: ko.toJS(self.selectedCustomer),
            order: ko.toJS(self.order)
        };

        $.ajax({
            url: '{{ url_ajax_order_add }}',
            type: 'POST',
            data: ko.toJSON(payload),
            contentType: 'application/json',
            cache: false,
            success: function (resp, status, request) {
                console.log(resp);
            },
            error: function (resp, status, request) {
                self.errorXHR(resp.responseJSON);
                console.log(self.errorXHR());
            }
        });
    };

    self.clearErrorXHR = function (data, event) {
        self.errorXHR(null);
    };

    ko.computed(function () {
        self.getCategories();
        self.getProducts();
        self.updateOrder();
    }, self);
}

ko.applyBindings(new OrderAddViewModel());