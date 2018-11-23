# OpenSRS_HostedEmail_Migration_Bulk_Token-SSO_Generator
# v 1.0
# Written by Tudor Ciolac
# October 1st 2018
# Prerequisites python3
# Dependancies. Stock Python 3 Libs & requests (obtained via pip installer: https://stackoverflow.com/questions/6587507/how-to-install-pip-with-python-3, https://stackoverflow.com/questions/17309288/importerror-no-module-named-requests)

#Purpose: Creates a CSV. Collumn one contains list of target emmail addresses provided by the user. Collumn two will include a Single Sign On (SSO) password, or Multi-Use Time Based Token. Additional options include a secondary SSO in collumn three.

#Parameters Needed:
#Source File: An authorized list of email addresses that require temporary passwords. Use line-breaks as delimiters
#Desination File: Output of results
#cust: Either Cluster A (admin.a.hostedemail.com) or B (admin.b.hostedemail.com). Depends on Reseller's defaulted assignment at time of service signup. To determine see: https://help.opensrs.com/hc/en-us/articles/204770158-Which-email-cluster-am-I-on-
#aUsername: Admin email address used to manage the end-user on the respective cluster. Make sure admin's permission profile is sufficient to support the request for desired users.
#option: SSO or Token?
#aDuration: if Token, anywhere from 1-744hours
#aBackup: if SSO, determines whether a backup SSO will be generated (ALL SSOs last 24 hours!)

#Features:
#Exception handling for invalid inputs
#Hidden password input
#Authorization check prior to file write
#Dynamic filename based on epoch time of run
