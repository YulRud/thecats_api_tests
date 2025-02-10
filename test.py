from client.cat_favorites_client import CatFavoritesClient

client = CatFavoritesClient()

response = client.get_favorites('live_Qc2yvxGD20H7cPuXf2TMWoxZmGT25UVZyPKHwR5vIlxLvmjLvx01PwXo8rXYu78O')
print(response.status_code)
print(response.json())