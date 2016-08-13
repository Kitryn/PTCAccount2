# Pokemon Trainer Club Account Creator 2
Script heavily based on the original [PTCAccount](https://github.com/jepayne1138/PTCAccount), by [jepayne1138](https://github.com/jepayne1138).

## Description
Semi-automatic creation of PTC accounts, with manual user intervention required for CAPTCHA input. This script is built on Selenium, which utilises a browser for automation rather than pure HTML requests.

## Installation

This script runs on Selenium using ChromeDriver. See the [Google documentation](https://sites.google.com/a/chromium.org/chromedriver/downloads) for platform specific installation.

OSX Installation: `brew install chromedriver`

Once ChromeDriver is installed, install PTCAccount2 from Github using pip:

`pip install git+https://github.com/Kitryn/PTCAccount2.git`

## Use

### Command line interface:

After installing the package run 'ptc2' from the terminal to create a new account. Optional parameters include --username, --password, and --email. Use --help for command line interface help.

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

Extra options:
* `--compact`: Compact the output to "username:password"