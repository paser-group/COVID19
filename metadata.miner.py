'''
Check data by looking into JSON files 
Akond Rahman 
Apr 03, 2020 
'''
import os 
import json 
import pandas as pd

def getJSONData(dir_):
    allContent = []
    tracker = []
    for root_, dirnames, filenames in os.walk(dir_):
        for file_ in filenames:
            full_path_file = os.path.join(root_, file_) 
            if(full_path_file.endswith('.json')):    
                # print(full_path_file) 
                with open(full_path_file) as jsonfile:
                    json_content = json.load(jsonfile)
                    if 'items' in json_content:
                        repo_details = json_content['items']
                        for repo_ in repo_details:
                            url_     = repo_['html_url']
                            fork     = repo_['fork']
                            watchers = repo_['watchers_count']
                            lang     = repo_['language']
                            issues   = repo_['open_issues']
                            private  = repo_['private']
                            date_    = repo_['created_at']
                            name     = repo_['full_name']
                            if name not in tracker:
                                allContent.append( (name, url_, fork, watchers, lang, issues, private, date_) )
                                tracker.append(name) 
    df_ = pd.DataFrame(allContent)
    df_.to_csv('ALL_REPOS.csv', index=False, encoding='utf-8') 

    




if __name__=='__main__':
    json_dir = '/Users/arahman/Documents/OneDriveWingUp/OneDrive-TennesseeTechUniversity/Research/SciSoft/COVID19/dataset/'
    getJSONData(json_dir)