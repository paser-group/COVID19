'''
Akond Rahman 
Sep 27, 2023
Answer to RQ1 
'''
import os 
import csv 
import pandas as pd 
import numpy as np 
from git import Repo
from git import exc 
import subprocess
from datetime import datetime


def ans2part1(file_):
    df_ = pd.read_csv(file_) 
    df_closed_bugs = df_[df_['CLOSED']!='NOT_CLOSED'] 
    categs_bugs =  np.unique( df_closed_bugs['BUG_CATEG_NEW'].tolist() )
    all_closed_bugs = np.unique( df_closed_bugs['URL'].tolist() )
    all_closed_bugs = [x_ for x_ in all_closed_bugs if 'https://api.github.com/repos/RehanSaeed/Schema.NET/issues/' not in x_ ]
    all_closed_bugs = [x_ for x_ in all_closed_bugs if 'https://api.github.com/repos/vinitshahdeo/Water-Monitoring-System/issues/' not in x_]
    for cat in categs_bugs:
        cat_bug_df = df_closed_bugs[df_closed_bugs['BUG_CATEG_NEW']==cat] 
        cat_bug_ls = np.unique( cat_bug_df['URL'].tolist()  )
        cat_bug_ls = [x_ for x_ in cat_bug_ls if 'https://api.github.com/repos/RehanSaeed/Schema.NET/issues/' not in x_   ]
        cat_bug_ls = [x_ for x_ in cat_bug_ls if 'https://api.github.com/repos/vinitshahdeo/Water-Monitoring-System/issues/' not in x_ ]
        print('CATEG:{}, ALL:{}, CATEG_COUNT:{}, CATEG_PROP:{}'.format( cat, len(all_closed_bugs) , len(cat_bug_ls) , (float(len(cat_bug_ls))/float(len(all_closed_bugs)) ) *100 ) )
        print('*'*50)


def ans2part2(repo_file, bug_file): 
    repo_df = pd.read_csv(repo_file) 
    
    repo_categs = np.unique( repo_df['CATEGORY'].tolist() ) 

    df_ = pd.read_csv(bug_file) 
    bug_df = df_[df_['CLOSED']!='NOT_CLOSED'] 
    categs_bugs =  np.unique( bug_df['BUG_CATEG_NEW'].tolist() )

    for bug_categ in categs_bugs:
        for repo_cat in repo_categs:
            categ_df = repo_df[repo_df['CATEGORY']==repo_cat]
            repos_per_categ =  np.unique( categ_df['REPO_DIR'].tolist() ) 
            per_repo_categ_bugs = [] 
            repo_categ_bug_categ = [] 
            for repo_dir in repos_per_categ:
                repo_name = repo_dir.split('/')[-1] 
                repo_bug_df = bug_df[bug_df['REPO']==repo_name] 
                per_repo_categ_bugs = per_repo_categ_bugs +  list(np.unique( repo_bug_df['URL'].tolist() ) )

                bug_categ_repo_df = repo_bug_df[repo_bug_df['BUG_CATEG_NEW']==bug_categ]
                per_repo_bug_categs = list(np.unique( bug_categ_repo_df['URL'].tolist() ) )
                repo_categ_bug_categ = repo_categ_bug_categ + per_repo_bug_categs 

            print('BUG_CATEG:{}, REPO_CATEG:{}, ALL_BUGS:{}, PER_CATEG_BUGS:{}, PROP:{}'.format(bug_categ, repo_cat, len(per_repo_categ_bugs), len(repo_categ_bug_categ), float(len(repo_categ_bug_categ))/float(len(per_repo_categ_bugs))*100) )
            print('-'*25)
        print('~'*50)



def perRepoBugs(repo_file, bug_file):
    repo_df = pd.read_csv(repo_file) 
    bug_df  = pd.read_csv(bug_file) 
    
    repo_categs = np.unique( repo_df['CATEGORY'].tolist() ) 

    df_closed_bugs = bug_df[bug_df['CLOSED']!='NOT_CLOSED']  

    for repo_cat in repo_categs:
            categ_df = repo_df[repo_df['CATEGORY']==repo_cat]
            repos_per_categ =  np.unique( categ_df['REPO_DIR'].tolist() ) 
            per_repo_categ_bugs = [] 

            for repo_dir in repos_per_categ:
                repo_name = repo_dir.split('/')[-1] 
                repo_bug_df = df_closed_bugs[df_closed_bugs['REPO']==repo_name]  
                per_repo_categ_bugs = per_repo_categ_bugs +  list(np.unique( repo_bug_df['URL'].tolist() ) )


            print('REPO_CATEG:{}, ALL_BUGS:{}'.format( repo_cat, len(per_repo_categ_bugs)  ) )
            print('-'*25)


def duration_between(d1_, d2_): ## pass in date time objects 
    secs  = (d2_- d1_).total_seconds()
    mins  = float(secs) / float(60) 
    hrs   = float(mins) / float(60)

    return mins, hrs 

def overallBugResolution(bug_fil): 
    df_ = pd.read_csv(bug_fil) 
    df_closed_bugs = df_[df_['CLOSED']!='NOT_CLOSED'] 
    
    categs_bugs =  np.unique( df_closed_bugs['BUG_CATEG_NEW'].tolist() )
    all_closed_bugs = np.unique( df_closed_bugs['URL'].tolist() )
    all_closed_bugs = [x_ for x_ in all_closed_bugs if 'https://api.github.com/repos/RehanSaeed/Schema.NET/issues/' not in x_ ]
    all_closed_bugs = [x_ for x_ in all_closed_bugs if 'https://api.github.com/repos/vinitshahdeo/Water-Monitoring-System/issues/' not in x_]
    
    for cat in categs_bugs:
        cat_bug_df = df_closed_bugs[df_closed_bugs['BUG_CATEG_NEW']==cat] 
        filtered_cat_bug_df = cat_bug_df[cat_bug_df['REPO']!='Schema.NET@RehanSaeed']
        final_cat_bug_df    = filtered_cat_bug_df[filtered_cat_bug_df['REPO']!='Water-Monitoring-System@vinitshahdeo']

        bugs = np.unique( final_cat_bug_df['URL'].tolist() ) 
        resolution_time = [] 
        for bugID in bugs:
            bug_df = final_cat_bug_df[final_cat_bug_df['URL']==bugID]

            bug_start = bug_df['CREATE'].tolist()[0] 
            bug_end   = bug_df['CLOSED'].tolist()[0] 
            bug_start = bug_start.replace('Z', '') 
            bug_end   = bug_end.replace('Z', '') 

            date_factor , time_factor = bug_start.split('T')[0], bug_start.split('T')[1] 
            bug_s_dt  = datetime(int(date_factor.split('-')[0]), int(date_factor.split('-')[1]), 
                                           int(date_factor.split('-')[2]), int(time_factor.split(':')[0]) , 
                                           int(time_factor.split(':')[1]), int(time_factor.split(':')[2])   
                                )  
            date_factor , time_factor = bug_end.split('T')[0], bug_end.split('T')[1] 
            bug_e_dt  = datetime(int(date_factor.split('-')[0]), int(date_factor.split('-')[1]), 
                                           int(date_factor.split('-')[2]), int(time_factor.split(':')[0]) , 
                                           int(time_factor.split(':')[1]), int(time_factor.split(':')[2]) 
                               )  

            res_time_minute, res_time_hour    = duration_between(bug_s_dt, bug_e_dt)  
            # print(bug_s_dt, bug_e_dt, res_time)  
            resolution_time.append( res_time_hour ) 
        # print(resolution_time) 
        print('CATEG:{}, MIN:{}, MEDIAN:{}, MAX:{} [DURATION:HOURS]'.format( cat, min(resolution_time), np.median(resolution_time), max(resolution_time) )) 
        print('*'*50) 
     

def durationRepoCategBugCateg(repo_file, bug_file): 
    repo_df = pd.read_csv(repo_file) 
    
    repo_categs = np.unique( repo_df['CATEGORY'].tolist() ) 

    df_ = pd.read_csv(bug_file) 
    bug_df = df_[df_['CLOSED']!='NOT_CLOSED'] 
    categs_bugs =  np.unique( bug_df['BUG_CATEG_NEW'].tolist() )

    for bug_categ in categs_bugs:
        for repo_cat in repo_categs:
            categ_df = repo_df[repo_df['CATEGORY']==repo_cat]
            repos_per_categ =  np.unique( categ_df['REPO_DIR'].tolist() ) 
            
            resolution_time = []             
            for repo_dir in repos_per_categ:
                repo_name = repo_dir.split('/')[-1] 

                repo_bug_df       = bug_df[bug_df['REPO']==repo_name] 
                repo_bug_categ_df = repo_bug_df[repo_bug_df['BUG_CATEG_NEW']==bug_categ]  

                bugs = np.unique( repo_bug_categ_df['URL'].tolist() ) 
                for bugID in bugs:
                    one_bug_df= bug_df[bug_df['URL']==bugID]

                    bug_start = one_bug_df['CREATE'].tolist()[0] 
                    bug_end   = one_bug_df['CLOSED'].tolist()[0] 
                    bug_start = bug_start.replace('Z', '') 
                    bug_end   = bug_end.replace('Z', '') 

                    date_factor , time_factor = bug_start.split('T')[0], bug_start.split('T')[1] 
                    bug_s_dt  = datetime(int(date_factor.split('-')[0]), int(date_factor.split('-')[1]), 
                                                int(date_factor.split('-')[2]), int(time_factor.split(':')[0]) , 
                                                int(time_factor.split(':')[1]), int(time_factor.split(':')[2])   
                                        )  
                    date_factor , time_factor = bug_end.split('T')[0], bug_end.split('T')[1] 
                    bug_e_dt  = datetime(int(date_factor.split('-')[0]), int(date_factor.split('-')[1]), 
                                                int(date_factor.split('-')[2]), int(time_factor.split(':')[0]) , 
                                                int(time_factor.split(':')[1]), int(time_factor.split(':')[2]) 
                                    )  

                    res_time_minute, res_time_hour    = duration_between(bug_s_dt, bug_e_dt)  
                    # print(bug_s_dt, bug_e_dt, res_time_hour)  
                    resolution_time.append( res_time_hour ) 
            if len(resolution_time) > 0: 
                print('REPO_CATEG:{}, BUG_CATEG:{}, MIN:{}, MEDIAN:{}, MAX:{} [DURATION:HOURS]'.format(repo_cat, bug_categ, min(resolution_time), np.median(resolution_time), max(resolution_time)))
                print('*'*25)
            else: 
                print('NO BUG REPORTS EXIST FOR BUG_CATEG:{} and REPO_CATEG:{}'.format(bug_categ, repo_cat)  )
                print('*'*25)
        print('~'*50)


def durationRepoCateg(repo_file, bug_file): 
    repo_df = pd.read_csv(repo_file) 
    
    repo_categs = np.unique( repo_df['CATEGORY'].tolist() ) 

    df_ = pd.read_csv(bug_file) 
    bug_df = df_[df_['CLOSED']!='NOT_CLOSED'] 

    mega_list = [] 
    for repo_cat in repo_categs:
            categ_df = repo_df[repo_df['CATEGORY']==repo_cat]
            repos_per_categ =  np.unique( categ_df['REPO_DIR'].tolist() ) 
            
            resolution_time = []             
            for repo_dir in repos_per_categ:
                repo_name = repo_dir.split('/')[-1] 

                repo_bug_df       = bug_df[bug_df['REPO']==repo_name] 

                bugs = np.unique( repo_bug_df['URL'].tolist() ) 
                for bugID in bugs:
                    one_bug_df= bug_df[bug_df['URL']==bugID]

                    bug_start = one_bug_df['CREATE'].tolist()[0] 
                    bug_end   = one_bug_df['CLOSED'].tolist()[0] 
                    bug_start = bug_start.replace('Z', '') 
                    bug_end   = bug_end.replace('Z', '') 

                    date_factor , time_factor = bug_start.split('T')[0], bug_start.split('T')[1] 
                    bug_s_dt  = datetime(int(date_factor.split('-')[0]), int(date_factor.split('-')[1]), 
                                                int(date_factor.split('-')[2]), int(time_factor.split(':')[0]) , 
                                                int(time_factor.split(':')[1]), int(time_factor.split(':')[2])   
                                        )  
                    date_factor , time_factor = bug_end.split('T')[0], bug_end.split('T')[1] 
                    bug_e_dt  = datetime(int(date_factor.split('-')[0]), int(date_factor.split('-')[1]), 
                                                int(date_factor.split('-')[2]), int(time_factor.split(':')[0]) , 
                                                int(time_factor.split(':')[1]), int(time_factor.split(':')[2]) 
                                    )  

                    res_time_minute, res_time_hour    = duration_between(bug_s_dt, bug_e_dt)  
                    # print(bug_s_dt, bug_e_dt, res_time_hour)  
                    resolution_time.append( res_time_hour ) 
                    mega_list.append( res_time_hour )

            print('REPO_CATEG:{}, MIN:{}, MEDIAN:{}, MAX:{} [DURATION:HOURS]'.format(repo_cat, min(resolution_time), np.median(resolution_time), max(resolution_time)))
            print('#'*25)
    print('ALL, MIN:{}, MEDIAN:{}, MAX:{} [DURATION:HOURS]'.format(min(mega_list), np.median(mega_list), max(mega_list) )  )
    print('#'*25)


if __name__ == '__main__':
    repo_categ_file = '/Users/arahman/Documents/OneDriveWingUp/OneDrive-TennesseeTechUniversity/Research/SciSoft/COVID19/results/FINAL_REPO_CATEGS.csv'
    bug_categ_file  = '/Users/arahman/Documents/OneDriveWingUp/OneDrive-TennesseeTechUniversity/Research/SciSoft/COVID19/results/FINAL_BUG_CATEGS.csv'

    print('FREQUNECY PER BUG CATEGORY')
    ans2part1(bug_categ_file)
    print('='*100) 
    print('FREQUNECY PER REPO CATEGORY PER BUG CATEGORY')
    ans2part2(repo_categ_file, bug_categ_file) 
    print('='*100)     
    print('FREQUNECY PER REPO CATEGORY ')
    perRepoBugs(repo_categ_file, bug_categ_file)     
    print('='*100)         

    print('DURATION PER BUG CATEGORY')
    overallBugResolution(bug_categ_file)     
    print('='*100)          

    print('DURATION PER BUG CATEGORY PER REPO CATEGORY')    
    durationRepoCategBugCateg(repo_categ_file, bug_categ_file)   
    print('='*100)              

    print('DURATION PER REPO CATEGORY')    
    durationRepoCateg(repo_categ_file, bug_categ_file)   
    print('='*100)              
