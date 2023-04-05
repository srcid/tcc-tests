from __future__ import print_function

import os.path
from os import getenv

from dotenv import load_dotenv
from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError


class GoogleSpreadsheet:
    def __init__(self) -> None:
        self.SCOPES = ['https://www.googleapis.com/auth/spreadsheets']
        self.SPREADSHEET_ID = getenv('SPREADSHEET_ID')
        self.__login()

    def __login(self) -> None:
        self.creds = None
        if os.path.exists(getenv('TOKEN_PATH')):
            self.creds = Credentials.from_authorized_user_file(getenv('TOKEN_PATH'), self.SCOPES)
        if not self.creds or not self.creds.valid:
            if self.creds and self.creds.expired and self.creds.refresh_token:
                self.creds.refresh(Request())
            else:
                flow = InstalledAppFlow.from_client_secrets_file(getenv('CLIENT_SECRET_PATH'), self.SCOPES)
                self.creds = flow.run_local_server(port=0)
            with open(getenv('TOKEN_PATH'), 'w') as token:
                token.write(self.creds.to_json())

    def appendRow(self, groupName: str, model: str, instance:str, size:int, val:int, time:int, solver:str, val_status: int) -> None:
        try:
            service = build('sheets', 'v4', credentials=self.creds)
            sheet = service.spreadsheets()
            values = [[instance], [model], [size], [val], [time], [solver], [val_status]]
            resource = {
                'majorDimension': 'COLUMNS',
                'values': values,
            }
            request = sheet.values().append(
                spreadsheetId=self.SPREADSHEET_ID, 
                range=f'{groupName}!A:A',
                valueInputOption='RAW', 
                insertDataOption='INSERT_ROWS',
                body=resource,
            )
            response = request.execute()
            print(response)
        except HttpError as err:
            print(err)

if __name__ == '__main__':
    load_dotenv()
    sheet = GoogleSpreadsheet()
    sheet.appendRow('1','cs','instance_xy','115','40','996553242','GUROBI', 1)
    sheet.appendRow('1','cb','instance_xy','115','40','996553242','CBC', 0)