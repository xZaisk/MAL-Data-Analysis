import requests
import pandas as pd

# Your MyAnimeList Client ID (Get it from https://myanimelist.net/apiconfig)
CLIENT_ID = "903b5eb0521641ee864a3cdd30dbe450"

# MAL API URL for anime ranking (fetching top anime)
BASE_URL = "https://api.myanimelist.net/v2/anime/ranking"

# Headers for authentication
HEADERS = {"X-MAL-CLIENT-ID": CLIENT_ID}

# Function to fetch anime data
def fetch_anime_data(limit=500):
    all_anime = []
    offset = 0  # Used for pagination
    
    while len(all_anime) < limit:
        # API request with pagination
        params = {
            "ranking_type": "all",
            "limit": 100,  # Max per request
            "offset": offset,
            "fields": "id,title,rank,mean,popularity,studios,num_episodes,status,genres,start_date,end_date,rating,media_type,mean,source,average_episode_duration,synopsis,statistics"
        }
        # 
        response = requests.get(BASE_URL, headers=HEADERS, params=params)
        
        if response.status_code != 200:
            print("Error:", response.status_code, response.text)
            break

        data = response.json()
        
        for anime in data.get("data", []):
            node = anime["node"]
            stats = node.get("statistics", {}).get("status", {})

            all_anime.append({
                "id": node.get("id", "N/A"),
                "title": node.get("title", "N/A"),
                "rank": node.get("rank", "N/A"),
                "mean": node.get("mean", "N/A"),
                "popularity": node.get("popularity", "N/A"),
                "studios": ", ".join(studio["name"] for studio in node.get("studios", [])),
                "num_episodes": node.get("num_episodes", "N/A"),
                "status": node.get("status", "N/A"),
                "genres": ", ".join(genre["name"] for genre in node.get("genres", [])),
                "start_date": node.get("start_date", "N/A"),
                "end_date": node.get("end_date", "N/A"),
                "rating": node.get("rating", "N/A"),
                "media_type": node.get("media_type", "N/A"),
                "source": node.get("source", "N/A"),
                "average_episode_duration": node.get("average_episode_duration", "N/A"),
                "synopsis": node.get("synopsis", "N/A"),
                "statistics": node.get("statistics", {})
                "Synopsis": node.get("synopsis", "N/A"),
                "Watching": stats.get("watching", 0),
                "Completed": stats.get("completed", 0),
                "On Hold": stats.get("on_hold", 0),
                "Dropped": stats.get("dropped", 0),
                "Plan to Watch": stats.get("plan_to_watch", 0),
                "Total List Users": node.get("statistics", {}).get("num_list_users", 0)


            })
        
        offset += 100  # Increase offset for pagination
        if "paging" not in data or "next" not in data["paging"]:  # Stop if there's no next page
            break

    return all_anime

# Fetch anime data
anime_list = fetch_anime_data(limit=500)  # Fetch up to 20000 anime

# Convert to DataFrame
df = pd.DataFrame(anime_list)

# Save to Excel
df.to_excel("mal_anime_list_v2.xlsx", index=False)

# Save to CSV (if needed)
df.to_csv("mal_anime_list_v2.csv", index=False)

print("Anime list saved to 'mal_anime_list.xlsx'")
