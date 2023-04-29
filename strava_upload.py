import re
import sys

from stravalib import Client

from strava_auth import Credentials


def main():
    credentials = Credentials.from_1password()

    client = Client()
    client.refresh_access_token(
        client_id=credentials.client_id,
        client_secret=credentials.client_secret,
        refresh_token=credentials.refresh_token,
    )

    for filename in sys.argv[1:]:
        upload_activity(client, filename)


def upload_activity(client: Client, filename: str):
    name = re.match(r"\d+ - (.+)\.fit", filename).group(1)

    print(name)
    with open(filename, "rb") as file:
        client.upload_activity(file, "fit", name)


if __name__ == "__main__":
    main()
