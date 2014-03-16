angular.module('blof', ['ngResource']).
    config(['$httpProvider', function($httpProvider){
        $httpProvider.defaults.xsrfHeaderName = 'X-CSRFToken';
        $httpProvider.defaults.xsrfCookieName = 'csrftoken';
    }]).
    service('authState', function () {
        return {
            user: undefined
        };
    }).
    factory('api', function($resource){
        function add_auth_header(data, headersGetter){
            var headers = headersGetter();
            headers['Authorization'] = ('Basic ' + btoa(data.username +
                                        ':' + data.password));
        }
        return {
            auth: $resource('/api/auth\\/', {}, {
                login:  {method: 'POST', transformRequest: add_auth_header},
                logout: {method: 'DELETE'}
            }),
            users: $resource('/api/users\\/', {}, {
                create: {method: 'POST'}
            }),
            posts: $resource('/api/posts\\/', {}, {
                list:   {method: 'GET', isArray: true},
                create: {method: 'POST'},
                detail: {method: 'GET', url: '/api/posts/:id'},
                delete: {method: 'DELETE', url: '/api/posts/:id'}
            })
        };
    }).
    controller('authController', function($scope, api, authState) {
        
        $('#id_auth_form input').checkAndTriggerAutoFillEvent();

        $scope.authState = authState;

        $scope.getCredentials = function(){
            return {username: $scope.username, password: $scope.password};
        };
        $scope.login = function(){
            api.auth.login($scope.getCredentials()).
                $promise.
                    then(function(data){
                        authState.user = data.username;
                    }).
                    catch(function(data){
                        alert(data.data.detail);
                    });
        };
        $scope.logout = function(){
            api.auth.logout(function(){
                authState.user = undefined;
            });
        };
        $scope.register = function($event){
            $event.preventDefault();
            api.users.create($scope.getCredentials()).
                $promise.
                    then($scope.login).
                    catch(function(data){
                        alert(data.data.username);
                    });
        };
    }).
    controller('postController', function($scope, api, authState){

        $scope.authState = authState;

        $scope.list = function(){
            api.posts.list(function(data){
                $scope.posts = data;
            });
        };
        $scope.list();

        $scope.create = function(){
            var data = {body: $scope.body};
            api.posts.create(data, function(data){
                $scope.body = '';
                $scope.posts.unshift(data);
            });
        };

        $scope.delete = function(id){
            api.posts.delete({id: id}, function(){
                $scope.posts.splice($scope.utils.getPostIndex(id), 1);
            });
        };

        $scope.utils = {
            getPostIndex: function(id){
                return _.indexOf(
                    $scope.posts,
                    _.findWhere($scope.posts, {id: id})
                );
            }
        };
    });