import sys
import requests

#e.g. python github-fork-sync.py github-username github-password
auth = (sys.argv[1], sys.argv[2])

# make sure user/pass is correct
resp_json = requests.get('https://api.github.com/user', auth=auth).json()
try:
    message = resp_json["message"]
    sys.exit("Credential check failed: %s" % message)
except KeyError as e:
    print("Credential check passed")

# find all the repos
repo_list_json = requests.get(resp_json["repos_url"], auth=auth).json()
for repo in repo_list_json:
    # repo is forked
    if repo["fork"] is True:
        repo_url = repo["url"]
        # get forked url
        repo_json = requests.get(repo_url, auth=auth).json()
        forked_url = repo_json["parent"]["url"]
        # get all forked repo branches
        branch_list_json = requests.get(forked_url + "/branches", auth=auth).json()
        for branch in branch_list_json:
            branch_name = branch["name"]
            # get forked/owned refs heads info
            ref_head = "/git/refs/heads/" + branch_name
            from_ref_head_url = forked_url + ref_head
            to_ref_head_url = repo_url + ref_head
            from_resp_json = requests.get(from_ref_head_url, auth=auth).json()
            to_resp_json = requests.get(to_ref_head_url, auth=auth).json()
            try:
                message = to_resp_json["message"]
                print("%s does not exist in your %s" % (branch_name, repo["full_name"]))
            except KeyError as e:
                # compare refs heads info
                print("Comparing %s:%s with %s:%s" % (repo_json["parent"]["full_name"], branch_name, repo["full_name"], branch_name))
                if from_resp_json["object"]["sha"] == to_resp_json["object"]["sha"]:
                    print("sha matched: %s" % from_resp_json["object"]["sha"])
                else:
                    print("sha mismatched: %s vs %s" % (from_resp_json["object"]["sha"], to_resp_json["object"]["sha"]))
                    # mismatched, try to patch owned branch refs heads sha to forked one
                    patched_json = requests.patch(to_ref_head_url, '{"sha": "%s", "force": true}' % from_resp_json["object"]["sha"], auth=auth).json()
                    # validate again
                    if patched_json["object"]["sha"] == from_resp_json["object"]["sha"]:
                        print("Update successful")
                    else:
                        print("Update failed")
