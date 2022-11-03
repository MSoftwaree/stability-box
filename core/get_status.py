from graphql_api.client_ptf import *


class TDPClient(GQL_Client_for_ptf):

    def __init__(self, *jira_plugins):
        super().__init__(*jira_plugins)

    def get_tdp_last_exec_status(self,tdp_key):
        self.get_testplan_id(tdp_key)
        self.command = "getTestPlan"
        self.arguments = {"issueId": self.test_plan_id}
        data = self.send_query(testExecutions=Fields(results=Fields("issueId")),
                               tests=Fields(results=Fields("issueId")))
        execs = len(data["getTestPlan"]["testExecutions"]["results"])
        if execs > 99:
            print(" Too many executions in test plan (>99)")
            raise Exception
        exec_id = data["getTestPlan"]["testExecutions"]["results"][execs-1]["issueId"]
        test_id = data["getTestPlan"]["tests"]["results"][0]["issueId"]

        self.command = "getTestRun"
        self.arguments = {"testIssueId": test_id, "testExecIssueId": exec_id}

        status = self.send_query(status=Fields("name", "final"))
        return status["getTestRun"]["status"]["name"]
