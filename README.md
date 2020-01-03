# BSQ Block Explorer

Follow these instructions to setup a [BSQ Block Explorer](https://explorer.bisq.network) using data from your [Bisq Seednode](https://github.com/bisq-network/bisq/tree/master/seednode). Keep in mind you need a dedicated seednode for the BSQ explorer, as the JSON data dump puts too much load on it to seed the network properly.

## Bisq Seednode

First, [setup your Bisq Seednode](https://github.com/bisq-network/bisq/tree/master/seednode#bisq-seed-node) so you have Tor, Bitcoin, and bisq-seednode running and fully synced. Then, enable BSQ data output on your Bisq Seednode with the following command

```bash
sudo sed -i -e 's!BISQ_DUMP_BLOCKCHAIN=false!BISQ_DUMP_BLOCKCHAIN=true!' /etc/default/bisq-seednode.env
sudo service bisq-seednode restart
```

It will take 10+ minutes before the seednode starts saving BSQ transaction data.

### Let's Encrypt

Next, request an SSL certificate for your server from Let's Encrypt using certbot-nginx

```bash
sudo apt-get update -q
sudo apt-get install -q -y nginx-core python-certbot-nginx
sudo certbot --nginx --agree-tos --non-interactive -m ssl@example.com -d explorer.example.com
```

After obtaining your SSL certificate, you should be able to see the default page at https://explorer.example.com/

### BSQ Indexer

Clone this repo to bisq user's homedir
```bash
curl -s https://raw.githubusercontent.com/bisq-network/bisq-explorer/master/install_bsq_explorer_debian.sh | sudo bash
```

### Nginx

Install the nginx.conf from this repository, substituting explorer.example.com for your server hostname
```bash
sudo wget -O /etc/nginx/nginx.conf https://raw.githubusercontent.com/bisq-network/bisq-explorer/master/nginx.conf
sudo sed -i -e '!__HOSTNAME__!explorer.example.com!g' /etc/nginx/nginx.conf
sudo service nginx restart
```

You should now be able to access your BSQ explorer at https://explorer.example.com/

### Tor onion (optional)

Add these lines to the bottom of /etc/tor/torrc
```
HiddenServiceDir /var/lib/tor/bsqexplorer/
HiddenServicePort 80 127.0.0.1:80
HiddenServiceVersion 2
```

Then restart Tor with the following command
```bash
sudo service tor restart
```

After Tor restarts, it will generate your onion hostname, get it by doing:

```bash
sudo cat /var/lib/tor/bsqexplorer/hostname
```

Then you can also access your BSQ explorer over Tor at http://foo.onion/
