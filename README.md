# Todo List using GitHub Gist

## Features

### Before

Create a Todo List in a GitHub Gist (following the
[task list syntax](https://help.github.com/en/github/managing-your-work-on-github/about-task-lists#creating-task-lists))
and create a list and check the tasks you have done off during the day.

![before todo](images/before-todo.png)

### After

After midnight your done tasks will be transferred to the done list. In this
way you will have a history of your list!

|               Todo                   |          Done            |
|--------------------------------------|--------------------------|
| ![after todo](images/after-todo.png) | ![done](images/done.png) |

## Usage

- First create two gists from <https://gist.github.com>, namely `todo` and `done`.
- Add file `todo.md` and `done.md` to them respectively. The file content should
  be a single header `# Todo` and `# Done` respectively.

- Generate a new personal access token with gist scope from
  here: <https://github.com/settings/tokens/new>.

- Fork this repository.

- Add the gist IDs as `TODO_GIST`, `DONE_GIST` and the personal access token as
 `GH_TOKEN` to your repository secrets: `https://github.com/<your_username>/<repository_name>/settings/secrets`.
  It will look something like this:

  ![secrets.jpg](./images/secrets.png)

  > Gist ID is the part of the URL after your username. For example the gist ID
  of this gist `https://gist.github.com/ayan-b/1b44e52eifj09bc75c914f6fedf95304`
  is `1b44e52eifj09bc75c914f6fedf95304`.

- Now you have your todo list using GitHub gist!
- **Optional**: Change the time of [cron job](.github/workflows/update-list.yml)
  in the workflow file according to your time zone so that the todo and done
  list update exactly at midnight (and not at UTC midnight)!

  Here's one for IST time zone (UTC +5:30). Note the use of `TIME_ZONE` environment
  variable and the change in cron job.

```yaml
name: Update Todo List IST

on:
  push:
    branches: [ master ]
  pull_request:
    branches: [ master ]
  schedule:
    - cron: "30 5 * * *"  # 0 + time zone difference time

jobs:
  build:

    runs-on: ubuntu-latest

    steps:
    - uses: actions/checkout@v2
    - name: Set up Python 3.8
      uses: actions/setup-python@v1
      with:
        python-version: 3.8
    - name: Install dependencies
      run: |
        python -m pip install --upgrade pip
        pip install -r requirements.txt
    - name: Lint with flake8
      run: |
        pip install flake8
        # stop the build if there are Python syntax errors or undefined names
        flake8 . --count --select=E9,F63,F7,F82 --show-source --statistics
        # exit-zero treats all errors as warnings.
        flake8 . --count --exit-zero --max-complexity=10 --max-line-length=79 --statistics
    - name: Update todo list
      run: |
        python3 construct_todo.py
      env:
        GH_TOKEN: ${{ secrets.GH_TOKEN }}
        TODO_GIST: ${{ secrets.TODO_GIST }}
        DONE_GIST: ${{ secrets.DONE_GIST }}
        TIME_ZONE: "Asia/Kolkata" # IST
```

## License

[MIT](LICENSE)
