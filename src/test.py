import requests

url = "https://api.bseindia.com/BseIndiaAPI/api/AnnSubCategoryGetData/w"

headers = {
    "accept": "application/json, text/plain, */*",
    "accept-language": "en-GB,en-US;q=0.9,en;q=0.8",
    "cache-control": "no-cache",
    "origin": "https://www.bseindia.com",
    "pragma": "no-cache",
    "priority": "u=1, i",
    "referer": "https://www.bseindia.com/",
    "sec-ch-ua": '"NotA;Brand";v="99", "Google Chrome";v="127", "Chromium";v="127"',
    "sec-ch-ua-mobile": "?0",
    "sec-ch-ua-platform": '"macOS"',
    "sec-fetch-dest": "empty",
    "sec-fetch-mode": "cors",
    "sec-fetch-site": "same-site",
    "user-agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/127.0.0.0 Safari/537.36",
}

params = {
    "pageno": 1,
    "strCat": "Company Update",
    "strPrevDate": "20240814",
    "strScrip": "",
    "strSearch": "P",
    "strToDate": "20240814",
    "strType": "C",
    "subcategory": "Award of Order / Receipt of Order",
}

response = requests.get(url, headers=headers, params=params)

print(response.json())
