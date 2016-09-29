var Socketpart2 = angular.module('Commerce', []);

Socketpart2.controller('MainPageController', function($scope) {
        var socket = io.connect('https://' + document.domain + ':' + location.port + '/eCom');
        
        $scope.loginFailed = "" 

        socket.on('connect', function() {
                console.log('connected to the controller')
        });

        $scope.login = function login() {
                console.log('enter');
                var user = $scope.username;
                var password = $scope.password;
                console.log('inside the login controller')
                socket.emit('login', user, password);
        };

        socket.on('redirect', function(destination) {
                window.location.href = destination;
        });
        
         socket.on('loginFailed', function(msg) {
		document.getElementById('message').textContent = msg;
        });
});