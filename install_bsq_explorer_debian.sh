#!/usr/bin/env bash
set -e

echo "[*] Bisq Explorer installation script"

##### change as necessary for your system

SYSTEMD_SERVICE_HOME=/etc/systemd/system
SYSTEMD_ENV_HOME=/etc/default

ROOT_USER=root
ROOT_GROUP=root
ROOT_HOME=~root

BISQ_USER=bisq
BISQ_HOME=~bisq


EXPLORER_REPO_URL=https://github.com/bisq-network/bisq-explorer
EXPLORER_REPO_NAME=bisq-explorer
EXPLORER_REPO_TAG=master

EXPLORER_DEBIAN_PKG="python3-pip inotify-tools rsync nginx-core python-certbot-nginx tor"
EXPLORER_PYTHON_PKG="simplejson gitpython"
EXPLORER_BIN_PATH="/usr/local/bin"

EXPLORER_HIDDENSVC=bsqexplorer

NGINX_CONFIGURATION=/etc/nginx/nginx.conf
TOR_CONFIGURATION=/etc/tor/torrc
TOR_RESOURCES=/var/lib/tor

#####

echo "[*] Cloning BSQ Explorer repo"
sudo -H -i -u "${BISQ_USER}" git config --global advice.detachedHead false
sudo -H -i -u "${BISQ_USER}" git clone --branch "${EXPLORER_REPO_TAG}" "${EXPLORER_REPO_URL}" "${BISQ_HOME}/${EXPLORER_REPO_NAME}"

echo "[*] Installing BSQ Explorer debian packages"
sudo -H -i -u "${ROOT_USER}" DEBIAN_FRONTEND=noninteractive apt-get update -q
sudo -H -i -u "${ROOT_USER}" DEBIAN_FRONTEND=noninteractive apt-get install -qq -y ${EXPLORER_DEBIAN_PKG}

echo "[*] Installing BSQ Explorer python packages"
sudo python3 -m pip install ${EXPLORER_PYTHON_PKG}

echo "[*] Adding Nginx configuration"
sudo -H -i -u "${ROOT_USER}" install -c -o "${ROOT_USER}" -g "${ROOT_GROUP}" -m 644 "${BISQ_HOME}/${EXPLORER_REPO_NAME}/nginx.conf" "${NGINX_CONFIGURATION}"

echo "[*] Adding Tor configuration"
if ! grep bsqexplorer /etc/tor/torrc >/dev/null 2>&1;then
  sudo -H -i -u "${ROOT_USER}" /bin/sh -c "echo HiddenServiceDir ${TOR_RESOURCES}/${EXPLORER_HIDDENSVC}/ >> ${TOR_CONFIGURATION}"
  sudo -H -i -u "${ROOT_USER}" /bin/sh -c "echo HiddenServicePort 81 >> ${TOR_CONFIGURATION}"
  sudo -H -i -u "${ROOT_USER}" /bin/sh -c "echo HiddenServiceVersion 3 >> ${TOR_CONFIGURATION}"
fi

echo "[*] Restarting Tor"
sudo -H -i -u "${ROOT_USER}" service tor restart

echo "[*] Installing BSQ Explorer scripts"
for script in bsq-index bsq-explorer;do
    sudo -H -i -u "${ROOT_USER}" install -c -o "${ROOT_USER}" -g "${ROOT_GROUP}" -m 755 "${BISQ_HOME}/${EXPLORER_REPO_NAME}/${script}" "${EXPLORER_BIN_PATH}"
done

echo "[*] Installing BSQ Explorer systemd service"
sudo -H -i -u "${ROOT_USER}" install -c -o "${ROOT_USER}" -g "${ROOT_GROUP}" -m 644 "${BISQ_HOME}/${EXPLORER_REPO_NAME}/bsq-explorer.service" "${SYSTEMD_SERVICE_HOME}"

echo "[*] Reloading systemd daemon configuration"
sudo -H -i -u "${ROOT_USER}" systemctl daemon-reload

echo "[*] Enabling BSQ Explorer service"
sudo -H -i -u "${ROOT_USER}" systemctl enable bsq-explorer.service

echo "[*] Starting BSQ Explorer service"
sudo -H -i -u "${ROOT_USER}" systemctl start bsq-explorer.service
sleep 5
sudo -H -i -u "${ROOT_USER}" journalctl --no-pager --unit bsq-explorer

echo '[*] Done!'
echo -n '[*] Access your BSQ explorer at http://'
cat "${TOR_RESOURCES}/${EXPLORER_HIDDENSVC}/hostname"

exit 0
