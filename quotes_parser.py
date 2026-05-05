"""
Учебный проект по веб-парсингу.
Скрипт получает HTML-код страницы quotes.toscrape.com,
извлекает цитаты, авторов и теги. Далее я произвожу небольшой анализ страницы,
а затем сохраняю данные в CSV-файл.
"""


from bs4 import BeautifulSoup
import requests
import pandas as pd


url = 'https://quotes.toscrape.com'

response = requests.get(url, timeout=10)
response.raise_for_status()

content = response.text

soup = BeautifulSoup(content, 'html.parser')

page_title = soup.title.get_text()
print(f'Заголовок страницы: {page_title}\n')

quotes_blocks = soup.find_all('div', class_='quote')
print(f'Количество цитат страницы: {len(quotes_blocks)}\n')

quotes_data = []

for block in quotes_blocks:
    text = block.find('span', class_='text').get_text()
    author = block.find('small', class_='author').get_text()
    tags = [t.get_text() for t in block.find_all('a', class_='tag')]

    quotes_data.append({
        'text': text,
        'author': author,
        'tags': ', '.join(tags)
    })
df = pd.DataFrame(quotes_data).sort_values('author').reset_index(drop=True)

print(df.head().to_string())


# Анализ страницы
unique_authors = df['author'].nunique()
print(f'Уникальных авторов на странице: {unique_authors} \n')

count_quotes_of_authors = df.groupby('author')['text'].count().reset_index()
count_quotes_of_authors.columns = ['Авторы', 'Кол-во цитат']
print(count_quotes_of_authors)

count_quotes = count_quotes_of_authors.iloc[0]
print(f'\nАвтор с максимальным кол-ом цитат:\n{count_quotes}\n')

all_tags = df['tags'].str.split(', ').explode()
count_unique_tags = all_tags.nunique()
print(f'Кол-во уникальных тегов: {count_unique_tags}\n')

tag_count = all_tags.value_counts()
most_frequent_tag = tag_count.idxmax()
most_frequent_tag_count = tag_count.max()

print(f'Часто встречающийся тег: {most_frequent_tag}\nКол-во повторений тега: {most_frequent_tag_count}')


df.to_csv('quotes_data.csv', index=False, encoding='utf-8-sig')