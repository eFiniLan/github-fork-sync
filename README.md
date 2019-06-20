github-fork-sync
------
A small python script to sync all forked repos, it uses github api with Basic Authentication:

1. get all repositories from owned account
2. get all forked repositories
3. for every forked repositories, find their parent repositories and branches
4. check parent branches refs heads SHA against owned one, update them if mis-match


This script was last tested on **2019/06/20**


```bash
git clone https://github.com/efiniLan/github-fork-sync.git
cd github-fork-sync
sudo apt-get install python-pip
sudo pip install requests
python github-fork-sync <github_username> <github_password>
```
