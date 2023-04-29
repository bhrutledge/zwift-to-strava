import json
import subprocess
from dataclasses import dataclass

from stravalib import Client


def main():
    credentials = Credentials.from_1password()

    client = Client()

    url = client.authorization_url(
        client_id=credentials.client_id,
        redirect_uri="http://localhost:5000/authorization",
        scope=["read", "activity:read", "activity:write"],
    )

    print(f"Open URL to authorize app:\n{url}\n")
    code = input("Enter 'code' from redirect: ")

    token_response = client.exchange_code_for_token(
        client_id=credentials.client_id,
        client_secret=credentials.client_secret,
        code=code,
    )

    print("Save refresh token to 1Password:")
    print(token_response)


@dataclass
class Credentials:
    client_id: str
    client_secret: str
    refresh_token: str

    @classmethod
    def from_1password(cls) -> "Credentials":
        user_item_name = "Strava"

        # TODO: Maybe use "op run" and retrieve credentials from an environment variable
        process = subprocess.run(
            f"op item get '{user_item_name}' "
            "--fields label='Client Id',label='Client Secret',label='Refresh Token' "
            "--format=json",
            shell=True,
            check=True,
            capture_output=True,
        )

        output = json.loads(process.stdout.decode().strip())

        return cls(*[field["value"] for field in output])


if __name__ == "__main__":
    main()
