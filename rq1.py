'''
Akond Rahman 
May 04, 2020 
Answer to RQ1 
'''
import os 
import csv 
import pandas as pd 
import numpy as np 
from git import Repo
from git import exc 
import subprocess

def getDevEmailForCommit(repo_path_param, hash_):
    author_emails = []

    cdCommand     = "cd " + repo_path_param + " ; "
    commitCountCmd= " git log --format='%ae'" + hash_ + "^!"
    command2Run   = cdCommand + commitCountCmd

    author_emails = str(subprocess.check_output(['bash','-c', command2Run]))
    author_emails = author_emails.split('\n')
    author_emails = [x_.replace(hash_, '') for x_ in author_emails if x_ != '\n' and '@' in x_ ] 
    author_emails = [x_.replace('^', '') for x_ in author_emails if x_ != '\n' and '@' in x_ ] 
    author_emails = [x_.replace('!', '') for x_ in author_emails if x_ != '\n' and '@' in x_ ] 
    author_emails = [x_.replace('\\n', ',') for x_ in author_emails if x_ != '\n' and '@' in x_ ] 
    try:
        author_emails = author_emails[0].split(',')
        author_emails = [x_ for x_ in author_emails if len(x_) > 3 ] 
        author_emails = list(np.unique(author_emails) )
    except IndexError as e_:
        pass
    return author_emails  

def getDevEmails(full_path_to_repo, branchName='master'):
    repo_emails = []
    all_commits = []
    repo_emails = []
    if os.path.exists(full_path_to_repo):
        repo_  = Repo(full_path_to_repo)
        try:
           all_commits = list(repo_.iter_commits(branchName))   
        except exc.GitCommandError:
           print('Skipping this repo ... due to branch name problem', full_path_to_repo )
        for commit_ in all_commits:
                commit_hash = commit_.hexsha

                emails = getDevEmailForCommit(full_path_to_repo, commit_hash)
                repo_emails = repo_emails + emails

    else:
        repo_emails = [ str(x_) for x_ in range(10) ]
    
    repo_emails = np.unique( repo_emails )
    return len(repo_emails) , len(all_commits) 

def mergeDataFrames(meta_df, loc_df):
    full_list = []
    repo_dirs  = np.unique(  loc_df['REPO'].tolist() )
    for repo_dir in repo_dirs:
        # part#1 
        repo_df    = loc_df[loc_df['REPO']==repo_dir] 
        repo_files = repo_df['FILES'].tolist()[0] 
        repo_devs , repo_commits    = getDevEmails(repo_dir)  

        # part#2 
        repo_tmp_name = repo_dir.split('/')[-1]
        repo_name     = repo_tmp_name.split('@')[-1] +  '/' +  repo_tmp_name.split('@')[0]
        repo_link     = 'https://github.com/' + repo_name
        repo_meta_df  = meta_df[meta_df['NAME']==repo_name]
        repo_releases = repo_meta_df['RELEASES'].tolist()[0]  	
        repo_watchers = repo_meta_df['WATCHERS'].tolist()[0]  				
        repo_issues   = repo_meta_df['ISSUES'].tolist()[0]  	    
        repo_lang     = repo_meta_df['LANG'].tolist()[0]  				
        repo_date     = repo_meta_df['DATE'].tolist()[0]  				        

        repo_tuple = (repo_dir, repo_devs, repo_commits, repo_files, repo_name, repo_link, repo_releases, repo_watchers, repo_issues, repo_lang, repo_date)
        print(repo_tuple)   

        full_list.append( repo_tuple )
    df_ = pd.DataFrame(full_list)

    return df_ 

def ans2rq1(file_name, issue_file_name): 
    full_df = pd.read_csv(file_name) 
    repo_categs = np.unique( full_df['CATEGORY'].tolist()  )
    issue_df = pd.read_csv(issue_file_name) 
    for repo_cat in repo_categs:
        repo_cat_df        = full_df[full_df['CATEGORY']==repo_cat] 
        per_categ_repos    = np.unique( repo_cat_df['REPO_DIR'].tolist() ) 
        categ_wise_repos   = len ( per_categ_repos )
        categ_wise_devs    = sum( repo_cat_df['DEVS'].tolist() ) 
        categ_wise_commits = sum( repo_cat_df['COMMITS'].tolist() )
        categ_wise_files   = sum( repo_cat_df['FILES'].tolist() ) 
        categ_wise_releases= sum( repo_cat_df['RELEASES'].tolist() ) 
        categ_wise_langs   = np.unique( repo_cat_df['LANG'].tolist() ) 
        print('CATEG:{}, REPOS:{}, DEVS:{}, COMMITS:{}, FILES:{}, RELEASES:{}, LANGS:{}'.format(repo_cat, categ_wise_repos, categ_wise_devs, categ_wise_commits, categ_wise_files, categ_wise_releases, categ_wise_langs) )
        print('*'*50)
        per_categ_issues = [] 
        for repo_ in per_categ_repos:
            repo_dir         = repo_.split('/')[-1] 
            per_categ_repo_issues_df = issue_df[issue_df['REPO']==repo_dir]
            per_categ_repo_issues    = list( np.unique( per_categ_repo_issues_df['URL'].tolist() ) )
            per_categ_issues         = per_categ_issues + per_categ_repo_issues 
        print('CATEG:{}, ISSUES:{}'.format( repo_cat, len(per_categ_issues) ) )
        print('*'*50)
        






                			
if __name__=='__main__':
   meta_file      = '/Users/arahman/Documents/OneDriveWingUp/OneDrive-TennesseeTechUniversity/Research/SciSoft/COVID19/results/META_REPOS.csv'
   local_file     = '/Users/arahman/Documents/OneDriveWingUp/OneDrive-TennesseeTechUniversity/Research/SciSoft/COVID19/results/LOCAL_REPOS.csv'
   summ_repo_file = '/Users/arahman/Documents/OneDriveWingUp/OneDrive-TennesseeTechUniversity/Research/SciSoft/COVID19/results/SUMMARY_REPOS.csv'

#    meta_df  = pd.read_csv(meta_file) 
#    local_df = pd.read_csv(local_file) 
#    full_df  = mergeDataFrames(meta_df, local_df)
#    full_df.to_csv(summ_repo_file, index=False, header=['REPO_DIR', 'DEVS', 'COMMITS', 'FILES' , 'NAME', 'LINK', 'RELEASES', 'WATCHERS', 'ISSUES', 'LANG', 'DATE']  , encoding='utf-8')                
   
   
   repo_categ_file = '/Users/arahman/Documents/OneDriveWingUp/OneDrive-TennesseeTechUniversity/Research/SciSoft/COVID19/dataset/FINAL_REPO_CATEGS.csv'
   issue_file      = '/Users/arahman/Documents/OneDriveWingUp/OneDrive-TennesseeTechUniversity/Research/SciSoft/COVID19/dataset/ALL_REPOS_ONLY_ISSUES.csv'
   ans2rq1(repo_categ_file, issue_file)

