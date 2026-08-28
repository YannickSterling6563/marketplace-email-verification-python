"""Run one marketplace email-verification delivery."""

import argparse

from src.verification import send_signup_verification


def main() -> None:
    parser = argparse.ArgumentParser(description="Send a marketplace verification email.")
    parser.add_argument("email", help="New account email address")
    parser.add_argument(
        "--app-url",
        default="https://marketplace.example",
        help="Public base URL for the marketplace",
    )
    args = parser.parse_args()
    sent = send_signup_verification(args.email, args.app_url)
    print(f"Verification email sent: {sent['message_id']}")
    print(f"Verification link: {sent['verification_url']}")


if __name__ == "__main__":
    main()
