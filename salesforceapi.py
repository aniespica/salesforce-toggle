from simple_salesforce import Salesforce
import json
import subprocess

class SalesforceAPI:
    def __init__(self, target_org):
        self.target_org = target_org
        self.sf = None

    def login(self):
        command = [f'sf org display --target-org {self.target_org} --verbose --json > .dl/auth.json']
        subprocess.run(command, shell=True, check=True, capture_output=True, text=True)

        with open('.dl/auth.json') as file:
            data = json.load(file)

        access_token = data['result']['accessToken']
        instance_url = data['result']['instanceUrl'].replace('https://','')

        self.sf = Salesforce(session_id=access_token, instance=instance_url)

    def bulk_insert_records(self, salesforce_data):
        if self.sf is None:
            self.login()
        return self.sf.bulk.Product_Time_Spent__c.insert(salesforce_data,batch_size='auto',use_serial=True)
    
    def bulk2_delete_records(self, salesforce_data_csv):
        if self.sf is None:
            self.login()
        return self.sf.bulk2.Contact.delete(salesforce_data_csv)