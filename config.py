import getpass

username = getpass.getuser()

# Bisq directory to get the git commit hash
bisqHome = "/home/"+username+"/bisq/bisq/desktop/"

# Data directory where seednode keeps the json dumps
dataDir = "/home/"+username+"/.local/share/seed_BTC_TESTNET_p66zj5dzhccqhes3"
