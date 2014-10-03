var app = angular.module('myCaloriesApp', [ 'ngAnimate', 'ngRoute']);

app.config(['$httpProvider', '$routeProvider', function($httpProvider, $routeProvider) {
    $routeProvider.when('/', {
        templateUrl: "/static/templates/home.html",
        controller: "HomeController"
    })
    .when('/settings', {
        templateUrl: '/static/templates/settings.html',
        controller: 'SettingsController'
    })
    .when('/profile', {
        templateUrl: '/static/templates/profile.html',
        controller: 'ProfileController'
    })
    .when('/signup', {
        templateUrl: '/static/templates/register.html',
        controller: 'RegisterController'
    })
    .otherwise({redirectTo: '/'});
    $httpProvider.defaults.xsrfCookieName = 'csrftoken';
    $httpProvider.defaults.xsrfHeaderName = 'X-CSRFToken';
}]);


app.controller('HomeController', ['$scope', '$http', function($scope, $http) {
    $scope.todo = {'priority' : 10 };
    $scope.todo_list = [];
    $scope.predicate = 'priority';
    $scope.reverse = false;
    $scope.user_msg = "";

    $scope.initial = function (){
        $http({
            method: 'GET',
            url: '/api/v1/meal/?format=json'
        }).success(function(data, status, headers) {
                $scope.todo_list = data.objects;
        }).error(function(data, status, headers) {
                console.log("Error trying to get todo items!" + status + headers);
                $scope.userMsg("error", status)
        });
    };

    $scope.userMsg = function(type, msg) {
        if (type == 'error') {
            $scope.user_msg = "Error: " + msg;
            $('#user-msg').removeClass('error-msg warning-msg info-msg success-msg').addClass('error-msg');
        } else if (type == 'success') {
            $scope.user_msg = "Success: " + msg;
            $('#user-msg').removeClass('error-msg warning-msg info-msg success-msg').addClass('success-msg');
        } else if (type == 'warning') {
            $scope.user_msg = "Warning: " + msg;
            $('#user-msg').removeClass('error-msg warning-msg info-msg success-msg').addClass('warning-msg');
        } else {
            $scope.user_msg = "Info: " + msg;
            $('#user-msg').removeClass('error-msg warning-msg info-msg success-msg').addClass('info-msg');
        };
    };


    $scope.addTodo = function() {
        console.log("addTodo was called");
        console.log($scope.todo);
        $http({
            method: 'POST',
            url: '/api/v1/item/?format=json',
            data: $scope.todo
        }).success(function(data, status, headers) {
                $http({
                        method: 'GET',
                        url: '/api/v1/item/?format=json'
                    }).success(function(data, status, headers) {
                            $scope.initial();
                    }).error(function(data, status, headers) {
                            console.log("Error trying to get todo items!" + status + headers);
                    });
                $scope.todo = {};
                $scope.userMsg("success", "Item Added.")

        }).error(function(data, status, headers) {
                console.log("Error trying to get todo items!" + status + headers);
                $scope.userMsg("error", status)
        });
    };
}]);

app.directive('datetimez', function() {
    return {
        restrict: 'A',
        require : 'ngModel',
        link: function(scope, element, attrs, ngModelCtrl) {
            element.datetimepicker({
                dateFormat:'dd/MM/yyyy hh:mm:ss',
                language: 'en-US'
            }).on('changeDate', function(e) {
                    ngModelCtrl.$setViewValue(e.date);
                    scope.$apply();
                });
            $('.icon-chevron-up').each(function(){
                $(this).addClass('glyphicon glyphicon-chevron-up');
            });
            $('.icon-chevron-down').each(function(){
                $(this).addClass('glyphicon glyphicon-chevron-down');
            });
        }
    };
});

app.controller('ItemController', ['$scope', '$http', function($scope, $http) {
    $scope.todo = null;
    $scope.edit_view = false;

    $scope.init = function(item) {
        $scope.todo = item;
    };

    $scope.save = function () {
        $http({
            method: 'PUT',
            url: '/api/v1/item/'+ $scope.todo.id +'?format=json',
            data: $scope.todo
        }).success(function(data, status, headers) {
                $scope.edit_view = false;
        }).error(function(data, status, headers) {
                console.log("Error trying to save item!" + status + headers);
        });
    };

    $scope.markAsDone = function () {
        $scope.todo.completed = true;
        $http({
            method: 'PUT',
            url: '/api/v1/item/'+ $scope.todo.id +'?format=json',
            data: $scope.todo
        }).success(function(data, status, headers) {
                $('#item-' + $scope.todo.id + ' legend').addClass('done');
        }).error(function(data, status, headers) {
                console.log("Error trying to markAsDone item!" + status + headers);
        });
    };

    $scope.markAsUndone = function () {
        $scope.todo.completed = false;
        $http({
            method: 'PUT',
            url: '/api/v1/item/'+ $scope.todo.id +'?format=json',
            data: $scope.todo
        }).success(function(data, status, headers) {
                $('#item-' + $scope.todo.id + ' legend').removeClass('done');
        }).error(function(data, status, headers) {
                console.log("Error trying to markAsUndone item!" + status + headers);
        });
    };

    $scope.editItem = function () {
        $scope.edit_view = true;
        console.log("editItem called for item");
        console.log($scope.todo);
    };

    $scope.deleteItem = function () {
        $http({
            method: 'DELETE',
            url: '/api/v1/item/'+ $scope.todo.id +'?format=json'
        }).success(function(data, status, headers) {
                $('#item-' + $scope.todo.id).remove();
                $scope.todo = null;
        }).error(function(data, status, headers) {
                console.log("Error trying to delete item!" + status + headers);
        });
    };
}]);

app.controller('ApiController', ['$scope', '$http', function($scope, $http) {
    $scope.refreshToken = function() {
        $http({
            method: 'GET',
            url: '/api/v1/user/?format=json'
        }).success(function(data, status, headers) {
                $scope.settings = data.objects[0];
        }).error(function(data, status, headers) {
                console.log("Error trying to get user settings!" + status + headers);
        });
    };
}]);

app.controller('SettingsController', ['$scope', '$http', function($scope, $http) {
    $scope.settings = {name: "",
                       email: "",
                       expected_calories: 0};

    $scope.initial = function () {
        $http({
            method: 'GET',
            url: '/api/v1/user/?format=json'
        }).success(function(data, status, headers) {
                $scope.settings = data.objects[0];
        }).error(function(data, status, headers) {
                console.log("Error trying to get user settings!" + status + headers);
        });
    };

    $scope.save = function () {
        $http({
            method: 'PUT',
            url: '/api/v1/user/'+ $scope.settings.username +'?format=json',
            data: $scope.settings
        }).success(function(data, status, headers) {
                console.log("User settings saved!" + status + headers);
        }).error(function(data, status, headers) {
                console.log("Error trying to save user settings!" + status + headers);
        });
    };
}]);

app.controller('RegisterController', function($scope) {

});