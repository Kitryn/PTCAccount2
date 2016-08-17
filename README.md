# Pokemon Trainer Club Account Creator 2
Script heavily based on the original [PTCAccount](https://github.com/jepayne1138/PTCAccount), by [jepayne1138](https://github.com/jepayne1138).

## Description
Semi-automatic creation of PTC accounts, with manual user intervention required for CAPTCHA input. This script is built on Selenium, which utilises a browser for automation rather than pure HTTP requests.

## Installation

This script runs on Selenium using ChromeDriver. See the [Google documentation](https://sites.google.com/a/chromium.org/chromedriver/downloads) for platform specific installation.

OSX Installation: `brew install chromedriver`

Once ChromeDriver is installed, install PTCAccount2 from Github using pip:

`pip install git+https://github.com/Kitryn/PTCAccount2.git`

NOTE: Google Chrome (the browser) must be installed for this script to work!

## Use

### Command line interface:

After installing the package run 'ptc2' from the terminal to create a new account. Optional parameters include --username, --password, and --email. Use --help for more commands and command line interface help.

Example 1 (Create entirely random new account):

```
> ptc2
Account successfully created.
  Username:  BcZvTnlTMwHsa6v
  Password:  WgZApVU5edTBMCs
  Email   :  ZApVgwHsa6sv@5aDsy.com
```

Example 2 (Create a new account with specified parameters):

```
> ptc2 --username=foo --password=bar --email=shin@ramyun.com
Account successfully created.
  Username:  foo
  Password:  bar
  Email   :  shin@ramyun.com
```

Example 3 (Create multiple accounts with a Gmail account for verification):
```
> ptc2 --email=len@gmail.com --multiple=2 --tofile
Creating new account(s):
...
...
...
Appended to file accounts.txt
Summary of accounts created:
3Dt9louj4X1cgA8:8NiCxnMKw6SC0UF
jTd5IrV5kDkzG9l:zyoqLOCoATdLImO
```

Extra options:

* `--multiple=MULTIPLE`: Specify number of accounts to make. `--username` cannot be set while `--multiple` is greater than 1.
* `--birthday=BIRTHDAY`: Specify a birthday. Must be between 1910 and 2002. Must be in YYYY-MM-DD format.
* `--compact`: Compact the output to "username:password"
* `--tofile` : Append newly created username and password into file "accounts.txt" with format "username:password".
* `--email-tag`: If set, adds the username as a tag to the email (i.e addr+tag@mail.com). Automatically set if --multiple is >1, AND an email is provided.

Note: email tags may not work with all service providers. Only tested with Gmail.

**As package:**

import the _ptcaccount2_ package to create new accounts in your own scripts:

```python
>>> import ptcaccount2
>>> ptcaccount2.random_account()
{"username": "BcZvTnlTMwHsa6v", "password": "WgZApVU5edTBMCs", "email": "ZApVgwHsa6sv@5aDsy.com"}
```

**Specifying your own data:**
```python
>>> ptcaccount2.random_account(username=<your data>, password=<your data>, email=<your data>, birthday=<your data>, email_tag=<True/False>)
```

Note: `birthday` must be a string in YYYY-MM-DD format.

## Troubleshooting

### OSX installation

Some OSX users may run into an issue which points to an error occurring in line: `create_account driver = webdriver.Chrome()` This may be related to `brew install chromedriver` installing a 32bit version rather than 64bit version.

To fix, see [this issue](https://github.com/Kitryn/PTCAccount2/issues/1) to make brew install the 64bit version of ChromeDriver.
