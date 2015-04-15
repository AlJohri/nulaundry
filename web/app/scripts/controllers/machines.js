'use strict';

/**
 * @ngdoc function
 * @name webApp.controller:MachinesCtrl
 * @description
 * # MainCtrl
 * Controller of the webApp
 */
angular.module('webApp')
  .controller('MachinesCtrl', function ($scope, $window, Ref, $firebaseArray) {

  // $scope.$window.$scope = $scope;
  // console.log($scope.$eval('$window'));

	$scope.machines = $firebaseArray(Ref.child('machines'));
	$scope.machines.$loaded().catch(alert);

  $scope.locations = $firebaseArray(Ref.child('locations'));
  $scope.locations.$loaded().catch(alert);

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

  $scope.averageMachineTime = function(type) {

    var waitTimes = _.chain($scope.machines)
      .filter(function(machine) {return machine['type'] == type; })
      .map(function(machine) {return _.values(machine.runs); }).flatten(true)
      .map(function(run) {return run ? (run[1] - run[0])/1000/60 : undefined; })
      .compact()
      .value();

    return _.reduce(waitTimes, function(x,y) {return x+y; }, 0) / waitTimes.length;

  }

  $scope.averageLocationTime = function(location_name, type) {

    var waitTimes = _.chain($scope.machines)
      .filter(function(machine) {return machine['location_name'] == location_name; })
      .filter(function(machine) {return machine['type'] == type; })
      .map(function(machine) {return _.values(machine.runs); }).flatten(true)
      .map(function(run) {return run ? (run[1] - run[0])/1000/60 : undefined; })
      .compact()
      .value();

    return _.reduce(waitTimes, function(x,y) {return x+y; }, 0) / waitTimes.length;

  }

  $scope._ = _;

});
