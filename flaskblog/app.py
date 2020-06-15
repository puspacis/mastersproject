import os
from flask import Flask, render_template
import googleapiclient.discovery
from google.oauth2 import service_account


def get_credentials():
    scopes = ["https://www.googleapis.com/auth/spreadsheets.readonly"]
    GOOGLE_PRIVATE_KEY = "-----BEGIN PRIVATE KEY-----\nMIIEvQIBADANBgkqhkiG9w0BAQEFAASCBKcwggSjAgEAAoIBAQDi3EQPyamRoh8Q\n1penpE6Z7ck+nTOdEjTANUfF9LiRuZ8mm4qxFf84RocdBXdiMOueeLwC5ZFrYlrI\ntgX7BLg378eU2K+FV6Q73qqhMDYdmmNUkzwOKOWQLeEv+5JEgC0+G1K8D+YznhPx\nU/AyjMKdRErhy5FjKW1X3ITvo0Ol7ULd5bByyMHNUB78ihBcUw6XXUgScl13/enO\nfNTh3ZrXjrwIfip/ZJXszx11ISRMRZRYcjyj+T+Xkot2buSCxDubMALSEaoXzCia\n59WovQXHbpGmfALuF9ub6E2r7mddfgFSvWGNMh2AN1SoQmu4yzjIg1ofiN0X99+S\ncnzdURyXAgMBAAECggEATanikxUSvAyoXfdZC8cwMXo6PvlKRieJb5PN8nMJDLpj\nRbBSFrXVHcrnToQkjrT4tNPYaZV15zFQqw3Fll3TQzMPPGHCFQAf9W8RMwVyQUgt\nYTLWiHJvxKAwS2DwfgrzciOge0lmIZ2obiGyRVvy9CwBBrPOHgh8qmuQBwn5ir+9\n2ZIVZ54L1BTBuGIE0kEesPUQkL9SDtsKrhUrnaAUdDAHWfDul8TBQzeYLtHnFrSj\n+oq9/vQ3JHHBHBfyG+G2DQSaAhO7+C/3OfM/GHXyXqnEUOk8TOucbe/R5PDL2tKH\nYZRs1QRRa58uSHQ0QHszCozThNeBYd+AM9kTNuanYQKBgQD6OdAkHl2YI3tytwgq\n5UOSzCb1F7ueof3uqx/Xx5iIb2eQ1GIK4m+Yx9AFL5kdYUuNUJY3n2uFO38g5BHB\nXIk2AjFt0geTO+4dD5rBe/1pnd6XHX/3dXLm+5q/XU59KIXkrmdXiVvqkeyEZPzx\nONtoP4bm4DFJuO9iAxuV8uETUwKBgQDoGGx1zzLwfyZZgvFt1kp8i8Yqv78/kG47\nY0Mi8+OmgjVeTIZHOLD42sZHWHLT7hVV9AUufG1YOWDlmT5ZpYZxvEpPu3eDTXfo\nSZh3OA43kBIFdVdbxlOESUNJ4ffyeOa+QVfWVT88j88DeeAOagkPOcz1wu+gOerB\nKVzv8/SNLQKBgDoJ6NZH2MuuBzcvbwyMCuVkxvB4ZcNAraaLOKKTIDUdKfd025zM\nsrfMONrLFIe1BpIri/ww1P6dMzqMy/V+ojDNx2tCmRE0iGFjOjEAsmGqBXQlmoXq\nTxF2cIlMeiUbnhrRvRSXvqMk36hByE2nM3T1rzOj8qq344ZnVCGuqTgTAoGBAJBv\nIo/t8XVYqzTpF/WSdagsE5Zm3U1hRDgQ/aayv+jO/wc/+BA6Z2d2Pg4ILO1WLFDh\nGphjNmjAzFwVkYeYSqJc2qHjt+wuOYCEzCzk5XQOZCihbUvfj/my3f0McpCiTHX5\nk//97OxzUhCHt7dApYKkJbiLJzQ+1qh+ZSeuWXHBAoGAdpdaxqipUx4sigPXu5Pm\nti4eoqTykyJnZh9RN9uXfFEHqC/PTjfMAYZdxq8PxFlT3unU2xHMxxPq6Ke0rim/\nIDznD8WeniBxwdXwKPLZIPy7xp3Up7h+CcX0+oB8+q00As8IM0hQWOkWBcnGF+cd\nWaA1elBSiA1hzfrAu8n71c8=\n-----END PRIVATE KEY-----\n"
    # The environment variable has escaped newlines, so remove the extra backslash
    GOOGLE_PRIVATE_KEY = GOOGLE_PRIVATE_KEY.replace('\\n', '\n')

    account_info = {
      "private_key": GOOGLE_PRIVATE_KEY,
      "client_email": "ashish@flask-278914.iam.gserviceaccount.com",
      "token_uri": "https://accounts.google.com/o/oauth2/token",
    }

    credentials = service_account.Credentials.from_service_account_info(account_info, scopes=scopes)
    return credentials


def get_service(service_name='sheets', api_version='v4'):
    credentials = get_credentials()
    service = googleapiclient.discovery.build(service_name, api_version, credentials=credentials)
    return service


app = Flask(__name__)


@app.route('/', methods=['GET'])
def homepage():
    service = get_service()
    spreadsheet_id = "1P7SQEXHAaYlm4IszRkGmtu0sM7ABZYL3cwKBte2aB58"
    range_name = "XR-Hardware!A:Z"

    result = service.spreadsheets().values().get(
        spreadsheetId=spreadsheet_id, range=range_name).execute()
    values = result.get('values', [])

    return render_template('index.html', values=values)


if __name__ == '__main__':
    app.run(debug=True)
