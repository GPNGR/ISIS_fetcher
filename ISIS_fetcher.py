# imports for ISIS
from selenium import webdriver
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.common.by import By
from selenium.webdriver.common.desired_capabilities import DesiredCapabilities
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.firefox.options import Options
from urllib.parse import unquote
import requests
import time

# imports for Git
from git import Repo
import datetime

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
        self.options = Options()
        # TODO: make driver --headless
        # self.options.headless = True
        self.options.set_preference('browser.download.folderList', 2)
        self.options.set_preference('browser.download.manager.showWhenStarting', False)
        self.options.set_preference('browser.download.dir', self.dldir)
        self.options.set_preference('browser.helperApps.neverAsk.saveToDisk',
        'application/msword, application/csv, application/ris, text/csv, image/png, application/pdf, text/html, text/plain, application/zip, application/x-zip, application/x-zip-compressed, application/download, application/octet-stream')
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
            div = 'div.tub-logo'  # DONE: check if right (seems to be working)
        self.wait.until(EC.visibility_of_element_located((By.CSS_SELECTOR, div)))

    def login(self):
        # DONE: login function

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
        r = self.request.head(url, allow_redirects=True)
        current_url = r.url

        file_name = (current_url.split('/'))[-1]
        if folder == 1:
            file_name = name[1:].replace(' ','_') + '.zip'

        file_path = path + unquote(file_name)

        if file_path.endswith('?forcedownload=1'): # remove forcedownload from zip filenames
            file_path = file_path[:-16]
            file_name = file_name[:-16]

        if not os.path.exists(file_path): # check if file exists, if not then download
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

        for courses, ID in self.ids.items():
            print(f'c Course: {courses}, id: {ID}')
            # go to resource page
            self.driver.get(self.courseLink + ID)

            # prepare download path
            if system == 'Windows':
                path = ISIS_dir + '\\' + courses + '\\'
            else:
                path = ISIS_dir + '/' + courses + '/'

            # find elements by class td,cell,c1 must include href find links to file (not actually the file link)
            elems = self.driver.find_elements_by_css_selector('td.cell.c1 [href]')
            url_dict = dict()
            for elem in elems:
                url = elem.get_attribute('href')
                name = elem.get_attribute('text')
                url_dict[url] = name

            for url, name in url_dict.items():
                if 'resource' in url:
                    self.downloader(path,url,name, 0) # download file only add name if folder

                if 'folder' in url:  # TODO: fix weird naming issue
                    print(f'Folder') #
                    
                    # print(f'{name}')

                    url_id = url.split('?')[-1]
                    f_url = 'https://isis.tu-berlin.de/mod/folder/download_folder.php?' + url_id

                    self.downloader(path, f_url, name,1)

class Git_handler:

    def __init__(self, rep_dir):
        self.rep_dir = rep_dir

    def git_pull(self):
        try:
            repo = Repo(self.rep_dir)
            origin = repo.remote('origin')
            origin.pull()
        except:
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
        except:
            time = str(datetime.date.today()) + ' ' + str(datetime.datetime.now().hour) + \
                ':' + str(datetime.datetime.now().minute)
            print(f'Failed to push to Uni Git repository on {time}\n')
        else:
            time = str(datetime.date.today()) + ' ' + str(datetime.datetime.now().hour) + \
                ':' + str(datetime.datetime.now().minute)
            print(f'Updated Uni Git repository on {time}\n')

if __name__ == '__main__':
    # Course_names and IDs
    ids = {'RnVs': '17196','SwtPP':'17456'
            ,'Logik':'17350','IG':'17280'}

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
    print(f'system -> {system}')
    for courses in ids:
        if system == 'Windows':
            directory = ISIS_dir + '\\' + courses
        else:
            directory = ISIS_dir + '/' + courses
        if not os.path.exists(directory):
            os.makedirs(directory)

    # get credentials from credentials.txt
    credentials = open(cred, 'r').readlines()
    is_login = credentials[0].strip('\n')
    is_pw = credentials[1].strip('\n')

    # pull git repo
    git = Git_handler(git_dir)
    git.git_pull()

    # Start fetching ISIS data
    ISIS(is_login, is_pw, ISIS_dir, ids)

    # push git repo
    git.git_push()