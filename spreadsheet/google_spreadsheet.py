from __future__ import print_function

import os.path
from logging import debug, error
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
                authorization_url, state = flow.authorization_url(access_type='offline', include_granted_scopes='true')
                self.creds = flow.run_local_server(port=0)
            with open(getenv('TOKEN_PATH'), 'w') as token:
                token.write(self.creds.to_json())
        self.service = build('sheets', 'v4', credentials=self.creds)
        self.sheets = (
            [sheet['properties']['title'] 
             for sheet in 
             self.service.spreadsheets()
                .get(spreadsheetId=self.SPREADSHEET_ID)
                .execute()
                .get('sheets', [])
            ]
        )


    def appendRow(self, groupName: str, model: str, instance:str, size:int, val:int, time:int, solver:str, val_status: int) -> None:
        try:
            if groupName not in self.sheets:
                debug('Sheet do not exist, creating it before insert.')
                request = {
                    "requests": [
                        {
                            "addSheet": {
                                "properties": {
                                    "title": groupName,
                                }
                            }
                        }
                    ]
                }
                response = (
                    self.service.spreadsheets()
                        .batchUpdate(spreadsheetId=self.SPREADSHEET_ID, body=request)
                        .execute()
                )
                self.sheets.append(groupName)
                debug(response)
            
            sheet = self.service.spreadsheets()
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
            debug(response)
        except HttpError as err:
            error(err)

if __name__ == '__main__':
    load_dotenv()
    sheet = GoogleSpreadsheet()
    sheet.appendRow('1','cs','instance_xy','115','40','996553242','GUROBI', 1)
    sheet.appendRow('1','cb','instance_xy','115','40','996553242','CBC', 0)