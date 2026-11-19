import json
import random
from datetime import datetime
from pathlib import Path


class Quiz:
    def __init__(self, question, choices, answer, hint=""):
        self.question = question
        self.choices = choices
        self.answer = answer
        self.hint = hint

    def show(self):
        print(f"\n{self.question}")
        for number, choice in enumerate(self.choices, 1):
            print(f"{number}. {choice}")

    def check_answer(self, user_answer):
        return user_answer == self.answer

    def to_dict(self):
        return {
            "question": self.question,
            "choices": self.choices,
            "answer": self.answer,
            "hint": self.hint,
        }


class QuizGame:
    def __init__(self):
        self.file_path = Path(__file__).resolve().parent / "state.json"
        self.quizzes = self.default_quizzes()
        self.best_score = None
        self.history = []
        self.load_data()

    def default_quizzes(self):
        return [
            Quiz("대한민국의 수도는?", ["부산", "서울", "대전", "인천"], 2, "우리나라의 가장 큰 도시예요."),
            Quiz("1년은 몇 개월일까요?", ["10개월", "11개월", "12개월", "13개월"], 3, "계절 네 개에 각각 세 달씩 있어요."),
            Quiz("지구의 위성은?", ["태양", "달", "화성", "금성"], 2, "밤하늘에서 볼 수 있어요."),
            Quiz("5 + 7은 얼마일까요?", ["10", "11", "12", "13"], 3, "5에 5를 더하고 2를 더해 봐요."),
            Quiz("물을 얼리면 무엇이 될까요?", ["수증기", "얼음", "모래", "구름"], 2, "냉동실에서 만들 수 있어요."),
        ]

    def save_data(self):
        data = {
            "quizzes": [quiz.to_dict() for quiz in self.quizzes],
            "best_score": self.best_score,
            "history": self.history,
        }
        try:
            # 임시 파일에 먼저 저장하여 쓰기 중 오류로 원본이 손상될 가능성을 줄입니다.
            temporary = self.file_path.with_name("state.json.tmp")
            with temporary.open("w", encoding="utf-8") as file:
                json.dump(data, file, ensure_ascii=False, indent=4)
            temporary.replace(self.file_path)
            return True
        except OSError as error:
            print(f"⚠️ 저장 실패: {error}")
            return False

    def load_data(self):
        if not self.file_path.exists():
            print("📂 첫 실행: 기본 퀴즈 5개를 준비합니다.")
            self.save_data()
            return
        try:
            with self.file_path.open("r", encoding="utf-8") as file:
                data = json.load(file)
            if not isinstance(data, dict):
                raise ValueError("저장 형식이 올바르지 않습니다.")
            entries = data["quizzes"]
            best_score = data.get("best_score")
            history = data.get("history", [])  # 이전 버전 state.json도 읽을 수 있음
            if not isinstance(entries, list) or not isinstance(history, list):
                raise ValueError("목록 형식이 올바르지 않습니다.")
            if best_score is not None and (type(best_score) is not int or not 0 <= best_score <= 100):
                raise ValueError("최고 점수 형식이 올바르지 않습니다.")
            loaded = []
            for item in entries:
                if not isinstance(item, dict):
                    raise ValueError("퀴즈 데이터가 올바르지 않습니다.")
                question = item["question"]
                choices = item["choices"]
                answer = item["answer"]
                hint = item.get("hint", "")  # 이전 버전은 힌트가 없어도 됨
                if (not isinstance(question, str) or not question.strip()
                        or not isinstance(choices, list) or len(choices) != 4
                        or not all(isinstance(c, str) and c.strip() for c in choices)
                        or type(answer) is not int or not 1 <= answer <= 4
                        or not isinstance(hint, str)):
                    raise ValueError("저장된 퀴즈 내용이 올바르지 않습니다.")
                loaded.append(Quiz(question, choices, answer, hint))
            for record in history:
                if (not isinstance(record, dict)
                        or not isinstance(record.get("date"), str)
                        or type(record.get("question_count")) is not int
                        or record["question_count"] < 1
                        or type(record.get("correct_count")) is not int
                        or not 0 <= record["correct_count"] <= record["question_count"]
                        or type(record.get("score")) is not int
                        or not 0 <= record["score"] <= 100
                        or type(record.get("hints_used", 0)) is not int
                        or not 0 <= record.get("hints_used", 0) <= record["question_count"]):
                    raise ValueError("점수 기록 형식이 올바르지 않습니다.")
            self.quizzes = loaded
            self.best_score = best_score
            self.history = history
            print(f"📂 저장된 데이터 불러오기 성공! 퀴즈 {len(loaded)}개")
        except (OSError, UnicodeError, json.JSONDecodeError, ValueError, KeyError, TypeError) as error:
            print(f"⚠️ 파일을 읽을 수 없습니다: {error}")
            print("기본 퀴즈로 초기화합니다. 기존 파일은 백업을 시도합니다.")
            backup = self.file_path.with_name("state.invalid.json")
            try:
                if backup.exists():
                    backup = self.file_path.with_name(f"state.invalid.{datetime.now():%Y%m%d%H%M%S}.json")
                self.file_path.replace(backup)
            except OSError as backup_error:
                print(f"⚠️ 백업 실패: {backup_error}")
                print("원본 파일을 덮어쓰지 않고 메모리에서 기본 퀴즈로 실행합니다.")
                return
            self.quizzes = self.default_quizzes()
            self.best_score = None
            self.history = []
            self.save_data()

    def get_text(self, prompt):
        while True:
            value = input(prompt).strip()
            if value:
                return value
            print("⚠️ 빈칸은 입력할 수 없어요.")

    def get_number(self, prompt, minimum, maximum):
        while True:
            value = input(prompt).strip()
            try:
                number = int(value)
            except ValueError:
                print("⚠️ 숫자를 입력해 주세요.")
                continue
            if minimum <= number <= maximum:
                return number
            print(f"⚠️ {minimum}~{maximum} 사이의 숫자를 입력해 주세요.")

    def show_menu(self):
        print("\n========== 🎯 상식 퀴즈 게임 ==========")
        print("1. 퀴즈 풀기 (랜덤·문제 수·힌트)")
        print("2. 퀴즈 추가")
        print("3. 퀴즈 목록")
        print("4. 최고 점수 확인")
        print("5. 종료")
        print("6. 퀴즈 삭제 [보너스]")
        print("7. 점수 기록 보기 [보너스]")
        print("=======================================")

    def play_quiz(self):
        if not self.quizzes:
            print("⚠️ 퀴즈가 없습니다. 먼저 퀴즈를 추가해 주세요.")
            return
        amount = self.get_number(f"몇 문제를 풀까요? (1~{len(self.quizzes)}): ", 1, len(self.quizzes))
        selected = random.sample(self.quizzes, amount)
        earned_points = 0
        correct_count = 0
        hints_used = 0
        print("\n📝 무작위로 문제를 골랐어요!")
        for index, quiz in enumerate(selected, 1):
            print(f"\n[문제 {index}/{amount}]")
            quiz.show()
            used_hint = False
            while True:
                prompt = "정답(1~4)"
                if quiz.hint and not used_hint:
                    prompt += " 또는 힌트(H)"
                answer_text = input(prompt + ": ").strip()
                if answer_text.lower() == "h":
                    if quiz.hint and not used_hint:
                        print(f"💡 힌트: {quiz.hint} (맞히면 이 문제는 80점 기준)")
                        used_hint = True
                        hints_used += 1
                    else:
                        print("⚠️ 사용할 수 있는 힌트가 없어요.")
                    continue
                try:
                    answer = int(answer_text)
                except ValueError:
                    print("⚠️ 1~4 숫자를 입력해 주세요.")
                    continue
                if 1 <= answer <= 4:
                    break
                print("⚠️ 1~4 사이의 숫자를 입력해 주세요.")
            if quiz.check_answer(answer):
                correct_count += 1
                earned_points += 80 if used_hint else 100
                print("✅ 정답입니다!")
            else:
                print(f"❌ 오답입니다. 정답은 {quiz.answer}번입니다.")
        score = earned_points // amount
        print(f"\n🏆 결과: {amount}문제 중 {correct_count}개 정답 / {score}점")
        print(f"💡 사용한 힌트: {hints_used}개 (정답 시 문제당 20점 감점)")
        record = {
            "date": datetime.now().astimezone().isoformat(timespec="seconds"),
            "question_count": amount,
            "correct_count": correct_count,
            "score": score,
            "hints_used": hints_used,
        }
        self.history.append(record)
        if self.best_score is None or score > self.best_score:
            self.best_score = score
            print("🎉 새로운 최고 점수입니다!")
        self.save_data()

    def add_quiz(self):
        question = self.get_text("문제를 입력하세요: ")
        choices = [self.get_text(f"선택지 {i}: ") for i in range(1, 5)]
        answer = self.get_number("정답 번호(1~4): ", 1, 4)
        hint = input("힌트(없으면 Enter): ").strip()
        self.quizzes.append(Quiz(question, choices, answer, hint))
        if self.save_data():
            print("✅ 퀴즈가 추가되고 저장됐어요!")
        else:
            print("⚠️ 메모리에는 추가했지만 파일 저장에 실패했어요.")

    def show_quizzes(self):
        if not self.quizzes:
            print("등록된 퀴즈가 없습니다.")
            return
        print(f"\n📋 등록된 퀴즈 {len(self.quizzes)}개")
        for i, quiz in enumerate(self.quizzes, 1):
            print(f"{i}. {quiz.question}")

    def show_score(self):
        if self.best_score is None:
            print("🏆 아직 퀴즈를 풀지 않았어요.")
        else:
            print(f"🏆 최고 점수: {self.best_score}점")

    def delete_quiz(self):
        if not self.quizzes:
            print("⚠️ 삭제할 퀴즈가 없어요.")
            return
        self.show_quizzes()
        number = self.get_number("삭제할 문제 번호(0은 취소): ", 0, len(self.quizzes))
        if number == 0:
            print("삭제를 취소했어요.")
            return
        target = self.quizzes[number - 1]
        confirmation = input(f"'{target.question}' 삭제할까요? (y/N): ").strip().lower()
        if confirmation != "y":
            print("삭제를 취소했어요.")
            return
        del self.quizzes[number - 1]
        if self.save_data():
            print("🗑️ 퀴즈가 삭제되고 저장됐어요!")
        else:
            print("⚠️ 메모리에서는 삭제됐지만 파일 저장에 실패했어요.")

    def show_history(self):
        if not self.history:
            print("📋 아직 저장된 게임 기록이 없어요.")
            return
        print(f"\n📋 게임 기록 총 {len(self.history)}회")
        for index, item in enumerate(self.history, 1):
            print(f"{index}. {item['date']} | {item['question_count']}문제 | "
                  f"{item['correct_count']}개 정답 | {item['score']}점 | "
                  f"힌트 {item.get('hints_used', 0)}회")

    def run(self):
        try:
            while True:
                self.show_menu()
                selection = self.get_number("선택(1~7): ", 1, 7)
                if selection == 1:
                    self.play_quiz()
                elif selection == 2:
                    self.add_quiz()
                elif selection == 3:
                    self.show_quizzes()
                elif selection == 4:
                    self.show_score()
                elif selection == 5:
                    print("👋 게임을 종료합니다.")
                    break
                elif selection == 6:
                    self.delete_quiz()
                elif selection == 7:
                    self.show_history()
        except (KeyboardInterrupt, EOFError):
            print("\n⚠️ 입력이 중단됐어요. 저장 후 안전하게 종료합니다.")
        finally:
            self.save_data()


if __name__ == "__main__":
    QuizGame().run()
