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
It will start the BSQ Explorer service and serve the generated content as static HTML on a Tor hiddenservice onion hostname.
```
[*] Done!
[*] Your BSQ Explorer hostname: http://qwertyuiop.onion
```

### Let's Encrypt (optional)

If you also want to serve BSQ explorer on clearnet, you'll need to open ports 80 and 443 on your firewall for HTTP and HTTPS
```bash
sudo ufw allow 80/tcp
sudo ufw allow 443/tcp
```

Request an SSL certificate for your server's hostname using certbot
```bash
sudo certbot --nginx -d explorer.example.com
```

Now you should be able to access your BSQ explorer at https://explorer.example.com/
