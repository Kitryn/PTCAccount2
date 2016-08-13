"""
PTCAccount2: Semi-automatic Pokemon Trainer Club account creator, with manual CAPTCHA prompts.
Heavily based on PTCAccount by jepayne1138 at https://github.com/jepayne1138/PTCAccount
Repo: https://github.com/Kitryn/PTCAccount2
"""

import time
import string
import random

from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By

from ptcaccount2.ptcexceptions import *

BASE_URL = "https://club.pokemon.com/us/pokemon-trainer-club"

# endpoints taken from PTCAccount
SUCCESS_URLS = (
    'https://club.pokemon.com/us/pokemon-trainer-club/parents/email',  # This initially seemed to be the proper success redirect
    'https://club.pokemon.com/us/pokemon-trainer-club/sign-up/',  # but experimentally it now seems to return to the sign-up, but still registers
)

# As both seem to work, we'll check against both success destinations until I have I better idea for how to check success
DUPE_EMAIL_URL = 'https://club.pokemon.com/us/pokemon-trainer-club/forgot-password?msg=users.email.exists'
BAD_DATA_URL = 'https://club.pokemon.com/us/pokemon-trainer-club/parents/sign-up'


def _random_string(length=15):
    return ''.join([random.choice(string.ascii_letters + string.digits) for _ in range(length)])


def _random_email(local_length=10, sub_domain_length=5, top_domain=".com"):
    return "{local}@{sub_domain}{top_domain}".format(
        local=_random_string(local_length),
        sub_domain=_random_string(sub_domain_length),
        top_domain=top_domain
    )


def _validate_password(password):
    # Check that password length is between 6 and 15 characters long
    if len(password) < 6 or len(password) > 15:
        raise PTCInvalidPasswordException('Password must be between 6 and 15 characters.')
    return True


def create_account(username, password, email):
    """
    As per PTCAccount by jepayne1138, this function raises:
      PTCInvalidNameException: If the given username is already in use.
      PTCInvalidPasswordException: If the given password is not a valid
        password that can be used to make an account. (Currently just
        validates length, so this means the given password was not between
        6 and 15 characters long.)
      PTCInvalidEmailException: If the given email was either in an invalid
        format (i.e. not local@subdomain.domain) or the email is already
        registered to an existing account.
      PTCInvalidStatusCodeException: If an invalid status code was received
        at any time. (Server or underlying code issue; try again and submit
        bug report on continues failure if creation works in browser.)
      AssertionError: If something a URL is not as expected

    This function returns true if account was created. Raises exceptions rather than returning false.
    """
    if password is not None:
        _validate_password(password)

    print("Attempting to create user {}. Opening browser...".format(username))
    driver = webdriver.Chrome()
    driver.set_window_size(600, 600)

    # Input age: 1992-01-08
    print("Step 1: Verifying age")
    driver.get("{}/sign-up/".format(BASE_URL))
    assert driver.current_url == "{}/sign-up/".format(BASE_URL)
    elem = driver.find_element_by_name("dob")
    driver.execute_script("arguments[0].removeAttribute('readonly')", elem)
    elem.clear()
    elem.send_keys("1992-01-08")
    elem.submit()

    # Create account page
    print("Step 2: Entering account details")
    assert driver.current_url == "{}/parents/sign-up".format(BASE_URL)

    user = driver.find_element_by_name("username")
    user.clear()
    user.send_keys(username)

    elem = driver.find_element_by_name("password")
    elem.clear()
    elem.send_keys(password)

    elem = driver.find_element_by_name("confirm_password")
    elem.clear()
    elem.send_keys(password)

    elem = driver.find_element_by_name("email")
    elem.clear()
    elem.send_keys(email)

    elem = driver.find_element_by_name("confirm_email")
    elem.clear()
    elem.send_keys(email)

    driver.find_element_by_id("id_public_profile_opt_in_1").click()
    driver.find_element_by_name("terms").click()

    # Now to handle captcha
    print("Waiting; Please enter the captcha in the browser window...")
    elem = driver.find_element_by_class_name("g-recaptcha")
    driver.execute_script("arguments[0].scrollIntoView(true);", elem)

    # Waits 1 minute for you to input captcha
    WebDriverWait(driver, 60).until(EC.text_to_be_present_in_element_value((By.ID, "g-recaptcha-response"), ""))
    print("Captcha successful. Sleeping for 1 second...")
    time.sleep(1)

    user.submit()

    try:
        _validate_response(driver)
    except:
        print("Failed to create user: {}".format(username))
        raise

    print("Account successfully created.")
    driver.close()
    return True


def _validate_response(driver):
    url = driver.current_url
    if url in SUCCESS_URLS:
        return True
    elif url == DUPE_EMAIL_URL:
        raise PTCInvalidEmailException("Email already in use.")
    elif url == BAD_DATA_URL:
        if "Enter a valid email address." in driver.page_source:
            raise PTCInvalidEmailException("Invalid email.")
        else:
            raise PTCInvalidNameException("Username already in use.")
    else:
        raise PTCException("Generic failure. User was not created.")


def random_account(username=None, password=None, email=None):
    try_username = _random_string() if username is None else str(username)
    password = _random_string() if password is None else str(password)
    try_email = _random_email() if email is None else str(email)

    account_created = False
    while not account_created:
        try:
            account_created = create_account(try_username, password, try_email)
        except PTCInvalidNameException:
            if username is None:
                try_username = _random_string()
            else:
                raise
        except PTCInvalidEmailException:
            if email is None:
                try_email = _random_email()
            else:
                raise

    return {
        "username": try_username,
        "password": password,
        "email": try_email
    }

