'use strict';

/**
 * @ngdoc function
 * @name webApp.controller:ItemsCtrl
 * @description
 * # MainCtrl
 * Controller of the webApp
 */
angular.module('webApp')
  .controller('ItemsCtrl', function ($scope, Ref, $firebaseArray) {

	$scope.items = $firebaseArray(Ref.child('items'));
	$scope.items.$loaded().catch(alert);

  function alert(msg) {
    $scope.err = msg;
    $timeout(function() {
      $scope.err = null;
    }, 5000);
  }

  });
