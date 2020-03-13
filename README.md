# new hire

New hire is a Python 3 script and set of functions that intergrates with the [Hutch's Toolbox](https://sciwiki.fredhutch.org/compdemos/toolbox/#what-is-toolboxfhcrcorg-) system to make it easier to identify new users.

## Installation

1. Download or copy the [New Hire repo](https://github.com/FredHutch/new_data_employee)
2. Locate the `new_hire.py` script and set it up to run as a weekly CRON job
3. Below discusses some of it's default parameters. _By default it is setup to retrieve the new users from Toolbox that have been added since the last time it ran. The "last time it ran" defaults to 7 days before it's current runtime. Therefore, if setup as a weekly CRON job it'll always be looking for new users over a 7-day timespan._
4. The script also ingests a config file that is in the same directory as the script.
