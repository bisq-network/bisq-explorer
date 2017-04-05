/*
    Copyright Grazcoin 2017
    https://github.com/grazcoin/bisq-tools
*/

function AdressController($scope, $http) {
    $scope.addressInformation = {};
    $scope.addressBalance = {};
    $scope.theAddress = "";
    $scope.footer = "FOOTER";
    $scope.title = "TITLE";
    
    $scope.createIconPopup = function () {
        $('.iconPopupInit').popover({ trigger: "hover" });           
    };

    $scope.paymentsReceivedSum = function () {
        var length = $scope.addressInformation.received_transactions.length;
        var sum = 0;
        for (var i = 0; i < length; i++) {
            sum += parseFloat($scope.addressInformation.received_transactions[i].amount);
        }
        return sum;
    }

    $scope.boughtViaExodusSum = function () {

        var length = $scope.addressInformation.genesis_transactions.length;
        var sum = 0;
        for (var i = 0; i < length; i++) {
            sum += parseFloat($scope.addressInformation.genesis_transactions[i].amount);

        }
        return sum;
    }
    $scope.paymentsSentSum = function () {
        var length = $scope.addressInformation.sent_transactions.length;
        var sum = 0;
        for (var i = 0; i < length; i++) {
            sum += parseFloat($scope.addressInformation.sent_transactions[i].amount);
        }
        return sum;
    }

    $scope.incomingTransCount = function () {
        var length = $scope.addressInformation.received_transactions.length;
        var sum = 0;
        for (var i = 0; i < length; i++) {
            sum++;

        }
        return sum;
    }

    $scope.outgoingTransCount = function () {
        var length = $scope.addressInformation.sent_transactions.length;
        var sum = 0;
        for (var i = 0; i < length; i++) {
            sum++;

        }
        return sum;
    }

    $scope.genesisTransCount = function () {
        var length = $scope.addressInformation.genesis_transactions.length;
        var sum = 0;
        for (var i = 0; i < length; i++) {
            sum++;

        }
        return sum;
    }

    $scope.getAddressData = function () {

        // parse addr from url parameters
	var myURLParams = BTCUtils.getQueryStringArgs();
	$scope.theAddress = myURLParams['addr'];
	if (!BTCUtils.isAddress($scope.theAddress)) {
		$scope.theAddress = "invalid";
	}
	$('#qrcode').qrcode({
		width: 130,
		height: 130,
		text: myURLParams['addr']
		});
       // Make the http request for address and process the result
       var file = 'addr/' + myURLParams['addr'] + '.json';	
       $http.get(file, {}).success(function (data, status, headers, config) {
           $scope.addressInformation = data;
           // get positive balances
           var balance = data['balance'];
           var length = balance.length;
           var j = 1;
           var url = BTCUtils.getUrl();
           for (var i = 0; i < length; i++) {
               if (balance[i].value != 0.0) {
                   balance[i].newUrl = BTCUtils.replaceCurrency(url, balance[i].symbol);
                   $scope.addressBalance[j]=balance[i];
                   j=j+1;
               }
           }
       });
    }
}
