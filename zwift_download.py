import json
import subprocess
from dataclasses import dataclass

import requests
from zwift import Client


def main():
    credentials = Credentials.from_1password()
    client = Client(credentials.username, credentials.password)

    for activity in get_activities(client):
        download_fit_file(activity)


@dataclass
class Credentials:
    username: str
    password: str

    @classmethod
    def from_1password(cls) -> "Credentials":
        user_item_name = "Zwift"

        # TODO: Maybe use "op run" and retrieve credentials from an environment variable
        process = subprocess.run(
            f"op item get '{user_item_name}' "
            "--fields label=username,label=password --format=json",
            shell=True,
            check=True,
            capture_output=True,
        )

        output = json.loads(process.stdout.decode().strip())

        return cls(**{field["id"]: field["value"] for field in output})


def get_activities(client: Client):
    profile = client.get_profile("me")

    start = 0
    limit = 50

    while True:
        yield from profile.get_activities(start, limit)
        start += limit


def download_fit_file(activity):
    filename = f"{activity['id']} - {activity['name']}.fit"
    print(filename)

    bucket = activity["fitFileBucket"]
    key = activity["fitFileKey"]
    url = f"https://{bucket}.s3.amazonaws.com/{key}"

    response = requests.get(url)
    response.raise_for_status()
    with open(filename, "wb") as f:
        f.write(response.content)


if __name__ == "__main__":
    main()
