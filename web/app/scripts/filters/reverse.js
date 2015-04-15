'use strict';

angular.module('webApp')
  .filter('reverse', function() {
    return function(items) {
      return angular.isArray(items)? items.slice().reverse() : [];
    };
  });


angular.module('webApp')
	.filter('total', ['$parse', function ($parse) {
    return function (input, property) {
        var i = input instanceof Array ? input.length : 0,
            p = $parse(property);

        if (typeof property === 'undefined' || i === 0) {
            return i;
        } else if (isNaN(p(input[0]))) {
            throw 'filter total can count only numeric values';
        } else {
            var total = 0;
            while (i--)
                total += p(input[i]);
            return total;
        }
    };
}]);