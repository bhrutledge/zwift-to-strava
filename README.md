# Upload Zwift activities to Strava

Single-use scripts to upload all of my Zwift activities to Strava, before I had connected the two.

Pre-requisites:

- Zwift username and password saved in 1Password
- [A Strava API application](https://developers.strava.com/docs/getting-started/#account) with Client ID and Client Secret saved in 1Password
- [The 1Password CLI](https://developer.1password.com/docs/cli/)

## Usage

Set up the environment:

```sh
python3 -m venv venv

source venv/bin/activate

pip install -r requirements.in
```

Sign in with 1Password:

```sh
eval $(op signin --account my)
```

Download all `.fit` files from Zwift:

```sh
export PROTOCOL_BUFFERS_PYTHON_IMPLEMENTATION=python

python3 zwift_download.py
```

Follow the instructions to authorize with Strava:

```sh
python3 strava_auth.py
```

Upload all `.fit` files to Strava:

```sh
python3 strava_upload.py *.fit
```
