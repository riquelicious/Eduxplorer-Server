from flask import  request, jsonify


from .RequestManager import RequestHandler

class AccountManager:
    def __init__(self):
        self.requester = RequestHandler()

    def create_account(self):
        data = request.get_json()
        account = {"username": data["username"], "password": data["password"], "email": data["email"], "account_type": data["account_type"]}
        result = self.requester.insert_account( account )
        print(result)
        return result

    def login(self):
        data = request.get_json()
        email = data["email"]
        password = data["password"]
        result = self.requester.login( email, password )
        return result        

    def change_password(self, username, old_password, new_password):
        pass
