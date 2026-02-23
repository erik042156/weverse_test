# weverse_test

📌 실행 환경
OS: macOS
Python 3.10 이상
Selenium
Chrome 브라우저

📦 설치 방법
1️⃣ 가상환경 생성 (선택)
python -m venv venv
source venv/bin/activate
2️⃣ 라이브러리 설치
pip install selenium

▶ 실행 방법
python test2_1.py
python test2_2.py

또는 PyCharm에서 실행 가능합니다.

🧪 테스트 시나리오
2_1
- 회원가입 후 wid 값 추출 
- 이메일 인증코드 수기 입력
(Gmail API 연동 가능하나 시간 관계상 미구현)
- 회원가입 완료 후 API 토큰 분석
- API request를 통해 wid 값 추출

✅ 실행 결과
콘솔 로그를 통해 id / pw / wid 확인 가능

2_2
- 커뮤니티 가입 후 커뮤니티 프로필로 이동 > 포스트 등록/수정/삭제
커뮤니티 가입 시 실제 존재하는 아티스트명 입력 필요
ㄴ 테스트 대상: SEVENTEEN
- 포스트 작성 → 등록 / 수정 / 삭제 검증

✅ 실행 결과
콘솔 로그를 통해 포스트 정상 등록 및 삭제 여부 확인 가능
