### All new employees likely to engage in data-intensive research will receive an email shortly after starting
### that includes information about computational resources on campus. This code enables this.

### Get the file from Toolbox
def get_employees():
    '''retrieves employee.csv from Toolbox'''
    try:
        df = pd.read_csv('https://toolbox.fhcrc.org/csv/employees.csv', usecols=['employeeID','mail','hireDate','jobTitle','deptID'], parse_dates=['hireDate'], infer_datetime_format=True)
        return df
    except:
        print("Error: retrieving employees.csv")

### Select new hires
def new_hires(df, last_runtime):
    '''selects new hires from employee.csv'''
    try:
        new_hires = df[df.hireDate >= last_runtime]
        return new_hires
    except:
        print("Error: selecting new hires")

### Select new hires by deptID
def hires_by_deptID(df):
    '''selects new hires by deptID'''
    deptID_list = ['PH06'] #`PHO6`= Computational Biology 
    try:
        df = df[df.deptID.isin(deptID_list)] 
        return df
    except:
        print("Error: selecting by deptID")

### Select new hires by jobTitle
def hires_by_jobTitle(df):
    '''selects new hires by jobTitle'''
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
        df = df[df.jobTitle.isin(jobTitle_list)]
        return df
    except:
        print("Error: selecting by jobTitle")

### Set up function to email
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
    """Compose and send email with provided info and attachments.

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
    """
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
