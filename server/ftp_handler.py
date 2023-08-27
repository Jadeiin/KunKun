import sqlite3
from pyftpdlib.authorizers import DummyAuthorizer, AuthenticationFailed
from socket_handler import db


class SQLiteAuthorizer(DummyAuthorizer):

    def validate_authentication(self, user_name, user_pwd_sha1, handler):

        if db.query_user_login(user_name, user_pwd_sha1) is not None:
            # 验证成功，添加用户到 authorizer 中
            try:
                self.add_user(user_name, user_pwd_sha1,
                              homedir="files/", perm='radfwMT')
            except:
                pass
        else:
            raise AuthenticationFailed("Authentication failed")
