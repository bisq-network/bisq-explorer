/*
    Copyright Grazcoin 2017
    https://github.com/grazcoin/bisq-tools
*/

function TransactionController($scope, $http) {
    $scope.transactionInformation;
    $scope.footer = "FOOTER";
    $scope.title = "TITLE";
    $scope.reason = "unknown";

    $scope.createIconPopup = function () {
        $('.iconPopupInit').popover({ trigger: "hover" });           
    };

    //Function for creating popup
    $scope.makePopup = function () {
	//Popup for valid/invalid 
	$('#validPopup').popover({ trigger: "hover" });
	var navHeight = $('.navbar').height();
	$('.page-container').css('paddingTop', navHeight + 20);
    };
    
    $scope.getTransactionData = function () {

        // parse txo from url parameters
        var myURLParams = BTCUtils.getQueryStringArgs();
        var file = 'txo/' + myURLParams['txo'] + '.json';
        // Make the http request and process the result
        $http.get(file, {}).success(function (data, status, headers, config) {
            $scope.transactionInformation = data;
	    $scope.transactionInformation.txo_url_param = myURLParams['txo'].replace("%3A",":");
            $scope.setDefaults();
            $scope.updateReason();
        });
    }
    
    $scope.setDefaults = function() {
        if ($scope.transactionInformation.isVerified == true) {
                $scope.transactionInformation.invalid = false;
        } else {
                $scope.transactionInformation.invalid = true;
        }

        if ($scope.transactionInformation.txType == "GENESIS") {
                $scope.transactionInformation.icon = "genesis";
                $scope.transactionInformation.color = "bgc-new";
        } else {
               if ($scope.transactionInformation.txType == "TRANSFER_BSQ") {
                    $scope.transactionInformation.icon = "simplesend";
                    $scope.transactionInformation.color = "bgc-new";
               } else {
                    $scope.transactionInformation.icon = "simplesend";
                    $scope.transactionInformation.color = "bgc-default";
               }
        }
    }
    
    $scope.updateReason = function () {
    	if (!angular.isArray($scope.transactionInformation.invalid)) return;
    	if ($scope.transactionInformation.invalid.length < 2) return;
    	$scope.reason = $scope.transactionInformation.invalid[1];
    }
}
