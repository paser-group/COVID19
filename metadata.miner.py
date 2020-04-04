'''
Check data by looking into JSON files 
Akond Rahman 
Apr 03, 2020 
'''
import os 
import json 

def getJSONData(dir_):
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
                            print(repo_['full_name'])

if __name__=='__main__':
    json_dir = '/Users/arahman/Documents/OneDriveWingUp/OneDrive-TennesseeTechUniversity/Research/SciSoft/COVID19/dataset/'
    getJSONData(json_dir)