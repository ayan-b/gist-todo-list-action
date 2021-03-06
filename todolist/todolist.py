from datetime import datetime
import json
import os

import pytz
import requests


class Gist:
    def __init__(self, id, token):
        self.id = id
        self.token = token

    def _form_request(self, request_type, api_end, content=''):
        api_base = 'https://api.github.com'
        api_url = api_base + api_end
        header = {
            'Authorization': 'token ' + self.token,
            'Content-Type': 'application/json',
        }
        if request_type == 'GET':
            r = requests.get(api_url, headers=header)
            return r.json()
        elif request_type == 'PATCH':
            r = requests.patch(
                api_url,
                headers=header,
                data=json.dumps(content)
            )
            return r.json()

    def update_gist(self, file_name, content, todo):
        description = ''
        if todo is True:
            description = 'My todo list!'
        else:
            description = 'My done list!'
        request_content = {
            'description': description,
            'files': {
                file_name: {
                    'content': content,
                    'filename': file_name,
                }
            }
        }
        self._form_request(
            request_type='PATCH',
            api_end=f'/gists/{self.id}',
            content=request_content,
        )

    def get_content(self, file_name):
        data = self._form_request(
            request_type='GET',
            api_end=f'/gists/{self.id}',
        )
        try:
            return data['files'][file_name]['content']
        except Exception:
            raise Exception(
                'Could not find the specified file. Returned data:', data
            )


def parser(todo_list):
    done = []
    not_done = []
    todo_lines = todo_list.split('\n')
    for todo in todo_lines:
        if todo.strip().lower().startswith('- [x]'):
            done.append(todo.strip())
        else:
            not_done.append(todo)
    return done, not_done


def update_todo(not_done):
    return '\n'.join(not_done)


def get_time_wrt_time_zone():
    utc_date = datetime.today()
    custom_timezone = pytz.timezone('UTC')
    try:
        custom_timezone = pytz.timezone(os.environ['TIME_ZONE'])
    except Exception:
        pass
    today = utc_date.astimezone(custom_timezone).strftime("%B %d, %Y")
    return today


def add_to_done(done, previous_done):
    formatted_date = get_time_wrt_time_zone()
    previous_done = previous_done.split('\n')
    if not done:
        return '\n'.join(previous_done)
    # remove first line
    if len(previous_done) > 0:
        previous_done.remove(previous_done[0])
    date_string = ''
    is_found = False
    for i in range(len(previous_done)):
        if previous_done[i].strip():
            if previous_done[i].find(formatted_date) != -1:
                is_found = True
                previous_done.remove(previous_done[i])
            break
    date_string = '## Completed on ' + formatted_date + '\n\n'
    done = date_string + '\n'.join(done)
    if is_found is False:
        done += '\n'
    final_done = '# Done \n\n' + done + '\n'.join(previous_done)
    return final_done


def make_todolist(path_to_todo, path_to_done):
    todo_gist_id = os.environ['TODO_GIST']
    done_gist_id = os.environ['DONE_GIST']
    token = os.environ['GH_TOKEN']
    todo_list_gist = Gist(todo_gist_id, token)
    todo_list = todo_list_gist.get_content(path_to_todo)
    done_list_gist = Gist(done_gist_id, token)
    done_list = done_list_gist.get_content(path_to_done)
    done, not_done = parser(todo_list)
    modified_done = add_to_done(done, done_list)
    modified_todo = update_todo(not_done)
    todo_list_gist.update_gist(path_to_todo, modified_todo, True)
    done_list_gist.update_gist(path_to_done, modified_done, False)
