import boto3
import datetime
from datetime import datetime
import time
import traceback
import os

class Logs:
    @staticmethod
    def warning(logBody):
        print("[WARNING] {}".format(logBody))

    @staticmethod
    def critical(logBody):
        print("[CRITICAL] {}".format(logBody))

    @staticmethod
    def info(logBody):
        print("[INFO] {}".format(logBody))

class Cognito:
    USERPOOLID = ""
    REGION = ""
    ATTRIBUTES = ""

    # INIT userpool id, region and column names to be exported. 
    # Currently region is not used. The export lambda must be in the same region as the Cognito service
    def __init__(self, userPoolId, region, attributes):
        self.USERPOOLID = userPoolId
        self.REGION = region
        self.ATTRIBUTES = attributes
    
    def getAttributes (self):
        try:
            boto = boto3.client('cognito-idp')
            headers = boto.get_csv_header(
                UserPoolId=self.USERPOOLID
            )
            self.ATTRIBUTES = headers["CSVHeader"]
            return headers["CSVHeader"]
        except Exception as e:
            Logs.critical("There is an error listing users attributes")
            Logs.critical(traceback.format_exc())
            exit()

    # List all cognito users with only the predefined columns in ATTRIBUTES variable
    # As there is a limit of 60 users per query, a multiple queries are executed separated in so called pages.
    def listUsers (self):
        try:
            boto = boto3.client('cognito-idp')

            users = []
            next_page = None
            kwargs = {
                'UserPoolId': self.USERPOOLID,
            }
            users_remain = True
            while(users_remain):
                if next_page:
                    kwargs['PaginationToken'] = next_page
                response = boto.list_users(**kwargs)
                users.extend(response['Users'])
                next_page = response.get('PaginationToken', None)
                users_remain = next_page is not None
                # COOL DOWN BEFORE NEXT QUERY
                time.sleep(0.15)

            return users
        except Exception as e:
            Logs.critical("There is an error listing cognito users")
            Logs.critical(traceback.format_exc())
            exit()

    # List all cognito groups with only the predefined columns in ATTRIBUTES variable
    # As there is a limit of 60 groups per query, a multiple queries are executed separated in so called pages.
    def listGroups (self):
        try:
            boto = boto3.client('cognito-idp')
            groups = []
            next_page = None
            kwargs = {
                'UserPoolId': self.USERPOOLID,
            }
            groups_remain = True
            while(groups_remain):
                if next_page:
                    kwargs['NextToken'] = next_page
                response = boto.list_groups(**kwargs)
                groups.extend(response['Groups'])
                next_page = response.get('NextToken', None)
                groups_remain = next_page is not None
                # COOL DOWN BEFORE NEXT QUERY
                time.sleep(0.15)
            return groups
        except Exception as e:
            Logs.critical("There is an error listing cognito groups")
            Logs.critical(traceback.format_exc())
            exit()
    
    def deleteGroups (self, groups):
        try:
            boto = boto3.client('cognito-idp')
            for group in groups:
                response = boto.delete_group(
                    GroupName=group["GroupName"],
                    UserPoolId=self.USERPOOLID
                )
        except Exception as e:
            Logs.critical("There is an error listing cognito groups")
            Logs.critical(traceback.format_exc())
            exit()

    def deleteUsers (self, users):
        try:
            boto = boto3.client('cognito-idp')
            for user in users:
                response = boto.admin_delete_user(
                    UserPoolId=self.USERPOOLID,
                    Username=user["Username"]
                )
        except Exception as e:
            Logs.critical("There is an error listing cognito groups")
            Logs.critical(traceback.format_exc())
            exit()


def lambda_function(event, context): 
    ### MAIN ###
    # VARIABLES
    REGION = os.environ['REGION']
    COGNITO_ID = os.environ['COGNITO_ID']

    # INIT CLASSES
    cognito = Cognito(COGNITO_ID, REGION, [])
    # LIST ALL USERS
    user_records = cognito.listUsers()
    cognito.deleteUsers(user_records)


    # LIST ALL GROUPS
    group_records = cognito.listGroups()
    cognito.deleteGroups(group_records)