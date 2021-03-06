# imports for ISIS
from selenium import webdriver
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.common.by import By
from selenium.webdriver.common.desired_capabilities import DesiredCapabilities
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.firefox.options import Options
from selenium.common.exceptions import NoSuchElementException
from urllib.parse import unquote
import requests
import time

# imports for Git
from git import Repo
import datetime

# imports for main
import os
import platform
import json


class ISIS():

    def __init__(self, usr, pw, dldir, courseIDs, **kwargs):
        self.is_login = usr
        self.is_pw = pw
        self.dldir = dldir
        self.ids = courseIDs
        self.courseLink = 'https://isis.tu-berlin.de/course/resources.php?id='
        self.options = Options()
        self.options.headless = True
        self.options.set_preference('browser.download.folderList', 2)
        self.options.set_preference(
            'browser.download.manager.showWhenStarting', False)
        self.options.set_preference('browser.download.dir', self.dldir)
        self.options.set_preference('browser.helperApps.neverAsk.saveToDisk',
                                    'application/msword, application/csv, application/ris, text/csv, image/png, image/jpg, image/jpeg, application/pdf, text/html, text/plain, application/zip, application/x-zip, application/x-zip-compressed, application/download, application/octet-stream')
        self.driver = webdriver.Firefox(options=self.options)
        self.wait = WebDriverWait(self.driver, 10)
        self.request = requests.Session()
        self.main()

    def main(self):
        self.login()
        self.dataFetcher()
        print(f'Finished fetching')
        self.driver.quit()

    def waiter(self, div):
        if div == '':
            div = 'div.tub-logo'
        self.wait.until(EC.visibility_of_element_located(
            (By.CSS_SELECTOR, div)))

    def login(self):
        print(f'Login in to Isis')

        self.driver.get('https://www.isis.tu-berlin.de/login/index.php')
        self.waiter('div.container')

        self.driver.find_element_by_id('shibboleth_login').click()
        self.waiter('div.contentContainer')

        self.driver.find_element_by_id('username').send_keys(self.is_login)
        self.driver.find_element_by_id('password').send_keys(self.is_pw)
        self.driver.find_element_by_id('login-button').click()
        # get cookies and forward them to the requests session

        cookiejar = self.driver.get_cookies()

        for cookie in cookiejar:
            self.request.cookies.set(cookie['name'], cookie['value'])

        print(f'Done')

    def downloader(self, path, url, name, folder):
        # redirect url to download url
        r = self.request.head(url, allow_redirects=True)
        current_url = r.url

        # if url == current_url then its not a pdf
        if current_url == url and folder == 0:
            self.driver.get(url)
            try:
                elem = self.driver.find_element_by_css_selector(
                    '.resourceimage')
                current_url = elem.get_attribute('src')
            except NoSuchElementException:
                print(f'not an image')
            try:
                elem = self.driver.find_element_by_css_selector(
                    '.resourceworkaround > a:nth-child(1)')
                url = elem.get_attribute('href')
                r = self.request.head(url, allow_redirects=True)
                current_url = r.url
            except NoSuchElementException:
                print(f'no workaround pdf either -> skipping file')
                pass

        # if folder == 1 create zip file name
        file_name = (current_url.split('/'))[-1]
        if folder == 1:
            file_name = name[1:].replace(' ', '_') + '.zip'

        # unqoute url to change %C3% to umlaut
        file_path = path + unquote(file_name)

        # remove forcedownload from zip filenames
        if file_path.endswith('?forcedownload=1'):
            file_path = file_path[:-16]
            file_name = file_name[:-16]

        # check if file exists, if not then download
        if not os.path.exists(file_path):
            print(f'Beginning file download {file_name}')

            t_start = time.time()
            data = self.request.get(current_url)
            with open(file_path, 'wb') as f:
                f.write(data.content)
            t_total = time.time() - t_start

            print(f'finished in {t_total} seconds\n')
        else:
            print(f'{file_name} already exists')

    def dataFetcher(self):
        for c, id_ in self.ids.items():
            print(f'Course: {c}, id: {id_}')
            # go to resource page
            self.driver.get(self.courseLink + id_)

            # prepare download path
            if system == 'Windows':
            	path = ISIS_dir + '\\' + c + '\\'
            else:
            	path = ISIS_dir + '/' + c + '/'

            # find elements by class td,cell,c1 must include href find links to
            # file (not actually the file link)
            elems = self.driver.find_elements_by_css_selector(
                'td.cell.c1 [href]')
            url_dict = dict()
            for elem in elems:
                url = elem.get_attribute('href')
                name = elem.get_attribute('text')
                url_dict[url] = name

            for url, name in url_dict.items():
                # download regular files
                if 'resource' in url:
                    self.downloader(path, url, name, 0)
                # download folder as .zip
                if 'folder' in url:
                    print(f'Folder')
                    url_id = url.split('?')[-1]
                    f_url = 'https://isis.tu-berlin.de/mod/folder/download_folder.php?' + url_id
                    self.downloader(path, f_url, name, 1)


class Git_handler:

    def __init__(self, rep_dir):
        self.rep_dir = rep_dir

    def git_pull(self):
        try:
            repo = Repo(self.rep_dir)
            origin = repo.remote('origin')
            origin.pull()
        except BaseException:
            time = str(datetime.date.today()) + ' ' + str(datetime.datetime.now().hour) + \
                ':' + str(datetime.datetime.now().minute)
            print(f'Failed to pull from Uni git repo on {time}')
        else:
            time = str(datetime.date.today()) + ' ' + str(datetime.datetime.now().hour) + \
                ':' + str(datetime.datetime.now().minute)
            print(f'Succsesfully pulled from Uni git repo on {time}')

    def git_push(self):
        time = str(datetime.date.today()) + ' ' + str(datetime.datetime.now().hour) + \
            ':' + str(datetime.datetime.now().minute)
        commit_message = f'Updated via Python at {time}'
        try:
            repo = Repo(self.rep_dir)
            repo.git.add('--all')
            repo.index.commit(commit_message)
            origin = repo.remote('origin')
            origin.push()
        except BaseException:
            time = str(datetime.date.today()) + ' ' + str(datetime.datetime.now().hour) + \
                ':' + str(datetime.datetime.now().minute)
            print(f'Failed to push to Uni Git repository on {time}\n')
        else:
            time = str(datetime.date.today()) + ' ' + str(datetime.datetime.now().hour) + \
                ':' + str(datetime.datetime.now().minute)
            print(f'Updated Uni Git repository on {time}\n')


if __name__ == '__main__':
    # get system info and paths to git repository
    system = platform.system()

    cwd = os.getcwd()
    # grab credentials and courses
    with open(os.path.join(cwd, 'credentials.json')) as input:
        cred = json.load(input)
    i_dir = cred['Git directory']
    ISIS_dir = os.path.join(os.pardir, i_dir)
    git_dir = os.path.join(ISIS_dir, '.git')

    # Course_names and IDs
    courses = cred['Courses']

    # create folder structer if non existent
    print(f'system -> {system}')
    for c in courses:
        dir_ = os.path.join(ISIS_dir, c)
        if not os.path.exists(dir_):
            os.makedirs(dir_)

    is_login = cred['Isis login']
    is_pw = cred['Isis password']

    # pull git repo
    git = Git_handler(git_dir)
    git.git_pull()

    # Start fetching ISIS data
    ISIS(is_login, is_pw, ISIS_dir, courses)

    # push git repo
    git.git_push()
