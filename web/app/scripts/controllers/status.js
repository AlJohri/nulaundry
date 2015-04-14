'use strict';

/**
 * @ngdoc function
 * @name webApp.controller:StatusCtrl
 * @description
 * # MainCtrl
 * Controller of the webApp
 */
angular.module('webApp')
  .controller('StatusCtrl', function ($scope, Ref, $firebaseArray) {

	$scope.status = $firebaseArray(Ref.child('status').orderByChild("timestamp").limitToLast(200));
	$scope.status.$loaded().catch(alert);

  function alert(msg) {
    $scope.err = msg;
    $timeout(function() {
      $scope.err = null;
    }, 5000);
  }

  });
