from client.cat_favorites_client import CatFavoritesClient

client = CatFavoritesClient()

response = client.get_favorites()
print(response.status_code)
print(response.json())