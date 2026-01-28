# WeatherFlow Mix: 스포티파이 곡 추천 도구

**다른 언어로 읽기:** [🇺🇸 English Version](./README.md)

---

## 프로젝트 개요
**WeatherFlow Mix**는 스포티파이 사용자를 위한 개인 맞춤형 음악 발굴 도구입니다. 단순히 듣던 곡을 반복하는 것이 아니라, 사용자가 선호하는 아티스트의 다른 인기곡들을 탐색하여 새로운 취향을 찾아줍니다.

## 현재 주요 기능
- **상위 50곡 분석**: 사용자의 최근 상위 50곡을 분석하여 선호 아티스트 목록을 추출합니다.
- **아티스트 딥다이브**: 추출된 각 아티스트의 인기곡(Top Tracks) 데이터를 수집합니다.
- **스마트 필터링**: 현재 상위 50곡에 포함된 곡은 자동으로 제외하여 중복 없는 신선한 리스트를 보장합니다.
- **30곡 큐레이션**: 엄선된 곡 중 무작위로 30곡을 선정하여 `WeatherFlow Mix` 플레이리스트를 생성 및 업데이트합니다.

## 기술 스택
- **프레임워크**: [Streamlit](https://streamlit.io/)
- **라이브러리**: [Spotipy](https://spotipy.readthedocs.io/)
- **배포**: Streamlit Cloud

## 향후 업데이트 계획 (Roadmap)
- [ ] **실시간 날씨 연동**: 사용자의 지역 날씨(기온, 강수 등)에 맞춰 플레이리스트 분위기 최적화.
- [ ] **생성 개수 조절**: 사용자가 원하는 곡 수만큼 플레이리스트 구성 기능 추가.

---
<p align="right">(<a href="#-weatherflow-mix-스포티파이-곡-추천-도구">상단으로 이동</a>)</p>

- Linke: [WeatherFlowMix](https://weatherflowmix.streamlit.app/)
