# ISIS_Downloader
Auto download slides and homework from ISIS

# HowTo
## setup
- download git repo  
- recomended folder structure
```
Uni_folder
├─ ISIS_Fetcher/
|   ├─ ISIS_fetcher.py
|   ├─ credentials.txt
|   └─ README.md
├─ Semester Folder/
|   ├─ Course_1/
|   |   ├─ Slide_1
|   |   └─ Slide_n
|   └─ Course_2
|       ├─ Slide_1
|       └─ Slide_n
```
- create credentials.txt 
```
# Isis login and pw
m.Mustermann
is_password
# Github login and pw
Mustermain
git_password
```
- change lines
  - 150 -160 replace test with your semester folder name
```Python
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
```
  - 146 -147 for your courses and the course ids
    - the id can be found on isis for example
    - https://isis.tu-berlin.de/course/view.php?id=17350
```Python
    ids = {'RnVs': '17196','SwtPP':'17456'
            ,'Logik':'17350','IG':'17280'}
```
