'use strict';
/**
 * @ngdoc overview
 * @name webApp:routes
 * @description
 * # routes.js
 *
 * Configure routes for use with Angular, and apply authentication security
 */
angular.module('webApp')

  .config(['$routeProvider', function($routeProvider) {
    $routeProvider
      .when('/', {
        templateUrl: 'views/machines.html',
        controller: 'MachinesCtrl'
      })

      // .when('/status', {
      //   templateUrl: 'views/status.html',
      //   controller: 'StatusCtrl'
      // })
      .otherwise({redirectTo: '/'});
  }]);
