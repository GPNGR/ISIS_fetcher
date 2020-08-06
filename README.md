# ISIS_Fetcher

Iisi fetcher is a script that allowes you to download all your course material from www.isis.tu-berlin.de and automatically push it to your git repository.

## Dependencies

  - Python 3
    - Selenium (`# pip install selenium`)
      - Firefox driver in `path`
    - Git python (`# pip install gitpython`)

## Setup

1. Folder structure
```
Uni_folder
├─ ISIS_Fetcher/
|   ├─ ISIS_fetcher.py
|   ├─ credentials.json
|   └─ README.md
├─ Semester directory/
|   ├─ Course_1/
|   |   ├─ Slide_1
|   |   ├─ ...
|   |   └─ Slide_n
|   └─ Course_2/
|       ├─ Slide_1
|       ├─ ...
|       └─ Slide_n
```
2. create credentials.json
```Json
{
  "Isis login": "abcdefg",
  "Isis password": "123456",
  "Git directory": "06_20_SS",
  "Courses": {
    "AlgTheo": "19353",
    "VS": "18890",
    "Stochastik": "18995",
    "Data_Science": "18803"
  }
}
```
- the  course id can be found on the isis course page for example:
  - https://isis.tu-berlin.de/course/view.php?id=17350
    - would be the course "[WiSe2019/20] Logik"
    - with the id `17350`
3. run the script from within the Isis_fetcher folder