import re


PASSWORD_RULES = [
    (re.compile(r"[a-z]"), "영문 소문자를 1개 이상 포함해야 합니다."),
    (re.compile(r"[A-Z]"), "영문 대문자를 1개 이상 포함해야 합니다."),
    (re.compile(r"\d"), "숫자를 1개 이상 포함해야 합니다."),
    (re.compile(r"[^A-Za-z0-9]"), "기호를 1개 이상 포함해야 합니다."),
]


def validate_password(password):
    errors = [
        message
        for pattern, message in PASSWORD_RULES
        if not pattern.search(password)
    ]

    return len(errors) == 0, errors


def main():
    password = input("비밀번호를 입력하세요: ")
    is_valid, errors = validate_password(password)

    if is_valid:
        print("사용 가능한 비밀번호입니다.")
        return

    print("사용할 수 없는 비밀번호입니다.")
    for error in errors:
        print(f"- {error}")


if __name__ == "__main__":
    main()
