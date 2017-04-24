/*
    Copyright Grazcoin 2017
    https://github.com/grazcoin/bisq-tools
*/

function BTCUtils() {
}

///// Public Methods

BTCUtils.getUrl = function () {
        var url = new String(location);
        return url;
}

BTCUtils.getQueryStringArgs = function () {
	//get query string without the initial ?
	var qs = (location.search.length > 0 ? location.search.substring(1) : ""),
		//object to hold data
		args = {},
		//get individual items
		items = qs.length ? qs.split("&") : [],
		item = null,
		name = null,
		value = null,
		//used in for loop
		i = 0,
		len = items.length;
	//fill defaults
	args['title']='BSQ data'
	args['tx']='sample_tx'
	args['addr']='sample_addr'
	args['currency']='BSQ'
	args['page']='0000'
	//assign each item onto the args object
	for (i=0; i < len; i++){
		item = items[i].split("=");
		name = encodeURIComponent(item[0]);
		value = encodeURIComponent(item[1]);
		if (name.length) {
			args[name] = value;
		}
	}
	return args;
}

BTCUtils.isAddress = function(adr) {
    var re = /^[123mn][1-9A-HJ-NP-Za-km-z]{26,35}/;
    return re.test(adr);
}

BTCUtils.isBAddress = function(adr) {
    var re = /^[B][1-9A-HJ-NP-Za-km-z]{26,36}/;
    return re.test(adr);
}




BTCUtils.isTxId = function(txid) {
    var re = /^[0-9a-fA-F]{64}$/;
    return re.test(txid);
}

BTCUtils.isCurrencySymbol = function(currency) {
    var re = /^[A-ZJa-z]{3,10}$/;
    return re.test(currency);
}

BTCUtils.isFilter = function(filter) {
    var re = /^[A-ZJa-z]{3,10}$/;
    return re.test(filter);
}

BTCUtils.replaceCurrency = function(url, c) {
    var oldUrl;
    var newUrl;

    oldUrl = url.replace(/\/+$/, "");
    if (url.search("currency=") == -1)
        {
        if (url.search("\\?") == -1)
            {
            newUrl = oldUrl.concat("?currency="+c);
            }
        else
            {
            newUrl = oldUrl.concat("&currency="+c);
            }
        }
    else
        {
        newUrl = oldUrl.replace(/(currency=).*(&)?/,'$1' + c + '$2');
        }
    //console.log(newUrl);
    return newUrl;
}
