# WeatherFlow Mix: Spotify Discovery Tool

<p align="center">
  <img src="https://img.shields.io/badge/python-3.9+-3776AB?logo=python&logoColor=white" alt="Python">
  <img src="https://img.shields.io/badge/Streamlit-FF4B4B?logo=streamlit&logoColor=white" alt="Streamlit">
  <img src="https://img.shields.io/badge/Spotify-API-1DB954?logo=spotify&logoColor=white" alt="Spotify">
</p>

**Read this in other languages:** [🇰🇷 한국어 버전](./README.ko.md)

---

## Overview
**WeatherFlow Mix** is a personalized discovery tool for Spotify users. Instead of repeating the same tracks, it explores the discography of artists you already love to find fresh tracks you might have missed.

## Current Features
- **Top 50 Analysis**: Analyzes your Top 50 tracks (medium term) to identify your favorite artists.
- **Deep Dive Discovery**: Fetches the "Top Tracks" from each of those artists.
- **Smart Filtering**: Automatically excludes your current Top 50 tracks to ensure you only get "new-to-you" music.
- **30-Track Curation**: Randomly selects 30 unique songs and updates them to a dedicated `WeatherFlow Mix` playlist in your library.

## Tech Stack
- **Framework**: [Streamlit](https://streamlit.io/)
- **API Library**: [Spotipy](https://spotipy.readthedocs.io/)
- **Deployment**: Streamlit Cloud

## Roadmap (Coming Soon)
- [ ] **Real-time Weather Integration**: Adjusting the playlist mood based on your local weather (Temperature, Precipitation, etc.).
- [ ] **Custom Limits**: Allow users to choose how many tracks to generate.

---
<p align="right">(<a href="#-weatherflow-mix-spotify-discovery-tool">Back to top</a>)</p>

- Link: [WeaterFlowMix](https://weatherflowmix.streamlit.app/)
