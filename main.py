
import json
from pathlib import Path


# 퀴즈 한 문제를 관리하는 클래스
class Quiz:
    def __init__(self, question, choices, answer):
        self.question = question
        self.choices = choices
        self.answer = answer

    def show(self):
        print("\n" + self.question)
        for number, choice in enumerate(self.choices, start=1):
            print(f"{number}. {choice}")

    def check_answer(self, user_answer):
        return user_answer == self.answer

    def to_dict(self):
        return {
            "question": self.question,
            "choices": self.choices,
            "answer": self.answer
        }


# 게임 전체를 관리하는 클래스
class QuizGame:
    def __init__(self):
        self.file_path = Path(__file__).resolve().parent / "state.json"
        self.quizzes = self.default_quizzes()
        self.best_score = None
        self.load_data()

    # 기본 퀴즈 5개
    def default_quizzes(self):
        return [
            Quiz(
                "대한민국의 수도는?",
                ["부산", "서울", "대전", "인천"], 2
            ),
            Quiz(
                "1년은 몇 개월일까요?",
                ["10개월", "11개월", "12개월", "13개월"], 3
            ),
            Quiz(
                "지구의 위성은?",
                ["태양", "달", "화성", "금성"], 2
            ),
            Quiz(
                "5 + 7은 얼마일까요?",
                ["10", "11", "12", "13"], 3
            ),
            Quiz(
                "물을 얼리면 무엇이 될까요?",
                ["수증기", "얼음", "모래", "구름"], 2
            )
        ]

    # 파일 저장
    def save_data(self):
        data = {
            "quizzes": [quiz.to_dict() for quiz in self.quizzes],
            "best_score": self.best_score
        }

        try:
            with open(self.file_path, "w", encoding="utf-8") as file:
                json.dump(data, file, ensure_ascii=False, indent=4)
            return True
        except OSError as error:
            print(f"⚠️ 저장 실패: {error}")
            return False

    # 파일 불러오기
    def load_data(self):
        if not self.file_path.exists():
            print("📂 기본 퀴즈 5개를 준비했어요.")
            self.save_data()
            return

        try:
            with open(self.file_path, "r", encoding="utf-8") as file:
                data = json.load(file)

            if not isinstance(data, dict):
                raise ValueError("데이터 형식이 잘못되었습니다.")

            items = data["quizzes"]
            score = data["best_score"]

            if not isinstance(items, list):
                raise ValueError("퀴즈 목록이 올바르지 않습니다.")

            if score is not None and (
                type(score) is not int or not 0 <= score <= 100
            ):
                raise ValueError("최고 점수 데이터가 올바르지 않습니다.")

            loaded_quizzes = []

            for item in items:
                question = item["question"]
                choices = item["choices"]
                answer = item["answer"]

                if (
                    not isinstance(question, str)
                    or not question.strip()
                    or not isinstance(choices, list)
                    or len(choices) != 4
                    or not all(
                        isinstance(choice, str) and choice.strip()
                        for choice in choices
                    )
                    or type(answer) is not int
                    or not 1 <= answer <= 4
                ):
                    raise ValueError("저장된 퀴즈가 올바르지 않습니다.")

                loaded_quizzes.append(Quiz(question, choices, answer))

            self.quizzes = loaded_quizzes
            self.best_score = score
            print("📂 저장된 데이터를 불러왔습니다.")

        except (OSError, UnicodeError, json.JSONDecodeError,
                ValueError, KeyError, TypeError) as error:
            print(f"⚠️ 데이터 파일 오류: {error}")
            print("기본 퀴즈로 초기화합니다.")
            self.quizzes = self.default_quizzes()
            self.best_score = None
            self.save_data()

    # 빈 입력 방지
    def get_text(self, message):
        while True:
            text = input(message).strip()

            if text:
                return text

            print("⚠️ 빈칸으로 둘 수 없어요. 다시 입력하세요.")

    # 숫자 입력 검사
    def get_number(self, message, minimum, maximum):
        while True:
            text = input(message).strip()

            if not text:
                print("⚠️ 숫자를 입력해 주세요.")
                continue

            try:
                number = int(text)
            except ValueError:
                print("⚠️ 숫자만 입력해 주세요.")
                continue

            if minimum <= number <= maximum:
                return number

            print(f"⚠️ {minimum}~{maximum} 사이의 숫자를 입력하세요.")

    # 메뉴 표시
    def show_menu(self):
        print("\n" + "=" * 40)
        print("       🎯 나만의 상식 퀴즈 게임 🎯")
        print("=" * 40)
        print("1. 퀴즈 풀기")
        print("2. 퀴즈 추가")
        print("3. 퀴즈 목록")
        print("4. 점수 확인")
        print("5. 종료")
        print("=" * 40)

    # 퀴즈 풀기
    def play_quiz(self):
        if not self.quizzes:
            print("⚠️ 등록된 퀴즈가 없어요.")
            return

        score = 0
        total = len(self.quizzes)

        print(f"\n📝 퀴즈 시작! 총 {total}문제입니다.")

        for index, quiz in enumerate(self.quizzes, start=1):
            print(f"\n[문제 {index}]")
            quiz.show()

            answer = self.get_number("정답 번호 (1~4): ", 1, 4)

            if quiz.check_answer(answer):
                print("✅ 정답입니다!")
                score += 1
            else:
                print(f"❌ 오답! 정답은 {quiz.answer}번입니다.")

        final_score = score * 100 // total

        print("\n" + "=" * 40)
        print(f"🏆 결과: {total}문제 중 {score}문제 정답!")
        print(f"🎯 점수: {final_score}점")
        print("=" * 40)

        if self.best_score is None or final_score > self.best_score:
            self.best_score = final_score
            print("🎉 새로운 최고 점수입니다!")
            self.save_data()

    # 퀴즈 추가
    def add_quiz(self):
        print("\n📌 새로운 퀴즈를 추가합니다.")

        question = self.get_text("문제를 입력하세요: ")

        choices = []

        for number in range(1, 5):
            choice = self.get_text(f"선택지 {number}: ")
            choices.append(choice)

        answer = self.get_number("정답 번호 (1~4): ", 1, 4)

        new_quiz = Quiz(question, choices, answer)
        self.quizzes.append(new_quiz)

        if self.save_data():
            print("✅ 퀴즈가 추가되고 저장되었습니다!")
        else:
            print("⚠️ 퀴즈는 추가됐지만 파일 저장에 실패했어요.")

    # 퀴즈 목록
    def show_quizzes(self):
        if not self.quizzes:
            print("⚠️ 등록된 퀴즈가 없습니다.")
            return

        print(f"\n📋 등록된 퀴즈 목록: 총 {len(self.quizzes)}개")

        for index, quiz in enumerate(self.quizzes, start=1):
            print(f"{index}. {quiz.question}")

    # 점수 확인
    def show_score(self):
        if self.best_score is None:
            print("\n🏆 아직 퀴즈를 풀지 않았어요.")
        else:
            print(f"\n🏆 최고 점수: {self.best_score}점")

    # 게임 실행
    def run(self):
        try:
            while True:
                self.show_menu()

                choice = self.get_number(
                    "번호를 선택하세요 (1~5): ", 1, 5
                )

                if choice == 1:
                    self.play_quiz()

                elif choice == 2:
                    self.add_quiz()

                elif choice == 3:
                    self.show_quizzes()

                elif choice == 4:
                    self.show_score()

                elif choice == 5:
                    print("👋 게임을 종료합니다. 안녕!")
                    break

        except (KeyboardInterrupt, EOFError):
            print("\n⚠️ 입력이 중단되었습니다.")
            print("저장 후 안전하게 종료합니다.")

        finally:
            self.save_data()


# 프로그램 시작
if __name__ == "__main__":
    game = QuizGame()
    game.run()
