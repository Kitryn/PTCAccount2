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
        help='Specify a number of accounts to create (default 1). If >1 AND `--email` is specified, the `--email-tag` option will be automatically set.'
    )
    parser.add_argument(
        '--compact', action='store_true',
        help='Compact the output to "username:password"'
    )
    parser.add_argument(
        '--email-tag', action='store_true',
        help='Add the username as a tag to the email (i.e addr+tag@mail.com).'
    )  # Note: Email max length is 75 characters.

    group = parser.add_mutually_exclusive_group()
    group.add_argument(
        '--tofile', action='store_true',
        help='Output "username:password" into file "accounts.txt". [Deprecated: Use "--output accounts.txt" instead.]'
    )
    group.add_argument(
        '-o', '--output', metavar='FILE',
        help='Output "username:password" to a file.'
    )

    return parser.parse_args(args)


def entry():
    """Main entry point for the package console commands"""
    args = parse_arguments(sys.argv[1:])
    account_summary = []
    try:
        if args.multiple > 1 and args.username is not None:
            raise ValueError("Username cannot be set if --multiple is greater than 1!")
        if args.email is not None and len(args.email) > 75:
            raise ValueError("Email cannot be longer than 75 characters!")

        if args.multiple > 1 and args.email is not None:
            # If email is set when more than one account is set to be created, email-tag must be True
            args.email_tag = True

        print('Creating new account(s):')

        for _ in range(args.multiple):
            # Create the random account
            account_info = ptcaccount2.random_account(
                args.username, args.password, args.email, args.birthday, args.email_tag)
            if args.compact:
                print('{}:{}'.format(account_info["username"], account_info["password"]))
            else:
                print('  Username:  {}'.format(account_info["username"]))
                print('  Password:  {}'.format(account_info["password"]))
                print('  Email   :  {}'.format(account_info["email"]))
                print('\n')

            if args.tofile:
                output = 'accounts.txt'
            elif args.output:
                output = args.output
            else:
                output = None

            if output is not None:
                with open(output, 'a+') as writeto:
                    writeto.write('{}:{}'.format(account_info["username"], account_info["password"]) + "\n")
                print('Appended to file {}'.format(output))
            account_summary.append({"username": account_info["username"], "password": account_info["password"]})

    # Handle account creation failure exceptions
    except PTCInvalidPasswordException as err:
        print('Invalid password: {}'.format(err))
    except (PTCInvalidEmailException, PTCInvalidNameException) as err:
        print('Failed to create account! {}'.format(err))
    except PTCException as err:
        print('Failed to create account! General error:  {}'.format(err))
    finally:
        if args.multiple > 1:
            print("Summary of accounts created:")
            for account in account_summary:
                print("{}:{}".format(account["username"], account["password"]))
