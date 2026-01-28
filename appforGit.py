import streamlit as st
import spotipy
from spotipy.oauth2 import SpotifyOAuth
import os
import random

# Streamlit Cloud의 secrets 사용
SPOTIPY_CLIENT_ID = st.secrets.get("SPOTIPY_CLIENT_ID", os.getenv("SPOTIPY_CLIENT_ID"))
SPOTIPY_CLIENT_SECRET = st.secrets.get("SPOTIPY_CLIENT_SECRET", os.getenv("SPOTIPY_CLIENT_SECRET"))
SPOTIPY_REDIRECT_URI = st.secrets.get("SPOTIPY_REDIRECT_URI", os.getenv("SPOTIPY_REDIRECT_URI"))

def get_spotify_client():
    """Spotify 클라이언트 반환 또는 로그인 URL 반환"""
    scope = "playlist-modify-public playlist-modify-private user-top-read"
    
    auth_manager = SpotifyOAuth(
        client_id=SPOTIPY_CLIENT_ID,
        client_secret=SPOTIPY_CLIENT_SECRET,
        redirect_uri=SPOTIPY_REDIRECT_URI,
        scope=scope,
        cache_handler=spotipy.cache_handler.MemoryCacheHandler(),
        show_dialog=True
    )
    
    # URL에서 code 파라미터 확인
    if 'code' in st.query_params:
        code = st.query_params['code']
        try:
            token_info = auth_manager.get_access_token(code, as_dict=True, check_cache=False)
            if token_info:
                st.session_state['token_info'] = token_info
                st.query_params.clear()
                st.rerun()
        except:
            pass
    
    # 세션에 저장된 토큰 확인
    if 'token_info' in st.session_state:
        return spotipy.Spotify(auth=st.session_state['token_info']['access_token'])
    
    # 로그인 필요
    return None

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
                    if track['id'] not in seen_track_ids:
                        candidate_tracks.append(track)
                        seen_track_ids.add(track['id'])
            except:
                continue
    
    st.success(f"✅ Collected {len(candidate_tracks)} new tracks (excluding your top 50)")
    
    random.shuffle(candidate_tracks)
    return candidate_tracks[:limit]

# --- UI ---
st.set_page_config(page_title="Spotify Playlist Generator", layout="centered")
st.title("🎵 Spotify Playlist Generator")
st.write("Generate a personalized playlist from your favorite artists!")
st.caption("💡 Tip: This app creates playlists based on artists you already love, excluding your current top 50 tracks for fresh discoveries!")

# Spotify 인증
sp = get_spotify_client()

if sp is None:
    # 로그인 필요
    st.warning("🔐 You need to login with Spotify first!")
    
    auth_manager = SpotifyOAuth(
        client_id=SPOTIPY_CLIENT_ID,
        client_secret=SPOTIPY_CLIENT_SECRET,
        redirect_uri=SPOTIPY_REDIRECT_URI,
        scope="playlist-modify-public playlist-modify-private user-top-read",
        cache_handler=spotipy.cache_handler.MemoryCacheHandler(),
        show_dialog=True
    )
    auth_url = auth_manager.get_authorize_url()
    
    st.markdown(f"### [Click here to login with Spotify]({auth_url})")
    st.info("After logging in, you'll be redirected back here automatically.")
    st.stop()

# 로그인 완료
st.success("✅ Connected to Spotify!")

# 로그아웃 버튼
if st.button("🚪 Logout"):
    if 'token_info' in st.session_state:
        del st.session_state['token_info']
    st.rerun()

# 메인 기능
if st.button("🔄 Generate Playlist"):
    try:
        user_id = sp.current_user()['id']
        user_name = sp.current_user()['display_name']
        
        st.info(f"👋 Hi {user_name}!")
        
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