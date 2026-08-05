def echo_input():
    # Keep reading sentences until the user enters the quit command.
    while True:
        sentence = input()

        if sentence == "!quit":
            break

        print(sentence)


if __name__ == "__main__":
    echo_input()
