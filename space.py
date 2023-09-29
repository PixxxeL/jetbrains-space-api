import json
import logging

import requests


logger = logging.getLogger(__name__)


class SpaceApi:

    _base_url = ''
    _api_url = ''
    _token = ''
    _list_limit = 1000

    def __init__(self, base_url, token):
        """\
        @param base_url like `https://<yourorganization>.jetbrains.space`
        @param token
        """
        self._base_url = base_url
        self._api_url = f'{base_url}/api/http'
        self._token = token

    def get_projects(self, offset=0, limit=self._list_limit):
        """\
        https://www.jetbrains.com/help/space/projects-a.html#get_all_projects
        """
        url = f'{self._api_url}/projects'
        params = self._get_params(get_data={
            '$skip': offset,
            '$top': limit,
        })
        response = requests.get(url, **params)
        return response.json().get('data')

    def get_users(self, offset=0, limit=self._list_limit):
        """\
        https://www.jetbrains.com/help/space/team-directory.html#get_all_profiles
        """
        url = f'{self._api_url}/team-directory/profiles'
        params = self._get_params(get_data={
            '$skip': offset,
            '$top': limit,
        })
        response = requests.get(url, **params)
        return response.json().get('data')

    def get_user(self, id):
        """\
        https://www.jetbrains.com/help/space/team-directory.html#get_profile
        """
        url = f'{self._api_url}/team-directory/profiles/{id}'
        params = self._get_params()
        response = requests.get(url, **params)
        return response.json()

    def delete_user(self, id):
        """\
        https://www.jetbrains.com/help/space/team-directory.html#get_profile
        """
        url = f'{self._api_url}/team-directory/profiles/{id}'
        params = self._get_params()
        response = requests.delete(url, **params)
        return response.json()

    def create_project(self, key, name, description=None):
        """\
        https://www.jetbrains.com/help/space/projects-a.html#create_project
        """
        url = f'{self._api_url}/projects'
        params = self._get_params(post_data={
            'key': {
                'key': key
            },
            'name': name,
            'description': description,
        })
        response = requests.post(url, **params)
        return response.json()

    def delete_project(self, project_id):
        """\
        https://www.jetbrains.com/help/space/projects-a.html#delete_project
        """
        url = f'{self._api_url}/projects/{project_id}'
        params = self._get_params(post_data={})
        response = requests.delete(url, **params)
        return response.json()

    def add_project_admin(self, project_id, username):
        """\
        https://www.jetbrains.com/help/space/projects-a.html#add_administrator
        """
        url = f'{self._api_url}/projects/{project_id}/access/admins/profiles'
        params = self._get_params(post_data={
            'profile': {
                'className': 'ProfileIdentifier.Username',
                'username': username,
            }
        })
        response = requests.post(url, **params)
        logger.info(f'Space.add_project_admin: {response.content}')

    def add_team(self, project_id, team_id):
        """\
        https://www.jetbrains.com/help/space/projects-a.html#add_team
        """
        url = f'{self._api_url}/projects/{project_id}/access/members/teams'
        params = self._get_params(post_data={
            'teamId': team_id,
        })
        response = requests.post(url, **params)
        logger.info(f'Space.add_team: {response.content}')

    def get_teams(self, offset=0, limit=self._list_limit):
        """\
        https://www.jetbrains.com/help/space/team-directory.html#get_all_teams
        """
        url = f'{self._api_url}/team-directory/teams'
        params = self._get_params(get_data={
            '$skip': offset,
            '$top': limit,
        })
        response = requests.get(url, **params)
        return response.json().get('data')

    def add_merge_request(self, project, repo, src, dst, title):
        """\
        https://www.jetbrains.com/help/space/projects-a.html#create_merge_request
        """
        url = f'{self._api_url}/projects/{project}/code-reviews/merge-requests'
        params = self._get_params(post_data={
            'repository': repo,
            'sourceBranch': src,
            'targetBranch': dst,
            'title': title,
            #'reviewers': [{'profileId': ''}],
        })
        response = requests.post(url, **params)
        return response.json()

    def add_participant(self, project, review, user, role='Reviewer'):
        """\
        https://www.jetbrains.com/help/space/projects-a.html#add_review_participant
        """
        if role not in ['Author', 'Reviewer']:
            role = 'Watcher'
        url = f'{self._api_url}/projects/{project}/code-reviews/{review}/participants/{user}'
        params = self._get_params(post_data={
            'role': role
        })
        response = requests.post(url, **params)
        #logger.info(f'Space.add_participant: {response.content}')

    def get_members(self, offset=0, limit=self._list_limit):
        """\
        https://www.jetbrains.com/help/space/team-directory.html#get_all_memberships
        """
        url = f'{self._api_url}/team-directory/memberships'
        params = self._get_params(get_data={
            '$skip': offset,
            '$top': limit,
        })
        response = requests.get(url, **params)
        return response.json().get('data')

    def get_roles(self):
        """\
        https://www.jetbrains.com/help/space/team-directory.html#get_all_roles
        """
        url = f'{self._api_url}/team-directory/roles'
        params = self._get_params()
        response = requests.get(url, **params)
        return response.json()

    def create_invitation(self, email, firstName, lastName, team=None, role=None):
        """\
        https://www.jetbrains.com/help/space/team-directory.html#create_invitation
        """
        url = f'{self._api_url}/team-directory/invitations'
        params = self._get_params(post_data={
            'inviteeEmail': email,
            'inviteeFirstName': firstName,
            'inviteeLastName': lastName,
            'team': team,
            'role': role,
            #project
            #projectRole
            #globalRole
        })
        response = requests.post(url, **params)
        return response.json()

    def create_profile(self, username, firstName, lastName, emails=[], guest=None):
        """\
        https://www.jetbrains.com/help/space/team-directory.html#create_profile
        @param username - (required)
        @param firstName - (required)
        @param lastName - (required)
        @param emails - optional list
        @param guest - ставим в True, если хотим external profile

        Высылается ссылка активации
        """
        url = f'{self._api_url}/team-directory/profiles'
        params = self._get_params(post_data={
            'username': username,
            'firstName': firstName,
            'lastName': lastName,
            'emails': emails,
            'guest': guest,
            #'notAMember': False, # ставим в True, если хотим неактивированного участника
        })
        response = requests.post(url, **params)
        return response.json()

    def get_reviews(self, project, state='Opened', offset=0, limit=self._list_limit):
        """\
        https://www.jetbrains.com/help/space/projects-a.html#get_all_code_reviews
        @param state - Opened|Closed|RequiresAuthorAttention|NeedsReview|Merged
        """
        url = f'{self._api_url}/projects/{project}/code-reviews'
        params = self._get_params(get_data={
            '$skip': offset,
            '$top': limit,
            'state': state,
            'sort': 'CreatedAtDesc', # CreatedAtAsc|CreatedAtDesc|LastUpdatedAsc|LastUpdatedDesc
        })
        response = requests.get(url, **params)
        return response.json().get('data')

    def get_review(self, project, review):
        """\
        https://www.jetbrains.com/help/space/projects-a.html#get_code_review
        """
        url = f'{self._api_url}/projects/{project}/code-reviews/{review}'
        params = self._get_params()
        response = requests.get(url, **params)
        return response.json()

    def get_channels(self, offset=0, limit=self._list_limit):
        """\
        https://www.jetbrains.com/help/space/chats-a.html#list_all_channels
        """
        url = f'{self._api_url}/chats/channels/all-channels'
        params = self._get_params(get_data={
            'query': '',
            '$skip': offset,
            '$top': limit,
        })
        response = requests.get(url, **params)
        return response.json().get('data')

    def get_repos(self, project_key):
        """\
        https://www.jetbrains.com/help/space/projects-a.html#delete_repository
        """
        url = f'{self._api_url}/projects/repositories/find'
        params = self._get_params(get_data={
            'term': project_key,
        })
        response = requests.get(url, **params)
        return response.json().get('data')

    def delete_repo(self, project_id, repository):
        """\
        https://www.jetbrains.com/help/space/projects-a.html#delete_repository
        """
        url = f'{self._api_url}/projects/{project_id}/repositories/{repository}'
        params = self._get_params(post_data={})
        response = requests.delete(url, **params)
        return response.json()

    def get_blog_posts(self, offset=0, limit=self._list_limit):
        """\
        https://www.jetbrains.com/help/space/blog.html#get_all_blog_posts
        """
        url = f'{self._api_url}/blog'
        params = self._get_params(get_data={
            '$skip': offset,
            '$top': limit,
        })
        response = requests.get(url, **params)
        return response.json().get('data')

    def get_blog_post(self, post_id):
        """\
        https://www.jetbrains.com/help/space/blog.html#get_blog_post
        """
        url = f'{self._api_url}/blog/{post_id}'
        params = self._get_params()
        response = requests.get(url, **params)
        return response.json()

    def send_message(self, message, channel=None, username=None):
        """\
        https://www.jetbrains.com/help/space/chats-a.html#send_message
        @param message - markdown format string
        @param channel - channel id like '4Thxmq3nxtok' (random, for example)
        @param username - like 'pixel'
        """
        if not channel and not username:
            raise Exception('Must defined `channel` or `username`!')
        url = f'{self._api_url}/chats/messages/send-message'
        post_data = {
            'content': {
                'className': 'ChatMessage.Text',
                'text': message,
            },
        }
        if username:
            post_data['channel'] = {
                'className': 'ChannelIdentifier.Profile',
                'member': {
                    'className': 'ProfileIdentifier.Username',
                    'username': username,
                }
            }
        if channel:
            post_data['channel'] = {
                'className': 'ChannelIdentifier.Id',
                'id': channel,
            }
        params = self._get_params(post_data=post_data)
        response = requests.post(url, **params)
        return response.json()

    def space_repo_change_hook(self, project_key, repo_name):
        url = f'{self._base_url}/~external-push-notification/{project_key}/{repo_name}'
        requests.get(url)

    def _get_params(self, post_data=None, get_data=None):
        params = {
            'headers' : {
                'Accept': 'application/json',
                'Authorization': f'Bearer {self._token}',
            },
        }
        if post_data:
            params['data'] = json.dumps(post_data)
        if get_data:
            params['params'] = get_data
        return params
