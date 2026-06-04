# 🔧 Supabase 연결 설정 가이드

Streamlit 앱이 Supabase 데이터베이스와 연결되었습니다. 실행하기 전에 다음 단계를 완료해주세요.

## 1️⃣ Supabase 프로젝트 준비

### 1-1. Supabase 접속
- [Supabase](https://supabase.com) 웹사이트 방문
- 로그인 후 프로젝트 대시보드 열기

### 1-2. API 자격증명 확인
1. 좌측 메뉴에서 **Settings** → **API** 선택
2. **Project URL** 복사
3. **anon public** 키 복사

## 2️⃣ Streamlit 비밀번호 파일 설정

### 2-1. 파일 위치
```
프로젝트 폴더
├── .streamlit/
│   └── secrets.toml  ← 이 파일 수정
├── app.py
└── requirements.txt
```

### 2-2. secrets.toml 수정
`C:\arum\.streamlit\secrets.toml` 파일을 열어서:

```toml
# Supabase 연결 설정
supabase_url = "https://your-supabase-url.supabase.co"
supabase_key = "your-supabase-anon-key"
```

위의 두 값을 1-2 단계에서 복사한 값으로 변경하세요.

**예시:**
```toml
supabase_url = "https://abc123def456.supabase.co"
supabase_key = "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9..."
```

## 3️⃣ 패키지 설치

```bash
pip install -r requirements.txt
```

## 4️⃣ Streamlit 앱 실행

```bash
streamlit run app.py
```

브라우저에서 `http://localhost:8501` 접속

## 🎯 기능

✅ **Supabase에서 실시간 데이터 로드**
- CSV 대신 Supabase의 `broadcast_schedule` 테이블에서 데이터 조회

✅ **데이터 편집 및 저장**
- 테이블에서 론칭여부를 수정 후 "💾 변경 내용 저장" 버튼으로 Supabase에 저장

✅ **필터 및 분석**
- 날짜, 카테고리, 난이도, 제작자로 필터링
- 대시보드에서 실시간 통계 확인

## ❓ 문제 해결

### "Supabase 연결 오류" 메시지가 나타나면:
1. `secrets.toml` 파일이 정확한 경로에 있는지 확인
2. Supabase URL과 API 키가 정확히 복사되었는지 확인
3. Supabase 프로젝트에서 `broadcast_schedule` 테이블이 있는지 확인

### 데이터가 보이지 않으면:
1. Supabase 프로젝트에 데이터가 로드되었는지 확인
2. API 키의 권한이 충분한지 확인
3. 테이블명이 정확한지 확인 (소문자: `broadcast_schedule`)

## 📝 데이터베이스 테이블 구조

```sql
broadcast_schedule (
  id: BIGINT (Primary Key)
  broadcast_date: DATE
  broadcast_time: TIME
  product_name: VARCHAR
  category: VARCHAR
  creator: VARCHAR
  launched: BOOLEAN
  difficulty: VARCHAR
  created_at: TIMESTAMP
)
```

## 🚀 배포 (Streamlit Cloud)

Streamlit Cloud에 배포할 경우:

1. GitHub 리포지토리에 코드 푸시
2. [Streamlit Cloud](https://share.streamlit.io) 접속
3. New app → 리포지토리 선택
4. Deploy 후 secrets 설정
   - App settings → Secrets 탭
   - `secrets.toml` 내용 복사 후 붙여넣기

---

✨ Supabase 연결이 완료되었습니다! 행운을 빕니다! 🎉
