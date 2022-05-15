from requests import Session
from bs4 import BeautifulSoup


headers = {"User-Agent": "Mozilla/5.0 (iPhone; CPU iPhone OS 12_0 like Mac OS X)"
                         " AppleWebKit/605.1.15 (KHTML, like Gecko)"
                         " CriOS/69.0.3497.105 Mobile/15E148 Safari/605.1"}

work = Session()
url = "https://quotes.toscrape.com/"

work.get(url, headers=headers)
response = work.get(url + "login", headers=headers)

soup = BeautifulSoup(response.text, 'lxml')
token = soup.find("form").find('input').get("value")

data = {
    'csrf_token': token,
    'username': "user1",
    'password': "user1auth",
}

result = work.post(url + "login", headers=headers, data=data, allow_redirects=True)

count = 1

while True:
    start_url = f"{url}page/{count}/"

    response = work.get(start_url, headers=headers)
    soup = BeautifulSoup(response.text, 'lxml')
    article = soup.find_all("div", class_="quote")

    for item in article:
        with open("get_all_quotes.txt", 'a', encoding="utf-8") as file:
            text = item.find("span", class_="text").text
            author = item.find("small", class_="author").text
            for_tags = item.find_all("a", class_="tag")
            tags = []

            for i in for_tags:
                tags.append(i.text)
            file.write(f"Text: {text}" + "\n")
            file.write(f"Author: {author}" + "\n")
            file.write(f"Tags: {tags}")
            file.write("\n\n")

    next_button = soup.find("li", class_="next")
    if not next_button:
        break
    count += 1
