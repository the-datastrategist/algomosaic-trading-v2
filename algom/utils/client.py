#!/usr/bin/env python

import os
from google.cloud import bigquery, storage
from google.oauth2 import service_account

from algom import configs

PROJECT_ID = configs.GOOGLE_PROJECT_ID
GOOGLE_APPLICATION_CREDENTIALS = configs.GOOGLE_APPLICATION_CREDENTIALS
CONFIG_FILE = configs.ALGOM_CONFIG_FILEPATH


class googleClient():
    """Set up configurations for google.cloud.bigquery using a GCP Service Account.

    Args:
        project (int): The first parameter. Defaults to the active GCP Project.
        credentials_file (str): File location of the GCP credentials file.

    Returns:
        None: Returns None by default; however, it adds the following
            attributes to the gClient class:
            bigquery_client: Client for GCP BigQuery instance.
            storage_client: Client for GCP Storage instance.

    Documentation:
        - Creating a Service Account:
            https://support.google.com/a/answer/7378726?hl=en
    """
    def __init__(self):
        self.project_id = PROJECT_ID
        self.credentials_filepath = GOOGLE_APPLICATION_CREDENTIALS
        self.credentials = self._get_credentials()

    def _get_credentials(self):
        if os.path.exists(self.credentials_filepath):
            self.credentials = \
                service_account.Credentials.from_service_account_file(
                    self.credentials_filepath)
        else:
            self._update_credentials_file()
            self.credentials = \
                service_account.Credentials.from_service_account_file(
                    self.credentials_filepath)
        return self.credentials

    def _update_credentials_file(self):
        """
        Check if creds file is available; otherwise,
        prompt for Service Key upload
        """
        cwd = os.getcwd()
        credentials_filepath = input(
            "Enter the file path and name for GCP's Service Account"
            "credentials file. See for more details:\n"
            "https://console.cloud.google.com/"
            "iam-admin/serviceaccounts?project=<projectId> \n"
            "The current directory is: {}.\n".format(cwd))
        self._update_config_file(
            file=CONFIG_FILE,
            variable='GOOGLE_APPLICATION_CREDENTIALS',
            replace_text=credentials_filepath)
        self.credentials_filepath = credentials_filepath

    def _update_config_file(self, file, variable, replace_text):
        import re
        f = open(file, "r")
        contents = f.read()
        new_contents = re.sub(
            r"{}\s*=\s*.*".format(variable),
            "{} = '{}'".format(variable, replace_text),
            contents)
        f = open(file, "w")
        f.write(new_contents)
        f.close()


class storageClient():
    def __init__(self):
        gClient = googleClient()
        self.project_id = gClient.project_id
        self.credentials_filepath = gClient.credentials_filepath
        self.credentials = gClient.credentials
        self.storage_client = self._get_storage_client()

    def _get_storage_client(self, project_id=PROJECT_ID):
        credentials = service_account.Credentials.from_service_account_file(
            configs.GOOGLE_APPLICATION_CREDENTIALS
        )
        self.storage_client = storage.Client(
            project=project_id,
            credentials=credentials)
        return self.storage_client


class bqClient():
    """ Google BigQuery client

    Class containing pertinent information for Google BigQuery
    authentication for a given Service Account.
    """
    def __init__(self):
        gClient = googleClient()
        self.project_id = gClient.project_id
        self.credentials_filepath = gClient.credentials_filepath
        self.credentials = gClient.credentials
        self.bq_client = self._get_bq_client()

    def _get_bq_client(self, project_id=PROJECT_ID):
        credentials = service_account.Credentials.from_service_account_file(
            configs.GOOGLE_APPLICATION_CREDENTIALS,
            scopes=["https://www.googleapis.com/auth/cloud-platform"]
        )
        self.bq_client = bigquery.Client(
            project=project_id,
            credentials=credentials)
        return self.bq_client
