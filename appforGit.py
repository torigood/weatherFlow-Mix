import streamlit as st
import spotipy
from spotipy.oauth2 import SpotifyOAuth
import requests
import os
import random
from dotenv import load_dotenv

load_dotenv()

SPOTIPY_CLIENT_ID = os.getenv("SPOTIPY_CLIENT_ID")
SPOTIPY_CLIENT_SECRET = os.getenv("SPOTIPY_CLIENT_SECRET")
SPOTIPY_REDIRECT_URI = os.getenv("SPOTIPY_REDIRECT_URI")
WEATHER_API_KEY = os.getenv("WEATHER_API_KEY")

def get_spotify_client():
    scope = "playlist-modify-public playlist-modify-private user-top-read"
    auth_manager=SpotifyOAuth(
        client_id=SPOTIPY_CLIENT_ID,
        client_secret=SPOTIPY_CLIENT_SECRET,
        redirect_uri=SPOTIPY_REDIRECT_URI,
        scope=scope,
        cache_handler=spotipy.cache_handler.MemoryCacheHandler(),  
        show_dialog=True
    )

    # On URL, check code parameter
    if 'code' in st.query_params:
        code = st.query_params['code']
        token_info = auth_manager.get_access_token(code, as_dict=True, check_cache=False)
        
        if token_info:
            st.session_state['token_info'] = token_info
            # After storing token, clear query params
            st.query_params.clear()
            st.rerun()
    
    # Check if token is already in session
    if 'token_info' in st.session_state:
        return spotipy.Spotify(auth=st.session_state['token_info']['access_token'])
    
    # 
    auth_url = auth_manager.get_authorize_url()
    return None, auth_url 


#def get_weather_data(city):
#    url = f"http://api.openweathermap.org/data/2.5/weather?q={city}&appid={WEATHER_API_KEY}&units=metric"
#    r esponse = requests.get(url)
#    return response.json()


def get_tracks_from_my_artists(sp, seed_track_ids, limit=30):
    """
    내 탑 트랙의 아티스트들의 다른 인기곡으로 플레이리스트 생성
    """
    candidate_tracks = []
    seen_track_ids = set(seed_track_ids)
    
    # 시드 트랙들에서 아티스트 추출
    artists = []
    with st.spinner("Analyzing your favorite artists..."):
        for track_id in seed_track_ids:
            try:
                track = sp.track(track_id)
                for artist in track['artists']:
                    if artist['id'] not in [a['id'] for a in artists]:
                        artists.append(artist)
            except:
                continue
    
    st.info(f"✅ Found {len(artists)} artists from your top 50 tracks")
    
    # 각 아티스트의 인기곡 가져오기
    with st.spinner("Collecting tracks from these artists..."):
        for artist in artists:
            try:
                top_tracks = sp.artist_top_tracks(artist['id'])
                
                for track in top_tracks['tracks']:
                    # 내 탑 50에 없는 곡만 추가
                    if track['id'] not in seen_track_ids:
                        candidate_tracks.append(track)
                        seen_track_ids.add(track['id'])
            except:
                continue
    
    st.success(f"✅ Collected {len(candidate_tracks)} new tracks (excluding your top 50)")
    
    # 랜덤 셔플 후 limit개 선택
    random.shuffle(candidate_tracks)
    return candidate_tracks[:limit]

st.set_page_config(page_title="Weather-Based Spotify Playlist", layout="centered")
# Title and Description
st.title("🎵 Spotify Playlist Generator")
st.write("Generate a personalized playlist from your favorite artists!")
st.caption("💡 Tip: This app creates playlists based on artists you already love, "
          "excluding your current top 50 tracks for fresh discoveries!")

if st.button("🔄 Generate Playlist"):
    try:
        sp = get_spotify_client()
        user_id = sp.current_user()['id']
        
        # Get current weather (for display only)
        #city = "Waterloo"
        #weather_data = get_weather_data(city)
        #weather_main = weather_data['weather'][0]['main']
        #temp = weather_data['main']['temp']

        #st.info(f"🌤️ Current Weather in {city}: {weather_main} ({temp}°C)")
        
        
        # Get top tracks
        with st.spinner("Fetching your top tracks..."):
            top_tracks = sp.current_user_top_tracks(limit=50, time_range='medium_term')
            all_track_ids = [t['id'] for t in top_tracks['items'] if t.get('id')]

        st.success(f"✅ Got {len(all_track_ids)} top tracks")

        # Get tracks from my artists
        recommendations = get_tracks_from_my_artists(sp, all_track_ids, limit=30)
        
        track_ids = [t['id'] for t in recommendations]
        
        if len(track_ids) >= 10:
            st.success(f"✅ Generated {len(track_ids)} recommendations")
            
            # Show some sample tracks
            with st.expander("📋 Preview tracks"):
                for i, track in enumerate(recommendations[:5], 1):
                    artists = ", ".join([a['name'] for a in track['artists']])
                    st.write(f"{i}. **{track['name']}** - {artists}")
            
            # Create/Update Playlist
            playlist_name = "WeatherFlow Mix"
            playlists = sp.current_user_playlists()
            target_playlist = next((p for p in playlists['items'] if p['name'] == playlist_name), None)
            
            if not target_playlist:
                target_playlist = sp.user_playlist_create(user_id, playlist_name, public=True, 
                                                         description=f"Generated playlist based on your music taste")
                st.info("✨ Created new playlist: WeatherFlow Mix")
            
            sp.playlist_replace_items(target_playlist['id'], track_ids)
            
            st.success("✅ Playlist updated successfully!")
            st.link_button("🎵 Open Playlist on Spotify", target_playlist['external_urls']['spotify'])
        else:
            st.warning(f"⚠️ Only found {len(track_ids)} tracks. Your music library might be too small. "
                      f"Try listening to more artists on Spotify!")

    except Exception as e:
        st.error(f"❌ Error: {e}")
        import traceback
        with st.expander("Show error details"):
            st.code(traceback.format_exc())