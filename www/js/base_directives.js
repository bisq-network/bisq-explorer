
myApp.directive('popover', function() {
   return function(scope, elem) {
      elem.popover();
   };
});


myApp.directive('setAddress', function() {
   return {
      restrict: 'E',
      templateUrl: 'templates/setAddress.html'
   };
});
myApp.directive('afterResponse', function() {
   return {
      restrict: 'E',
      templateUrl: 'templates/afterResponse.html'
   };
});
myApp.directive('sendPart', function() {
   return {
      restrict: 'E',
      templateUrl: 'templates/sendPart.html'
   };
});
myApp.directive('privateKeyError', function() {
   return {
      restrict: 'E',
      templateUrl: 'templates/privateKeyError.html'
   };
});
