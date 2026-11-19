
while True:
    print("\n🎯 나만의 상식 퀴즈 게임 🎯")
    print("1. 퀴즈 풀기")
    print("2. 퀴즈 추가")
    print("3. 퀴즈 목록")
    print("4. 점수 확인")
    print("5. 종료")

    choice = input("번호를 선택하세요: ").strip()

    if choice == "1":
        print("퀴즈 풀기를 선택했어요!")
    elif choice == "2":
        print("퀴즈 추가를 선택했어요!")
    elif choice == "3":
        print("퀴즈 목록을 선택했어요!")
    elif choice == "4":
        print("점수 확인을 선택했어요!")
    elif choice == "5":
        print("게임을 종료합니다. 안녕!")
        break
    else:
        print("⚠️ 1~5 사이의 숫자를 입력해 주세요.")
