# 🎵 Songs In Your Neighborhood 
## Summary
Originally created in 2021 for Python programming labs, Songs In Your Neighborhood was designed as a **personal song recommendation app**. It allowed the user to find songs from a chosen Spotify playlist based on a reference song and selected audio features.

## ⚠ Spotify Web API Update & Project Status
🚨 Update (Feb 2025): Spotify recently [removed access to audio features](https://developer.spotify.com/blog/2024-11-27-changes-to-the-web-api) (e.g., danceability, energy) from their API, which were a **core part** of this project.  

❌ As a result, the original functionality is no longer working.   
🔄 The project is in transition and may evolve over time. I may explore adapting it to focus on user behavior analysis, such as listening habits and trends.

##  How It Used to Work
1) Pick a Spotify playlist to use as a recommendation source.
2) Choose a reference song to base the recommendation on.
3) Select audio features (e.g. energy, danceability, key) to guide the recommendation.
4) Find similar songs in your "neighborhood" that you might like.  

## 🛠 Technologies used
- Python
- pandas
- Spotify Web API (Spotipy)
- GUI (Tkinter)
- KNN-style similarity search using feature distances
- matplotlib (for visualizing nearest neighbors)


🚨 Note: Due to Spotify API changes, the recommendation system based on audio features is no longer functional.

## Planned upgrades (outdated due to the API update)
- GUI major upgrade
- Data visualization changes
  - interactive annotations (hover over feature) 
- Built-in music player to play snippets of recommended songs

## Screenshots
![SIYN_screenshot1](https://user-images.githubusercontent.com/50332018/233088348-b5a47b3f-de6c-45f1-8f5c-ca02dac45a09.png)
![SIYN_screenshot2](https://user-images.githubusercontent.com/50332018/233088354-e08dfc38-3b6a-46ac-8efa-6748ebf4a163.png)


