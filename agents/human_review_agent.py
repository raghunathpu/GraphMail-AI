def review_email(email: dict, response: str) -> str:

    print("\n" + "=" * 60)
    print("Generated Draft")
    print("=" * 60)

    print(response)

    print("\nOptions:")
    print("1. Approve")
    print("2. Edit")

    choice = input("\nChoose option (1/2): ").strip()

    if choice == "2":
        print("\nEnter revised response:")
        return input("> ")

    return response
