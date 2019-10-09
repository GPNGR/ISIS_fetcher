# imports for ISIS
from selenium import webdriver
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.common.by import By
from selenium.webdriver.common.desired_capabilities import DesiredCapabilities
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.firefox.options import Options
# import numpy as np
# import re

# imports for Git

# imports for mail

# imports for main
import os
import platform


class ISIS():

    def __init__(self, usr, pw, dldir, courseIDs, **kwargs):
        self.is_login = usr
        self.is_pw = pw
        self.dldir = dldir
        self.ids = courseIDs
        self.courseLink = 'https://isis.tu-berlin.de/course/resources.php?id='
        # TODO: make driver --headless
        self.options = Options()
        self.options.set_preference("browser.download.folderList", 2)
        self.options.set_preference("browser.download.manager.showWhenStarting", False)
        self.options.set_preference("browser.download.dir", "/data")
        self.options.set_preference("browser.helperApps.neverAsk.saveToDisk", "application/octet-stream,application/vnd.ms-excel")
        self.driver = webdriver.Firefox(firefox_options=self.options)
        self.wait = WebDriverWait(self.driver, 10)
        self.main()

    def main(self):
        self.login()
        # self.dataFetcher()
        # self.downloadMNGR()

    def waiter(self, div):
        if div == '':
            div = 'div.tub-logo'  # TODO: check if right
        self.wait.until(EC.visibility_of_element_located((By.CSS_SELECTOR, div)))

    def login(self):
        # DONE: login function

        self.driver.get('https://www.isis.tu-berlin.de/login/index.php')
        self.waiter('div.container')

        self.driver.find_element_by_id('shibboleth_login').click()
        self.waiter('div.contentContainer')

        self.driver.find_element_by_id('username').send_keys(self.is_login)
        self.driver.find_element_by_id('password').send_keys(self.is_pw)
        self.driver.find_element_by_id('login-button').click()

    def dataFetcher(self):
        # TODO: dataFetcher
        for courseID, ID in self.ids.items():
            print(f'c id: {courseID}, id: {ID}')
            self.driver.get(self.courseLink + ID)


if __name__ == '__main__':
    # Course_names and IDs
    ids = {'ISDA': '15697', 'Diskrete-Strukturen': '15604',
           'Stochastik': '15633', 'Sysprog': '15693'}

    # get system info and paths to git repository
    system = platform.system()

    if system == 'Windows':
        cwd = os.getcwd()
        cred = cwd + r'\credentials.txt'
        git_dir = os.getcwd().strip('ISIS_fetcher') + r'Test\.git'
        ISIS_dir = os.getcwd().strip('ISIS_fetcher') + r'Test'
    else:
        cwd = os.getcwd()
        cred = cwd + '/credentials.txt'
        git_dir = os.getcwd().strip('ISIS_fetcher') + 'Test/.git'
        ISIS_dir = os.getcwd().strip('ISIS_fetcher') + 'Test'

        # create folder structer if non existent
    for courses in ids:
        if system == 'Windows':
            directory = ISIS_dir + r'\Course-' + courses
        else:
            directory = ISIS_dir + '/Course-' + courses
        if not os.path.exists(directory):
            os.makedirs(directory)

    # get credentials from credentials.txt
    credentials = open(cred, 'r').readlines()
    is_login = credentials[1].strip('\n')
    is_pw = credentials[2].strip('\n')
    git_login = credentials[4].strip('\n')
    git_pw = credentials[5].strip('\n')
    mail_login = credentials[7].strip('\n')
    mail_pw = credentials[8].strip('\n')
    provider = credentials[9].strip('\n')
    smtp = credentials[10].strip('\n')
    port = int(credentials[11].strip('\n'))

    # Start fetching ISIS data
    ISIS(is_login, is_pw, ISIS_dir, ids)
