from settings import Settings
from salesforceapi import SalesforceAPI
from togglapi import TogglReport
import json

settings = Settings()
settings.set('api_key', settings.get('api_key', 'Toggl API key: '))
settings.set('workspace_id', settings.get('workspace_id', 'Toggl workspace ID: '))
settings.set('target_org', settings.get('target_org', 'Salesforce target org: '))
settings.save_if_updated()

toggl_report = TogglReport(settings.data.get('api_key'), settings.data.get('workspace_id'))
report = toggl_report.get_report()

sf_api = SalesforceAPI(settings.data.get('target_org'))
sf_api.login()

with open('.dl/toInsert.json', 'w') as file:
    json.dump(report, file)

inserted_records = sf_api.bulk_insert_records(report)

with open('.dl/insert.json', 'w') as file:
    json.dump(inserted_records, file)

print(f'Records Inserted')

# deleted_records = sf_api.delete_bulk2_records('./report1708535746180.csv')
# print(f'deleted_records: {deleted_records}')