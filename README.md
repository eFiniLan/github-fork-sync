github-fork-sync
------
A small python script to sync all forked repos, it uses github api with Basic Authentication.

# get all repositories from owned account
# get all forked repositories
# for every forked repositories, find their parent repositories and branches
# check parent branches refs heads SHA against owned one, update them if mis-match

This script was last tested on **2019/06/20**

```bash
git clone https://github.com/efiniLan/github-fork-sync.git
sudo apt-get install python-pip
sudo pip install requests
python github-fork-sync <github_username> <github_password>
```
