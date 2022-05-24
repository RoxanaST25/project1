from flask_app.config.mysqlconnection import connectToMySQL
from flask import flash
import re	

EMAIL_REGEX = re.compile(r'^[a-zA-Z0-9.+_-]+@[a-zA-Z0-9._-]+\.[a-zA-Z]+$')

class User:
    db = "project_folder"

    def __init__(self,data):
        self.id = data['id']
        self.first_name = data['first_name']
        self.email = data['email']
        self.password = data['password']
        self.created_at = data['created_at']
        self.updated_at = data['updated_at']

    @classmethod
    def save(cls,data):
        query = "INSERT INTO users (first_name,email,password) VALUES(%(first_name)s,%(email)s,%(password)s)"
        return connectToMySQL(cls.db).query_db(query,data)    #this is what is making my first id for a new user

    @classmethod
    def get_user_with_email(cls,data):
        query = "SELECT * FROM users WHERE email = %(email)s;"
        results = connectToMySQL(cls.db).query_db(query,data)
        print(results)
        if len(results) < 1:
            
            return False
        return cls(results[0])

    @classmethod
    def get_user(cls,data):
        query = "SELECT * FROM users WHERE id = %(id)s;"
        results = connectToMySQL(cls.db).query_db(query,data)
        print(results)
        return cls(results[0])

    @staticmethod
    def validate(user):
        is_valid = True
        query = "SELECT * FROM users WHERE email = %(email)s;"
        results = connectToMySQL(User.db).query_db(query,user)
        if results:
            flash("Email already registered.","register")
            is_valid=False
        if not EMAIL_REGEX.match(user['email']):
            flash("Invalid Email!","register")
            is_valid=False
        if len(user['first_name']) < 2:
            flash("First name must be at least 2 characters.","register")
            is_valid= False
        
        if len(user['password']) < 8:
            flash("Password must be at least 8 characters.","register")
            is_valid= False
        if user['password'] != user['confirm']:
            flash("Passwords do not match.","register")
        return is_valid


    @staticmethod
    def edit_validate(user):
        is_valid = True
        query = "SELECT * FROM users WHERE email = %(email)s;"
        results = connectToMySQL(User.db).query_db(query,user)
        if not EMAIL_REGEX.match(user['email']):
            flash("Invalid Email!","register")
            is_valid=False
        if len(user['first_name']) < 2:
            flash("First name must be at least 2 characters.","register")
            is_valid= False
        return is_valid

    @classmethod
    def update(cls, data):
        query = "UPDATE users SET first_name=%(first_name)s, email=%(email)s, updated_at=NOW() WHERE id = %(id)s;"
        return connectToMySQL(cls.db).query_db(query,data)