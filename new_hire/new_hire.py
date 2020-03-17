#!/usr/bin/env python
# coding: utf-8

## Define functions
def get_employees(filepath):
    """ takes a Toolbox csv filepath, retrieves it and exports as dataframe
    """
    import pandas as pd
    
    if not filepath:
        print("Please provide a Toolbox filepath to 'employees.csv'")
        return
    try:
        df =pd.read_csv(filepath, usecols=['employeeID','mail','hireDate','jobTitle','deptID'], parse_dates=['hireDate'],infer_datetime_format=True)
        return df.drop_duplicates()
    except:
        print("Error: retrieving employees.csv")

def new_hires(df, last_runtime):
    """ selects new hires from employee.csv
    """
    if not last_runtime:
        print("Please provide a last_runtime value e.g. '1999-01-01'")
        return
    try:
        return df[df.hireDate >= last_runtime]
    except:
        print("Error: selecting new hires")

def hires_by_deptID(df):
    """ selects new hires by deptID
    """
    deptID_list = ['PH06'] #`PH06`= Computational Biology 
    try:
        return df[df.deptID.isin(deptID_list)]
    except:
        print("Error: selecting by deptID")

def hires_by_jobTitle(df):
    """" selects new hires by jobTitle
    """
    jobTitle_list = ['Post-Doctoral Research Fellow',
                     'Staff Scientist',
                     'Research Techn II',
                     'Graduate Research Asst',
                     'Assistant Member',
                     'Research Techn III',
                     'Research Assc (PhD or MD)',
                     'Sr Staff Scientist',
                     'Research Techn IV',
                     'Data Coord III',
                     'Data Coord II',
                     'Stat Research Assc II',
                     'Stat Research Assc IV',
                     'Stat Research Assc III',
                     'Software Dev Engineer II',
                     'Data Coord IV',
                     'Software Dev Engineer III',
                     'Statistical Analyst, Sr',
                     'Principal Staff Scientist',
                     'Stat Research Assc V',
                     'Statistical Programmer III',
                     'Research Asst (Pre-Doc)',
                     'Statistical Programmer IV',
                     'Software Dev Engineer IV',
                     'Bioinformatics Analyst I',
                     'Data Scientist I',
                     'Bioinformatics Analyst III',
                     'Stat Research Assc I'
               ] # List of job titles taken from `dirks-issue.xlxs` and marked as "yes" or "possibly"
    try:
        return df[df.jobTitle.isin(jobTitle_list)]
    except:
        print("Error: selecting by jobTitle")

# Email Function
# Graciously shared by Mike B who shamelessly stole it from stackoverflow :)
# It uses the python built-in email package https://docs.python.org/3.4/library/email.html#module-email to create and send emails in an object model
# You can start a local SMTP debugging server by typing the following in shell "python -m smtpd -c DebuggingServer -n localhost:1025" and set server to `localhost` in the send_mail()

import smtplib
import os.path as op
from email.mime.multipart import MIMEMultipart
from email.mime.base import MIMEBase
from email.mime.text import MIMEText
from email.utils import COMMASPACE, formatdate
from email import encoders

# create the function that will create and send emails
def send_mail(send_from, send_to, subject, message, files=[],
              server='mx.fhcrc.org', port=25, username='', password='',
              use_tls=True):
    '''Compose and send email with provided info and attachments.
    Args:
        send_from (str): from email address/name
        send_to (str): common seperated list of email addresses
        subject (str): email subject line
        message (str): email body
        files (list[str]): list of file paths to be attached to email
        server (str): mail server host name
        port (int): port number
        username (str): server auth username
        password (str): server auth password
        use_tls (bool): use TLS mode
    '''
    # creates the container for the email message
    msg = MIMEMultipart()
    msg['From'] = send_from
    msg['To'] = COMMASPACE.join(send_to)
    msg['Date'] = formatdate(localtime=True)
    msg['Subject'] = subject
    
    # handles any attachements
    msg.attach(MIMEText(message))

    for path in files:
        part = MIMEBase('application', "octet-stream")
        with open(path, 'rb') as file:
            part.set_payload(file.read())
        encoders.encode_base64(part)
        part.add_header('Content-Disposition',
                        'attachment; filename="{}"'.format(op.basename(path)))
        msg.attach(part)
        
    # initiates a SMTP connect and uses tls to secure the connection
    smtp = smtplib.SMTP(server, port)
    smtp.connect(server, port)
    if use_tls:
        smtp.starttls()
        
    #smtp.login(username, password)
    # send email and quit SMTP
    smtp.sendmail(send_from, send_to, msg.as_string())
    smtp.quit()

# This function runs the whole process
def run_process(test=True):
    """ This function runs the whole process and logs accordingly.
    Args:
        test (bool): uses test parameters in functions. True by default.
    """
    import pandas as pd
    from datetime import datetime, timedelta
    
    import logging
    # Set up logging (start time, end time, toolbox output for each run, any errors (from toolbox fun or email returns))
    # NEED TO DO STILL

    import json, os
    # Load and assign config values from 'config.txt'
    
    path_to_test= os.path.dirname(os.path.realpath(__file__))
    base_path= os.path.dirname(path_to_test)
    full_path = base_path + '/new_hire/config.txt'

    config = json.load(open(full_path))
    
    # 1. Get the `last_runtime` value. This assumes that the CRON job is run every week
    last_runtime = datetime.today() - timedelta(days=7)
    last_runtime = last_runtime.strftime('%Y-%m-%d')
    
    filepath = config["filepath"]
    
    if test:
        last_runtime = '1999-01-01'
        filepath = config["test_filepath"]
        
    # 2. Get the file from toolbox and then select new hires
    try:
        new_hires_df = new_hires(get_employees(filepath), last_runtime) # retrieve employee.csv and filter down to new hires from the employee.csv table from toolbox
    except:
        print("Error: retrieving new hires")
        
    # 3. Select new hires by deptID
    try:
        hires_by_deptID_df = hires_by_deptID(new_hires_df)
    
    # 4. Select new hires by jobTitle
        hires_by_jobTitle_df = hires_by_jobTitle(new_hires_df)
    except:
        print("Error: retrieving hires by deptID & jobTitle")
    
    # 5. Extract the email addresses from the list of new hires and remove duplicates
    email_addresses = hires_by_deptID_df['mail'].tolist() + hires_by_jobTitle_df['mail'].tolist()
    email_addresses = list(set(email_addresses))
    
    # 6. Compose the email
    send_from = config["send_from"]
    send_to = email_addresses
    subject = config["subject"]
    message = config["message"]
    
    if test:
        send_to = config["test_send_to"]
        message = "THIS MESSAGE:-->" + message + "<--WOULD GO TO THESE ADDRESSES: " + ', '.join(email_addresses)
        
    # 7. Send emails. To test emails locally and send to localhost set these parameters; "port = 1025", "server = `localhost`", and "use_tls = False" after setting up a local SMTP debugging server
    # You can start a local SMTP debugging server by typing the following in shell "python -m smtpd -c DebuggingServer -n localhost:1025" and set server to `localhost` in the send_mail()
    if test:
        try:
            send_mail(send_from, send_to, subject, message, port=1025, server='localhost', use_tls=False) # for debugging/testing purposes
        except:
            print("Error: sending emails")
    else:
        try:
            send_mail(send_from, send_to, subject, message) # fires off email in production
        except:
            print("Error: sending emails")
        
    # 8. Logging and error reporting
    # NEED TO DO STILL
    
run_process(test=True)

# Check to see if new_hire.py is being runned as a script. If so run_process()
if __name__ == '__main__':
    run_process()