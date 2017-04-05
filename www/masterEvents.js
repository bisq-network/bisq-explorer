/*
    Copyright Grazcoin 2017
    https://github.com/grazcoin/bisq-tools
*/

myApp.run(function($rootScope) {
    $rootScope.$on('handlePagesEmit', function(event, args) {
        $rootScope.$broadcast('handlePagesBroadcast', args);
    });
});
