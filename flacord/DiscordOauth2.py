from flacord import scope
from flask import request, session, redirect, current_app

class DiscordOauth2Session:
    def __init__(self, app):
        self.app = app
        self.config = self.app.config
        self.base_url = 'https://discord.com/api/v9'
        self.oauth_url = self.base_url + '/oauth2/'
        self.get_token_url = self.oauth_url + '/token'

    def login(self,scope=scope.all()):
        scope = '%20'.join(scope)
        login_url = f"{self.oauth_url}authorize?client_id={self.config['DISCORD_CLIENT_ID']}&redirect_uri={self.config['DISCORD_REDIRECT_URI']}&response_type=code&scope={scope}"
        return redirect(login_url)

    def callback(self):
        authorization_code = request.args.get("code")

        request_postdata = {'client_id': self.config['DISCORD_CLIENT_ID'], 'client_secret': self.config['DISCORD_CLIENT_SECRET'], 'grant_type': 'authorization_code', 'code': authorization_code, 'redirect_uri': self.config['DISCORD_REDIRECT_URI']}
        accesstoken_request = requests.post(url=self.get_token_url, data=request_postdata)

        responce_json = accesstoken_request.json()

        session['access_token'] = responce_json['access_token']
        session['token_type'] = responce_json['token_type']
        session['expires_in'] = responce_json['expires_in']
        session['refresh_token'] = responce_json['refresh_token']
        session['scope'] = responce_json['scope']
        
        return
