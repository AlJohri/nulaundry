'use strict';

/**
 * @ngdoc function
 * @name webApp.controller:MachinesCtrl
 * @description
 * # MainCtrl
 * Controller of the webApp
 */
angular.module('webApp')
  .controller('MachinesCtrl', function ($scope, Ref, $firebaseArray) {

	$scope.machines = $firebaseArray(Ref.child('machines'));
	$scope.machines.$loaded().catch(alert);

  function alert(msg) {
    $scope.err = msg;
    $timeout(function() {
      $scope.err = null;
    }, 5000);
  }

  });
