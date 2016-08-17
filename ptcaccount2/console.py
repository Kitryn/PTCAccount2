import argparse
import sys

import ptcaccount2
from ptcaccount2.ptcexceptions import *


def parse_arguments(args):
    """Parse the command line arguments for the console commands.
    Args:
      args (List[str]): List of string arguments to be parsed.
    Returns:
      Namespace: Namespace with the parsed arguments.
    """
    parser = argparse.ArgumentParser(
        description='Pokemon Trainer Club Account Creator'
    )
    parser.add_argument(
        '-u', '--username', type=str, default=None,
        help='Username for the new account (defaults to random string).'
    )
    parser.add_argument(
        '-p', '--password', type=str, default=None,
        help='Password for the new account (defaults to random string).'
    )
    parser.add_argument(
        '-e', '--email', type=str, default=None,
        help='Email for the new account (defaults to random email-like string).'
    )
    parser.add_argument(
        '-b', '--birthday', type=str, default=None,
        help='Birthday for the account. Must be YYYY-MM-DD. (default is a random birthday).'
    )
    parser.add_argument(
        '-m', '--multiple', type=int, default=1,
        help='Create multiple accounts at once (defaults to 1)'
    )
    parser.add_argument(
        '--compact', action='store_true',
        help='Compact the output to "username:password"'
    )
    parser.add_argument(
        '--tofile', action='store_true',
        help='Output "username:password" into file "accounts.txt"'
    )

    return parser.parse_args(args)


def entry():
    """Main entry point for the package console commands"""
    args = parse_arguments(sys.argv[1:])
    try:
        print('Creating new account(s):')
        for _ in range(args.multiple):
            # Create the random account
            account_info = ptcaccount2.random_account(
                args.username, args.password, args.email, args.birthday)
            if args.compact:
                print('{}:{}'.format(account_info["username"], account_info["password"]))
            else:
                print('  Username:  {}'.format(account_info["username"]))
                print('  Password:  {}'.format(account_info["password"]))
                print('  Email   :  {}'.format(account_info["email"]))
                print('\n')
            if args.tofile:
                with open("accounts.txt", 'a+') as writeto:
                    writeto.write('{}:{}'.format(account_info["username"], account_info["password"]) + "\n")
                print "Appended to file accounts.txt"

    # Handle account creation failure exceptions
    except PTCInvalidPasswordException as err:
        print('Invalid password: {}'.format(err))
    except (PTCInvalidEmailException, PTCInvalidNameException) as err:
        print('Failed to create account! {}'.format(err))
    except PTCException as err:
        print('Failed to create account! General error:  {}'.format(err))
