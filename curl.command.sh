#!/bin/bash
while IFS='' read -r line || [[ -n "$line" ]]; do
  repo_name=$line
  echo "----------------------------------------------------------------------------"
  echo $repo_name
  jsonFileName=`echo $repo_name | tr '/' _`
  echo $jsonFileName
  curl -H "Authorization: token <TOKEN_GOES_HERE>" -ni "https://api.github.com/repos/"$repo_name"/issues?state=closed&per_page=100&page=14" -H 'Accept: json' > $jsonFileName.json
  echo "----------------------------------------------------------------------------"
done < "$1" 



## pagination with query 
## CFP: https://emsejournal.github.io/special_issues/2020_SE_and_COVID-19.html

# curl -H "Authorization: token <TOKEN_GOES_HERE>" -ni "https://api.github.com/search/repositories?q=covid19&sort=stars&order=desc&per_page=100&page=7" -H 'Accept: json' > covid17.json  

