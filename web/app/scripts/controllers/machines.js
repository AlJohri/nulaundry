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

  $scope.showRuns = true;

  function alert(msg) {
    $scope.err = msg;
    $timeout(function() {
      $scope.err = null;
    }, 5000);
  }

  Ref.child('machines').on('child_changed', function(snapshot) {
    var changed_machine = snapshot.val();
    $scope.last_change = changed_machine;
  });

  $scope._ = _;

});
