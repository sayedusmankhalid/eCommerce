var Socketpart2 = angular.module('Commerce', []);

Socketpart2.controller('MainPageController', function($scope) {
        var socket = io.connect('https://' + document.domain + ':' + location.port + '/eCom');
        
        $scope.loginFailed = "" 

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
               //var model = document.getElementById('login');
                var loginLink = document.getElementById('loginLink');
                window.location.href = destination;
       });
        
        socket.on('loginText', function(name) {
           console.log(name); 
        });
        
         socket.on('loginFailed', function(msg) {
		//document.getElementById('message').textContent = msg;
		$('#message').text(msg);


        });
        ////////////////////registration///////////////////////////////////////
        $scope.register = function register(){
        console.log('inside the register controller');
          socket.emit('register',$scope.userName, $scope.firstName, $scope.lastName,
                        $scope.regPassword,$scope.conPassword, $scope.address, $scope.city,
                        $scope.state, $scope.zip, $scope.country, $scope.email);      
        };
        
        socket.on('regFail', function(msg) {
		document.getElementById('regMessage').textContent = msg;
		$('#regMessage').text(msg);
        });
});