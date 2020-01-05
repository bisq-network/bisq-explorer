# BSQ Explorer

Follow these instructions to setup a [BSQ Explorer](https://explorer.bisq.network) using data from your [Bisq Seednode](https://github.com/bisq-network/bisq/tree/master/seednode). Keep in mind you need a dedicated seednode for the BSQ explorer, as the JSON data dump puts too much load on it to seed the network properly.

## Bisq Seednode

First, [setup your Bisq Seednode](https://github.com/bisq-network/bisq/tree/master/seednode#bisq-seed-node) so you have Tor, Bitcoin, and bisq-seednode running and fully synced. Then, enable BSQ data output on your Bisq Seednode with the following command
```bash
sudo sed -i -e 's!BISQ_DUMP_BLOCKCHAIN=false!BISQ_DUMP_BLOCKCHAIN=true!' /etc/default/bisq-seednode.env
sudo service bisq-seednode restart
```

It will take a few minutes before the seednode starts saving BSQ transaction data.

## BSQ Explorer

Next, run the intallation script from this repo to install BSQ explorer as a systemd service
```bash
curl -s https://raw.githubusercontent.com/bisq-network/bisq-explorer/master/install_bsq_explorer_debian.sh | sudo bash
```
It will start the BSQ Explorer service and output the generated content as static HTML. You'll setup a webserver to serve this HTML in the next step.

### NGINX + Let's Encrypt

For the next step, you'll need to open ports 80 and 443 on your firewall for HTTP and HTTPS
```bash
sudo ufw allow 80/tcp
sudo ufw allow 443/tcp
```

Request an SSL certificate for your server's hostname using certbot
```bash
sudo certbot --nginx --agree-tos --non-interactive -m ssl@example.com -d explorer.example.com
```

After you successfully obtain the SSL certificate, install the nginx.conf from this repo, and substite explorer.example.com with your server hostname
```bash
sudo wget -O /etc/nginx/nginx.conf https://raw.githubusercontent.com/bisq-network/bisq-explorer/master/nginx.conf
sudo sed -i -e 's!__HOSTNAME__!explorer.example.com!g' /etc/nginx/nginx.conf
sudo service nginx restart
```

Now you should be able to access your BSQ explorer at https://explorer.example.com/

### Tor onion (optional)

Add these lines to the bottom of /etc/tor/torrc
```
HiddenServiceDir /var/lib/tor/bsqexplorer/
HiddenServicePort 81 127.0.0.1:81
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

Then you'll also be able to access your BSQ explorer over Tor at http://foo.onion/
