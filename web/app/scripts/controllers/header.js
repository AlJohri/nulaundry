'use strict';

/**
 * @ngdoc function
 * @name webApp.controller:HeaderCtrl
 * @description
 * # MainCtrl
 * Controller of the webApp
 */
angular.module('webApp')
  .controller('HeaderCtrl', function ($scope, $location) {

    $scope.isActive = function (viewLocation) {
        return viewLocation === $location.path();
    };

  });


