from toggl.TogglPy import Toggl
from datetime import datetime, timedelta

class TogglReport:

    def __init__(self, api_key, workspace_id):
        self.selectedDate = datetime.now() #- timedelta(days=1)
        self.toggl = Toggl()
        self.toggl.setAPIKey(api_key)
        self.workspace_id = workspace_id
        self.salesforce_lookup = {
            'Veevart_Acceptance_Criteria__c': 'Veevart_Acceptance_Criteria__c',
            'agf__ADM_Work__c':'Work__c',
            'agf__ADM_Epic__c':'Epic__c',
            'Case':'Case__c',
            'agf__PPM_Project__c':'Project__c',
            'agf__ADM_Build__c':'Build__c',
            'agf__ADM_Release__c':'Release__c',
            'Objective_Key_Result__c':'OKR_Objective_Key_Result__c',
            'Knowledge__kav':'Knowledge__c',
            'Review_Type':'Sub_Category__c'
        }

    def get_report(self):
        report = self.toggl.getDetailedReport(data={'since': self.selectedDate, 'until': self.selectedDate, 'workspace_id': self.workspace_id,'display_hours':'minutes', 'calculate':'time'})
        return self.process_report(report)

    def process_report(self, report):
        salesforce_data = []
        for toggl_record in report['data']:
            salesforce_record = {
                'Work_Done__c':(toggl_record['description']).replace("'",""),
                'Minutes_Spent__c': round(toggl_record['dur'] / (1000 * 60)),
                'Category__c': toggl_record['project'],
                'Day__c': self.selectedDate.strftime("%Y-%m-%d")
            }
            for toggl_tag in toggl_record['tags']:
                toggl_tag_parts = toggl_tag.split('/')
                salesforce_record[self.salesforce_lookup[toggl_tag_parts[0]]] = toggl_tag_parts[1]
            salesforce_data.append(salesforce_record)
        return salesforce_data