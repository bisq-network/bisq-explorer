import getpass

username = getpass.getuser()

# Bisq directory to get the git commit hash
bisqHome = "/home/"+username+"/bisq/bisq/desktop/"

# Data directory where seednode keeps the json dumps
dataDir = "/home/"+username+"/.local/share/dao_test/seed_2002/btc_regtest/db/"
