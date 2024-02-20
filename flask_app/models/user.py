from flask_app.config.mysqlconnection import connectToMySQL
from flask import flash
from flask_app import app, bcrypt
import re
EMAIL_REGEX = re.compile(r'^[a-zA-Z0-9.+_-]+@[a-zA-Z0-9._-]+\.[a-zA-Z]+$')


class User:
    db="sasquatches_schema"

    def __init__(self, data):
        self.id = data['id']
        self.first_name = data['first_name']
        self.last_name = data['last_name']
        self.email = data['email']
        self.password = data['password']
        self.created_at = data['created_at']
        self.updated_at = data['updated_at']
        self.sasquatches = []

#create user
    @classmethod
    def create_user(cls,data):
        query = """
            INSERT INTO users (first_name, last_name, email, password)
            VALUES (%(first_name)s, %(last_name)s, %(email)s, %(password)s)
        """
        return connectToMySQL(cls.db).query_db(query, data)

#view user
    @classmethod
    def get_user_by_email(cls,data):
        query = """
            SELECT * FROM users 
            WHERE email = %(email)s;
        """
        results = connectToMySQL(cls.db).query_db(query, data)

        if len(results) <1:
            return False
        
        return cls(results[0])
    
#view user by id
    @classmethod
    def get_user_by_id(cls,data):
        query = """
            SELECT * FROM users 
            WHERE id = %(id)s;
        """
        results = connectToMySQL(cls.db).query_db(query, data)

        return cls(results[0])
    

#validations for user
    @staticmethod
    def validate_registration(data):
        is_valid = True
        one_user = User.get_user_by_email(data)

        if one_user:
            is_valid = False
            flash('Please login', 'reg')
        if len(data['first_name']) <2:
            is_valid = False
            flash('First name must be at least 2 characters long', 'reg')
        if len(data['last_name']) <2:
            is_valid = False
            flash('Last name must be at least 2 characters long', 'reg')
        if len(data['email']) ==0:
            is_valid = False
            flash('Email cannot be empty')
        elif not EMAIL_REGEX.match(data['email']):
            is_valid=False
            flash('Invalid email format', 'reg')
        if len(data['password']) <8:
            is_valid = False
            flash('Password must be at least 8 characters long', 'reg')
        if len(data['confirm_password']) <8:
            is_valid = False
            flash('Confirm password must be at least 8 characters long', 'reg')
        if data['password'] != data['confirm_password']:
            is_valid = False
            flash('Passwords do not match','reg')
        return is_valid
    
    @staticmethod
    def validate_login(data):
        one_user = User.get_user_by_email(data)

        if not one_user:
            flash('Invalid credentials','login')
            return False
        if not bcrypt.check_password_hash(one_user.password, data['password']):
            flash('Invalid credentials','login')
            return False
        return one_user
    
