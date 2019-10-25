# ISIS_Downloader
Auto download slides and homework from ISIS

# setup
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
|   └─ Course_2/
|       ├─ Slide_1
|       └─ Slide_n
```
- create credentials.txt 
```
m.Mustermann
is_password
```
- change lines
  -  for your courses and the course ids
    - the id can be found on the isis course page link for example:
    - https://isis.tu-berlin.de/course/view.php?id=17350
```Python
181    ids = {'RnVs': '17196','SwtPP':'17456'
182            ,'Logik':'17350','IG':'17280'}
```
  - replace Test with your semester folder name
```Python
187    if system == 'Windows':
188        cwd = os.getcwd()
189        cred = cwd + r'\credentials.txt'
190        git_dir = os.getcwd().strip('ISIS_fetcher') + r'Test\.git'
191        ISIS_dir = os.getcwd().strip('ISIS_fetcher') + r'Test'
192    else:
193       cwd = os.getcwd()
194        cred = cwd + '/credentials.txt'
195        git_dir = os.getcwd().strip('ISIS_fetcher') + 'Test/.git'
196        ISIS_dir = os.getcwd().strip('ISIS_fetcher') + 'Test'
```