/*
    Copyright Grazcoin 2017
    https://github.com/grazcoin/bisq-tools
*/

function PropertiesController($scope, $http) {
    $scope.properties = {};
    $scope.footer = "FOOTER";
    $scope.title = "TITLE";
    
    $scope.createIconPopup = function () {
        $('.iconPopupInit').popover({ trigger: "hover" });           
    };


    $scope.getPropertiesData = function () {

        // Make the http request for extracted_currencies and process the result
	var properties_file = 'general/stats.json';	
        $http.get(properties_file, {}).success(function (properties_data, status, headers, config) {
            $scope.properties = properties_data;
            console.log($scope.properties[0]);
            var properties_list = properties_data[0];

        });
    }
}
