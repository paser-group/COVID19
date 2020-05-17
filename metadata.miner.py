'''
Check data by looking into JSON files 
Akond Rahman 
Apr 03, 2020 
'''
import os 
import json 
import pandas as pd
import csv 
import subprocess
import numpy as np
import shutil
from git import Repo
from git import exc 
import time 
from datetime import datetime
import markdown
from bs4 import BeautifulSoup

def giveTimeStamp():
  tsObj = time.time()
  strToret = datetime.fromtimestamp(tsObj).strftime('%Y-%m-%d %H:%M:%S')
  return strToret

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
    df_.to_csv('ALL_REPOS.csv', index=False, header=['NAME', 'URL' , 'FORK_FLAG', 'WATCHERS', 'LANG', 'ISSUES', 'PRIVATE', 'DATE']  , encoding='utf-8') 

def cloneRepo(repo_name, target_dir):
    cmd_ = "git clone " + repo_name + " " + target_dir 
    try:
       subprocess.check_output(['bash','-c', cmd_])    
    except subprocess.CalledProcessError:
       print('Skipping this repo ... trouble cloning repo:', repo_name )

def dumpContentIntoFile(strP, fileP):
    fileToWrite = open( fileP, 'w')
    fileToWrite.write(strP )
    fileToWrite.close()
    return str(os.stat(fileP).st_size)

def deleteRepo(dirName, type_):
    print(':::' + type_ + ':::Deleting ', dirName)
    try:
        if os.path.exists(dirName):
            shutil.rmtree(dirName)
    except OSError:
        print('Failed deleting, will try manually')             


def getDevCount(full_path_to_repo, branchName='master', explore=1000):
    repo_emails = []
    all_commits = []
    repo_emails = []
    if os.path.exists(full_path_to_repo):
        repo_  = Repo(full_path_to_repo)
        try:
           all_commits = list(repo_.iter_commits(branchName))   
        except exc.GitCommandError:
           print('Skipping this repo ... due to branch name problem', full_path_to_repo )
        if len( all_commits ) < explore:
            for commit_ in all_commits:
                commit_hash = commit_.hexsha
                emails = getDevEmailForCommit(full_path_to_repo, commit_hash)
                repo_emails = repo_emails + emails
        else:
            repo_emails = [ str(x_) for x_ in range(10) ]
    return len(repo_emails) 


def cloneRepos(repo_list): 
    counter = 0     
    str_ = ''
    for repo_ in repo_list: 
            counter += 1 
            print('Cloning ', repo_ )
            dirName = '/Users/arahman/COVID19_REPOS/' + repo_.split('/')[-1] + '@' + repo_.split('/')[-2] ## '/' at the end messes up the index 
            cloneRepo(repo_, dirName )
            ### get file count 
            all_fil_cnt = sum([len(files) for r_, d_, files in os.walk(dirName)])
            if (all_fil_cnt <= 0):
               deleteRepo(dirName, 'NO_FILES')
            else:  
                dev_count = getDevCount(dirName)             
            str_ = str_ + str(counter) + ',' +  repo_ + ',' + dirName + ',' + ','  + str(dev_count) + ',' + '\n'



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

def days_between(d1_, d2_): ## pass in date time objects, if string see commented code 
    # d1_ = datetime.strptime(d1_, "%Y-%m-%d")
    # d2_ = datetime.strptime(d2_, "%Y-%m-%d")
    return abs((d2_ - d1_).days)


def getDevDayCount(full_path_to_repo, branchName='master', explore=1000):
    repo_emails = []
    all_commits = []
    repo_emails = []
    all_time_list = []
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

                timestamp_commit = commit_.committed_datetime
                str_time_commit  = timestamp_commit.strftime('%Y-%m-%d') ## date with time 
                all_time_list.append( str_time_commit )

    else:
        repo_emails = [ str(x_) for x_ in range(10) ]
    all_day_list   = [datetime(int(x_.split('-')[0]), int(x_.split('-')[1]), int(x_.split('-')[2]), 12, 30) for x_ in all_time_list]
    all_day_list   = all_day_list + [datetime(2020, 4, 4, 12, 30)]
    min_day        = min(all_day_list) 
    max_day        = max(all_day_list) 
    ds_life_days   = days_between(min_day, max_day)
    ds_life_months = round(float(ds_life_days)/float(30), 5)
    
    return len(repo_emails) , len(all_commits) , ds_life_days, ds_life_months     

def performFurtherChecks(root_dir_path):
    list_subfolders_with_paths = [f.path for f in os.scandir(root_dir_path) if f.is_dir()]
    all_list = []
    count    = 0 
    for dirName in list_subfolders_with_paths:
        count += 1
        print(dirName)  
        dev_count, all_file_count = 0 , 0 
        all_file_count                                 = sum([len(files) for r_, d_, files in os.walk(dirName)]) 
        dev_count, commit_count, age_days, age_months  = getDevDayCount(dirName)
        tup = ( count,  dirName, dev_count, all_file_count, commit_count, age_months)
        print('*'*10)
        all_list.append( tup ) 
    df_ = pd.DataFrame( all_list ) 
    df_.to_csv('COVID19_BREAKDOWN.csv', header=['INDEX', 'REPO', 'DEVS', 'FILES', 'COMMITS', 'AGE_MONTHS'] , index=False, encoding='utf-8')    

def preProcess(txt_, replace_char): 
    if(type(txt_) == str):
        txt_ = txt_.replace('\n', replace_char)
        txt_ = txt_.replace('\r', replace_char)
        txt_ = txt_.replace(',',  replace_char)    
        txt_ = txt_.replace('\t', replace_char)
        txt_ = txt_.replace('&',  replace_char)  
        txt_ = txt_.replace('#',  replace_char)
        txt_ = txt_.replace('=',  replace_char)  
        txt_ = txt_.replace('-',  replace_char)  
        txt_ = txt_.lower()
    else:
        txt_ = 'NOT_FOUND'
    return txt_ 

def getIssueDataFrame(repo_name_file, json_dir, out_file): 
    repo_df   = pd.read_csv(repo_name_file) 
    repo_dirs = np.unique(repo_df['REPO'].tolist()  )
    repos     = [x_.split('/')[-1] for x_ in repo_dirs]
    # print(repos) 
    repos      = [(x_, json_dir  +  x_.split('@')[-1] + '_' + x_.split('@')[0] + '.json' ) for x_ in repos]
    allContent = []
    for repo_ in repos:
        repo_dir, json_file = repo_ 
        github_name = repo_dir.split('@')[-1] + '/' + repo_dir.split('@')[0]
        if os.path.exists(json_file):
            # print(json_file) 
            with open(json_file) as jsonfile:
                json_content = json.load(jsonfile)
                if (len(json_content) > 95 ):
                    print(github_name) 
                # print(json_content) 
                for issue_content in json_content:
                    url_        = issue_content['url']
                    title       = issue_content['title'] 
                    title       = preProcess(title, ' ')
                    create_date = issue_content['created_at']
                    close_date  = issue_content['closed_at']
                    comment_cnt = issue_content['comments']
                    body_       = issue_content['body']
                    body_       = preProcess(body_, ' ')
                    label_list  = issue_content['labels']
                    if len(label_list) > 0:
                        for label_ in label_list:
                            label_name = label_['name']
                            label_name = preProcess(label_name, ' ')                        
                            label_desc = label_['description']
                            label_desc = preProcess(label_desc, ' ')  
                            the_tup = ( repo_dir, json_file, url_, title, create_date, close_date, comment_cnt, body_, label_name, label_desc )
                            allContent.append( the_tup )
                    else:
                        label_name, label_desc = 'NOT_FOUND', 'NOT_FOUND'
                        the_tup = ( repo_dir, json_file, url_, title, create_date, close_date, comment_cnt, body_, label_name, label_desc )
                        allContent.append( the_tup )
    df_ = pd.DataFrame(allContent)
    df_.to_csv(out_file, index=False, header=['REPO', 'JSON', 'URL' , 'TITLE', 'CREATE', 'CLOSED', 'COMMENT', 'BODY', 'LABEL_NAME', 'LABEL_DESC']  , encoding='utf-8')             

def getREADME(csv_file, dir_):
    df_ = pd.read_csv(csv_file) 
    repo_dirs = np.unique( df_['REPO'].tolist() )
    for repo_ in repo_dirs:
        full_repo_path = dir_ + repo_ 
        if (os.path.exists( full_repo_path ) ):
            for root_, dirnames, filenames in os.walk(full_repo_path):
                for file_ in filenames:
                    full_path_file = os.path.join(root_, file_) 
                    if(full_path_file.endswith('.md')  and ('README'  in full_path_file)):   
                        print('='*100)             
                        print('*'*50)
                        print(repo_ + ':::::::::::')
                        print('*'*50)
                        print(full_path_file) 
                        print('*'*50)
                        html = markdown.markdown(open( full_path_file  ).read())
                        print( "".join(BeautifulSoup(html).findAll(text=True))  )
                        print('*'*50)
                        print('='*100)             

def joinIssues(type_, issues_, output_):
    temp_list = []
    type_df   = pd.read_csv(type_)
    the_repos = list( np.unique(type_df['REPO'].tolist()) )
    for repo_ in the_repos:
        type_ = type_df[type_df['REPO']==repo_]['TYPE'].tolist()[0]
        temp_list.append( (repo_, type_) ) 
    temp_df  = pd.DataFrame( temp_list, columns =['REPO', 'REPO_TYPE'] ) 
    issue_df = pd.read_csv( issues_ )
    full_issue_df = temp_df.merge( issue_df, on =['REPO'] ) 
    print(full_issue_df.head())
    full_issue_df.to_csv(output_, index=False, header=['REPO', 'REPO_TYPE', 'JSON', 'URL' , 'TITLE', 'CREATE', 'CLOSED', 'COMMENT', 'BODY', 'LABEL_NAME', 'LABEL_DESC']  , encoding='utf-8')             

def giveMeOnlyDate(x_):
    x_ = x_.split('T')[0]
    date2ret = datetime( int(x_.split('-')[0]), int(x_.split('-')[1]), int(x_.split('-')[2]) , 12, 30, 30 ) 
    return date2ret 

def getWeekWiseData(week_df, out_fil): 
    full_list = [] 
    week_df['ONLY_DATE'] = week_df['DATE'].apply(giveMeOnlyDate)
    valid_weeks = ['2019-12-22', '2019-12-29', 
                   '2020-01-07', '2020-01-14', '2020-01-21', 
                   '2020-01-28', '2020-02-07', '2020-02-15', 
                   '2020-02-22', '2020-02-29', '2020-03-07', 
                   '2020-03-15', '2020-03-22', '2020-03-29', 
                   '2020-04-07'
    ]
    for week_ in valid_weeks: 
        week_       = week_.split('T')[0]
        # print(week_) 
        dt_week     = datetime( int(week_.split('-')[0]), int(week_.split('-')[1]), int(week_.split('-')[2]) , 12, 30, 30) 
        per_week_df = week_df[ week_df['ONLY_DATE'] <= dt_week ] 
        # print(per_week_df) 
        per_week_repos = np.unique( per_week_df['REPO_DIR'].tolist() )
        proj_count     = len(per_week_repos)
        full_list.append( (week_, proj_count )  )
    df_ = pd.DataFrame( full_list )
    df_.to_csv( out_fil, index=False, header=['WEEK', 'COUNT']  , encoding='utf-8' )
    




if __name__=='__main__':

    '''
    # json_dir = '/Users/arahman/Documents/OneDriveWingUp/OneDrive-TennesseeTechUniversity/Research/SciSoft/COVID19/dataset/'
    # getJSONData(json_dir)

    # repos_df = pd.read_csv('/Users/arahman/Documents/OneDriveWingUp/OneDrive-TennesseeTechUniversity/Research/SciSoft/COVID19/dataset/REPOS2DLOAD.csv')
    # list_    = repos_df['URL'].tolist()
    # list_ = np.unique(list_)

    # print('Repos to download:', len(list_)) 
    # cloneRepos(list_)

    # performFurtherChecks('/Users/arahman/COVID19_REPOS/')   
    # https://api.github.com/repos/CodeForPhilly/chime/issues  

    # repo_list_final    = '/Users/arahman/Documents/OneDriveWingUp/OneDrive-TennesseeTechUniversity/Research/SciSoft/COVID19/dataset/FINAL_REPOS.csv'
    # issues_dir         = '/Users/arahman/Documents/OneDriveWingUp/OneDrive-TennesseeTechUniversity/Research/SciSoft/COVID19/dataset/closed_issues_json/'
    # issues_output_file = '/Users/arahman/Documents/OneDriveWingUp/OneDrive-TennesseeTechUniversity/Research/SciSoft/COVID19/dataset/FINAL_CLOSED_ISSUES.csv'
    # getIssueDataFrame(repo_list_final, issues_dir, issues_output_file) 

    # issue_file = '/Users/arahman/Documents/OneDriveWingUp/OneDrive-TennesseeTechUniversity/Research/SciSoft/COVID19/dataset/FINAL_REPOS.csv'
    # repo_dir   = '/Users/arahman/COVID19_REPOS/'
    # getREADME( issue_file, repo_dir ) 

    # repo_type_file = '/Users/arahman/Documents/OneDriveWingUp/OneDrive-TennesseeTechUniversity/Research/SciSoft/COVID19/dataset/REPO_TYPE.csv'
    # repo_issues_file = '/Users/arahman/Documents/OneDriveWingUp/OneDrive-TennesseeTechUniversity/Research/SciSoft/COVID19/dataset/RAW_ISSUES.csv'
    # out_fil = '/Users/arahman/Documents/OneDriveWingUp/OneDrive-TennesseeTechUniversity/Research/SciSoft/COVID19/dataset/FINAL_ISSUES.csv'
    # joinIssues(repo_type_file, repo_issues_file, out_fil) 

    repo_file = '/Users/arahman/Documents/OneDriveWingUp/OneDrive-TennesseeTechUniversity/Research/SciSoft/COVID19/results/FINAL_REPO_CATEGS.csv'
    repo_df   = pd.read_csv(repo_file)
    getWeekWiseData(repo_df, '/Users/arahman/Documents/OneDriveWingUp/OneDrive-TennesseeTechUniversity/Research/SciSoft/COVID19/dataset/WEEK_REPOS.csv')


    '''

    t1 = time.time()
    print('Started at:', giveTimeStamp() )
    print('*'*100 )


    print('*'*100 )
    print('Ended at:', giveTimeStamp() )
    print('*'*100 )
    t2 = time.time()
    time_diff = round( (t2 - t1 ) / 60, 5) 
    print('Duration: {} minutes'.format(time_diff) )
    print( '*'*100  )  

 