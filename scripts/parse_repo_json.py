import sys
import json




repo_json = json.loads(str(sys.stdin.readline()))

out_string = ''
for repo in repo_json['data']:
    if repo['type'] == 'project':
        repo_name = repo['id'].replace(' ','')
        out_string += repo_name+' '

print (out_string)


