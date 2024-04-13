import requests
from bs4 import BeautifulSoup
import pandas as pd

# Send a GET request to the IMDb Top Rated Movies page
url = "https://www.imdb.com/chart/top/"
response = requests.get(url)

# Parse the HTML content using BeautifulSoup
soup = BeautifulSoup(response.content, 'html.parser')

# Find the table containing the movie information
movie_table = soup.find('table', {'class': 'chart'})

# Extract the rows from the table
movie_rows = movie_table.find_all('tr')

# Create a list to store the movie information
movies = []

# Extract the title, year, and rating for each movie
for row in movie_rows[1:]:
    columns = row.find_all('td')
    title = columns[1].find('a').text
    year = columns[1].find('span', {'class': 'secondaryInfo'}).text.strip('()')
    rating = float(columns[2].text)
    genre = columns[3].text.strip()
    movies.append({'title': title, 'year': year, 'rating': rating, 'genre': genre})

# Create a pandas DataFrame from the movie information
df = pd.DataFrame(movies)

# Split the genre column into multiple columns
df[['genre1', 'genre2', 'genre3']] = df['genre'].str.split(' / ', expand=True)

# Calculate the number of movies for each genre
genre_count = df['genre'].value_counts()

# Filter the DataFrame to only include the top 10 genres
top_genres = genre_count.head(10)

# Calculate the average rating for each of the top 10 genres
avg_rating_by_genre = df.loc[df['genre'].isin(top_genres.index), ['genre', 'rating']] \
    .groupby('genre') \
    .mean() \
    .reset_index()

# Print the result
print("Average rating for each of the top 10 genres:")
print(avg_rating_by_genre)