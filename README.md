# new_hire

new_hire is a Python 3 script and set of functions that intergrates with the [Hutch's Toolbox](https://sciwiki.fredhutch.org/compdemos/toolbox/#what-is-toolboxfhcrcorg-) system to make it easier to identify new users for additional support.

## Installation

1. Download or copy the [new_hire]- (https://github.com/FredHutch/new_data_employee) repo
2. Locate the `new_hire.py` script and set it up to run as a weekly CRON job
3. Below discusses some of it's default parameters. _By default it is setup to retrieve the new users from Toolbox that have been added since the last time it ran. The "last time it ran" defaults to 7 days before it's current runtime. Therefore, if setup as a weekly CRON job it'll always be looking for new users over a 7-day timespan._
4. The script also ingests a config.txt file that is in the same directory as the script and contains a dictionary of key/values you can use to set key variables in the script such as.

```{"filepath": FILEPATH TO TOOLBOX FILE, 
"test_filepath": FILEPATH TO TEST FILE,
"send_from": SEND FROM EMAIL ADDRESS,
"subject": “EMAIL SUBJECT LINE,
"message": EMAIL MESSAGE,
"test_send_to": SEND TO TEST ADDRESS}
```

5. The script must also be executed behind the firewall

## Overview

This script interacts with Toolbox and more information on what Toolbox is [can be found here.](https://sciwiki.fredhutch.org/compdemos/toolbox/)

The new_hire.py script utilizes the following functions to query, filter and extract data from Toolbox. It then compiles an email and sends an email based on the retrieved data to certain users.

- get_employees() - takes a Toolbox csv filepath, retrieves and prunes it, and exports it as a dataframe

- new_hires() - take a dataframe and filters it based on date i.e. supplied `last_runtime`

- hires_by_deptID() and hires_by_jobTitle() - queries a dataframe and returns rows

- send_mail() - compiles and sends the emails with the desired data

- run_process() - runs the whole process and has a test parameter currently defaulted to `True` which sets up an environment to test/debug. You can start a local SMTP debugging server by typing the following in shell `python -m smtpd -c DebuggingServer -n localhost:1025` and set server to `localhost` in the send_mail()
