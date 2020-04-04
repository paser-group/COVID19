## pagination with query 
## CFP: https://emsejournal.github.io/special_issues/2020_SE_and_COVID-19.html

curl -H "Authorization: token <TOKEN_GOES_HERE>" -ni "https://api.github.com/search/repositories?q=covid19&sort=stars&order=desc&per_page=100&page=7" -H 'Accept: json' > covid17.json  

