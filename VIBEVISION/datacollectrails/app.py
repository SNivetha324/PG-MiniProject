import http.client

conn = http.client.HTTPSConnection("real-time-amazon-data.p.rapidapi.com")

headers = {
    'x-rapidapi-key': "2edbed8e82msh10fc08c071362b0p1c559cjsn76bf1b23b427",
    'x-rapidapi-host': "real-time-amazon-data.p.rapidapi.com"
}

conn.request("GET", "/product-reviews?asin=B07ZPKN6YR&country=US&sort_by=TOP_REVIEWS&star_rating=ALL&verified_purchases_only=false&images_or_videos_only=false&current_format_only=false&page=1", headers=headers)

res = conn.getresponse()
data = res.read()

print(data.decode("utf-8"))