from flask_app.config.mysqlconnection import connectToMySQL
from flask import flash

from flask_app.models import user


class Sasquatch:
    db="sasquatches_schema"

    def __init__(self, data):
        self.id = data['id']
        self.location = data['location']
        self.what_happened = data['what_happened']
        self.date_of_siting = data['date_of_siting']
        self.number_of_sasquatches = data['number_of_sasquatches']
        self.user_id = data['user_id']
        self.created_at = data['created_at']
        self.updated_at = data['updated_at']
        self.creator = None

#create a new sasquatch
    @classmethod
    def create_sasquatch(cls, data):
        query="""
            INSERT INTO sasquatches (location, what_happened, date_of_siting, number_of_sasquatches, user_id)
            VALUES (%(location)s, %(what_happened)s, %(date_of_siting)s, %(number_of_sasquatches)s, %(user_id)s);
        """
        return connectToMySQL(cls.db).query_db(query, data)

#view all sasquatches
    @classmethod
    def get_all_sasquatches(cls):
        query="""
            SELECT * FROM sasquatches
            JOIN users ON sasquatches.user_id = users.id;
        """
        results =connectToMySQL(cls.db).query_db(query)

        all_sasquatches=[]

        for row in results:
            one_sasquatch = cls(row)

            user_data={
                'id': row['user_id'],
                'first_name': row['first_name'],
                'last_name': row['last_name'],
                'email': row['email'],
                'password': row['password'],
                'created_at': row['created_at'],
                'updated_at': row['updated_at']
            }
            one_sasquatch.creator = user.User(user_data)
            all_sasquatches.append(one_sasquatch)
        return all_sasquatches

# # view one sasquatch
    @classmethod
    def get_one_sasquatch(cls,data):
        query="""
            SELECT * FROM sasquatches
            JOIN users ON sasquatches.user_id = users.id
            WHERE sasquatches.id = %(id)s;
        """

        results =connectToMySQL(cls.db).query_db(query,data)

        one_sasquatch = cls(results[0])

        user_data={
                'id': results[0]['users.id'],
                'first_name': results[0]['first_name'],
                'last_name': results[0]['last_name'],
                'email': results[0]['email'],
                'password': results[0]['password'],
                'created_at': results[0]['created_at'],
                'updated_at': results[0]['updated_at']
        }

        one_sasquatch.creator = user.User(user_data)

        return one_sasquatch
    

#update
    @classmethod
    def update_sasquatch(cls,data):
        query="""
            UPDATE sasquatches
            SET location=%(location)s, what_happened=%(what_happened)s, date_of_siting=%(date_of_siting)s, number_of_sasquatches=%(number_of_sasquatches)s
            WHERE id=%(id)s;
        """
        return connectToMySQL(cls.db).query_db(query,data)


#delete a sasquatch
    @classmethod
    def delete_sasquatch(cls,data):
        query="""
            DELETE FROM sasquatches
            WHERE id = %(id)s;
        """
        return connectToMySQL(cls.db).query_db(query,data)


#validations
    @staticmethod
    def validate_sasquatch(data):
        is_valid = True

        if len(data['location']) == 0:
            is_valid = False
            flash('Location is required', 'sasquatch')
        if len(data['what_happened']) == 0:
            is_valid = False
            flash('What happened cannot be left empty', 'sasquatch')
        if len(data['date_of_siting']) == 0:
            is_valid = False
            flash('Date is required', 'sasquatch')
        if len(data['number_of_sasquatches']) == 0:
            is_valid = False
            flash('At least 1 sasquatch has to be seen', 'sasquatch')
        return is_valid
