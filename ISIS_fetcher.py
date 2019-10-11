# imports for ISIS
from selenium import webdriver
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.common.by import By
from selenium.webdriver.common.desired_capabilities import DesiredCapabilities
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.firefox.options import Options

# import magic

import urllib.request
import urllib.parse
import urllib.error


# imports for Git

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
        self.dataFetcher()
        # self.downloadMNGR()
        # self.driver.quit()

    def waiter(self, div):
        if div == '':
            div = 'div.tub-logo'  # DONE: check if right (seems to be working)
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

        for courses, ID in self.ids.items():
            print(f'c id: {courses}, id: {ID}')
            # go to resource page
            self.driver.get(self.courseLink + ID)

            # prepare download path
            if system == 'Windows':
                path = ISIS_dir + '\\' + courses + '\\'
            else:
                path = ISIS_dir + '/' + courses + '/'

            # find elements by class td,cell,c1 must include href find links to file (not actually the file link)
            elems = self.driver.find_elements_by_css_selector('td.cell.c1 [href]')

            for elem in elems:
                # ignore if url contains page
                url = elem.get_attribute('href')

                name = elem.get_attribute('text')  # probably not usefull

                # follow the link to get next link wich is actually the fucking file ????

                print(f'{url}, {name}')


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
            directory = ISIS_dir + '\\' + courses
        else:
            directory = ISIS_dir + '/' + courses
        if not os.path.exists(directory):
            os.makedirs(directory)

    # get credentials from credentials.txt
    credentials = open(cred, 'r').readlines()
    is_login = credentials[1].strip('\n')
    is_pw = credentials[2].strip('\n')
    git_login = credentials[4].strip('\n')
    git_pw = credentials[5].strip('\n')

    # Start fetching ISIS data
    ISIS(is_login, is_pw, ISIS_dir, ids)
