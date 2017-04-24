/*
    Copyright Grazcoin 2017
    https://github.com/grazcoin/bisq-tools
*/

$(document).ready(function () {

    var myURLParams = BTCUtils.getQueryStringArgs();
    console.log(myURLParams);


    var tx = myURLParams['tx'];
    var url = '';
    if (tx.length < 63)
    {
        var addr = tx;
        if (addr[0]=='B') { // drop the B of BSQ
            addr = tx.substring(1,tx.length);
        }
	var file = 'addr/' + addr + '.json';
        $.getJSON( file, function( data ) {
        	console.log("ok");
		url = "Address.html?addr=" + addr;
	    	window.location = url;
        }).fail(function() {
		console.log( "error" );
		$('#errorAddressModal').modal('show');
	});
    
    	return;
    }


    //Ajax call so I can see transactionType from JSON
    url = 'tx/' + tx + '.json';
    $.ajax({
	url: url,
	type: 'get',
	success: function (data) {
	    //successfull callback, forward user to original_url
	    //  window.location = url;
	    var url = "";

	    var response = data;
            console.log('DEBUG-DEBUG-DEBUG start a');
	    console.log(response);
            console.log('DEBUG-DEBUG-DEBUG start b');
	    console.log(response.txVersion);
            console.log('DEBUG-DEBUG-DEBUG start c');
	    if (response.txVersion == "1") {
		//it is tx
		url += "tx.html?tx=";
	    }
            url += tx;
	    console.log(url);
            console.log('DEBUG-DEBUG-DEBUG end');
	    window.location = url;
	},
	error: function () {
	    console.log('Error');
	    $('#errorTransactionModal').modal('show');
	}
    });
});
