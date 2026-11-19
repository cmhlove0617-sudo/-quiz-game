
# 🎯 Python 상식 퀴즈 게임 개발 완료 보고서

## 1. 프로젝트 개요

| 항목 | 내용 |
|---|---|
| 프로젝트명 | 나만의 상식 퀴즈 게임 |
| 개발 언어 | Python 3.10 이상 |
| 개발 도구 | VS Code, Git, GitHub |
| 실행 방식 | 터미널 기반 콘솔 프로그램 |
| 데이터 저장 | JSON 파일 |
| GitHub | [프로젝트 저장소](https://github.com/cmhlove0617-sudo/-quiz-game) |

### 프로젝트 목표

Python의 기본 문법을 배우고 직접 실행할 수 있는
퀴즈 게임을 개발하는 것이 목표입니다.

클래스와 객체, 조건문, 반복문, 파일 저장 기능을
활용하여 프로그램을 구현했습니다.

또한 Git과 GitHub를 이용하여 개발 과정을 기록하고,
브랜치를 생성하고 병합하는 방법을 학습했습니다.

---

## 2. 퀴즈 주제 선정 이유

**주제: 초등학생 상식 퀴즈**

일상생활에서 쉽게 접할 수 있는 과학, 수학,
생활 상식 등의 문제를 통해 누구나 재미있게
학습할 수 있도록 주제를 선정했습니다.

기본 퀴즈 5개를 준비했으며,
사용자가 새로운 문제를 직접 추가할 수 있습니다.

---

## 3. 개발 환경

- Python 3.10 이상
- Visual Studio Code
- Git
- GitHub
- Windows PowerShell

### 개발 환경 확인 화면

![개발 환경](docs/screenshots/environment.png)

---

## 4. 프로젝트 파일 구조

```text
-quiz-game/
├── main.py
├── state.json
├── README.md
├── REPORT.md
├── .gitignore
└── docs/
    └── screenshots/
        ├── environment.png
        ├── menu.png
        ├── play.png
        ├── add_quiz.png
        ├── score.png
        └── git-log.png
```

---

## 5. 프로그램 설계

### Quiz 클래스

하나의 퀴즈 문제를 관리합니다.

- question: 문제 내용
- choices: 선택지 4개
- answer: 정답 번호
- show(): 문제와 선택지 출력
- check_answer(): 정답 여부 확인
- to_dict(): JSON 저장용 데이터 변환

### QuizGame 클래스

게임 전체의 실행과 데이터를 관리합니다.

- show_menu(): 메뉴 출력
- play_quiz(): 퀴즈 진행
- add_quiz(): 퀴즈 추가
- show_quizzes(): 퀴즈 목록 확인
- show_score(): 최고 점수 확인
- save_data(): 파일 저장
- load_data(): 파일 불러오기
- run(): 게임 실행

---

## 6. 주요 기능 및 실행 결과

### 6.1 게임 메뉴

사용자는 1~5번 메뉴를 선택할 수 있습니다.

![게임 메뉴](docs/screenshots/menu.png)

### 6.2 퀴즈 풀기

등록된 퀴즈를 풀고 정답 여부와
최종 점수를 확인할 수 있습니다.

![퀴즈 실행](docs/screenshots/play.png)

### 6.3 퀴즈 추가

새로운 문제, 선택지 4개, 정답 번호를 입력하여
퀴즈를 등록할 수 있습니다.

![퀴즈 추가](docs/screenshots/add_quiz.png)

### 6.4 최고 점수 확인

퀴즈를 풀고 얻은 최고 점수를 저장하여
다음 실행에서도 확인할 수 있습니다.

![최고 점수](docs/screenshots/score.png)

---

## 7. 데이터 저장 및 불러오기

프로젝트 루트의 state.json 파일에
퀴즈 목록과 최고 점수를 저장합니다.

### 데이터 구조 예시

```json
{
  "quizzes": [
    {
      "question": "대한민국의 수도는?",
      "choices": ["부산", "서울", "대전", "인천"],
      "answer": 2
    }
  ],
  "best_score": 100
}
```

- quizzes: 저장된 퀴즈 목록
- best_score: 최고 점수
- 파일 인코딩: UTF-8

프로그램을 종료한 뒤 다시 실행해도
저장된 데이터를 불러올 수 있습니다.

파일이 없거나 손상된 경우에는
기본 퀴즈 데이터로 초기화하도록 구현했습니다.

---

## 8. 예외 처리

다음 상황을 처리하도록 구현했습니다.

| 테스트 항목 | 처리 방식 |
|---|---|
| 문자 입력(abc) | 숫자 재입력 안내 |
| 범위 밖 숫자(9) | 허용 범위 안내 |
| 빈 입력 | 재입력 안내 |
| 입력 앞뒤 공백 | 공백 제거 후 처리 |
| Ctrl+C | 데이터 저장 후 안전 종료 |
| EOFError | 안전 종료 |
| JSON 파일 손상 | 기본 데이터로 초기화 |

---

## 9. Git 및 GitHub 활용

### Git 작업 내용

1. Git 저장소 초기화
2. 파일 추가 및 기능별 커밋
3. GitHub 원격 저장소 연결
4. main 브랜치에 코드 업로드
5. feature/quiz-play 브랜치 생성
6. 퀴즈 게임 기능 개발
7. feature/quiz-play 브랜치 병합
8. GitHub 저장소 복제(clone)
9. 복제 폴더에서 README 수정 및 push
10. 원본 폴더에서 pull 실습

### Git 커밋 그래프

![Git 커밋 그래프](docs/screenshots/git-log.png)

10개 이상의 커밋을 생성하고,
브랜치 생성 및 병합 기록을 남겼습니다.

---

## 10. 기능 테스트 결과

| 테스트 항목 | 결과 |
|---|---|
| 게임 메뉴 출력 | 성공 |
| 퀴즈 풀기 | 성공 |
| 정답 및 점수 계산 | 성공 |
| 새로운 퀴즈 추가 | 성공 |
| 퀴즈 목록 확인 | 성공 |
| 최고 점수 확인 | 성공 |
| 프로그램 재시작 후 데이터 유지 | 성공 |
| GitHub push | 성공 |
| 브랜치 병합 | 성공 |
| Git clone 및 pull | 성공 |

※ 예외 입력 및 손상 파일에 대한 모든 세부 테스트는
제출 전 추가 확인이 필요합니다.

---

## 11. 학습 성과

이번 프로젝트를 진행하며 다음 내용을 학습했습니다.

- 변수와 자료형의 사용 방법
- if, elif, else 조건문
- for, while 반복문
- 함수와 반환값
- 클래스와 객체
- JSON 파일 저장 및 불러오기
- try/except 오류 처리
- Git 커밋과 GitHub 업로드
- 브랜치 생성 및 병합
- clone과 pull을 이용한 동기화

---

## 12. 프로젝트 마무리

이번 프로젝트를 통해 Python으로 직접
동작하는 프로그램을 구현하는 경험을 했습니다.

또한 Git과 GitHub를 이용하여 코드 변경 이력을
관리하고 원격 저장소와 동기화하는 방법을
실습했습니다.

앞으로 퀴즈 문제를 더욱 다양하게 추가하고
게임 기능을 확장할 수 있습니다.

### GitHub 저장소

https://github.com/cmhlove0617-sudo/-quiz-game

