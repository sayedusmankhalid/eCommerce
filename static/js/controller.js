var Socketpart2 = angular.module('Commerce', []);

Socketpart2.controller('MainPageController', function($scope) {
    var socket = io.connect('https://' + document.domain + ':' + location.port + '/eCom');

    $scope.loginFailed = ""
    $scope.sellerInfoList = [];

    socket.on('connect', function() {
        console.log('connected to the controller')
    });
    //////////////////login////////////////////////////////////////////////
    $scope.login = function login() {
        var user = $scope.username;
        var password = $scope.password;
        socket.emit('login', user, password);
    };


    socket.on('redirect', function(destination) {
        var loginLink = document.getElementById('loginLink');
        window.location.href = destination;
    });

    socket.on('loginFailed', function(msg) {
        $('#message').text(msg);


    });
    ////////////////////registration///////////////////////////////////////
    $scope.register = function register() {
        socket.emit('register', $scope.userName, $scope.firstName, $scope.lastName,
            $scope.regPassword, $scope.conPassword, $scope.address, $scope.city,
            $scope.state, $scope.zip, $scope.country, $scope.email);
    };

    socket.on('regFail', function(msg) {
        document.getElementById('regMessage').textContent = msg;
        $('#regMessage').text(msg);
    });
    /////////////////////seller information/////////////////////////////////
    $scope.sellerInfo = function sellerInfo(name) {

        socket.emit('sellerInfo', name);

    };

    socket.on('returnSellerInfo', function(information) {
        $('#sellerName').text("Full Name: " + information.firstname + " " + information.lastname);
        $('#address').text("Address: " + information.address + ", " + information.city + " " + information.state + " " + information.zip + " " + information.country)
        $('#email').text("Email: " + information.email)
 
    });
    ///////////////////////////// Post Product ////////////////////////////
    $scope.postProduct = function postProduct() {
        var today = new Date();
        var dd = today.getDate();
        var mm = today.getMonth() + 1; //January is 0!
        var yyyy = today.getFullYear();

        if (dd < 10) {
            dd = '0' + dd
        }

        if (mm < 10) {
            mm = '0' + mm
        }

        today = yyyy + '-' + mm + '-' + dd;

        socket.emit('postProduct', $scope.productName, $scope.price, $scope.quantity, $scope.category, $scope.desc, today )

    }
    
//////////////////////////////////Searh Product//////////////////////////////
$scope.searchProduct = function searchProduct() {
    
    var searchInput = $('#searchInput').val();
    var category =$('#cat').text();
    socket.emit('searchProduct', searchInput, category);
};
    
    
});
