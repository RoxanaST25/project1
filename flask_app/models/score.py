from flask_app.config.mysqlconnection import connectToMySQL
from flask import flash

class Score:
    db = 'project_folder'

    def __init__(self,data):
        self.id = data['id']
        self.score = data['score']
        self.user_id = data['user_id']
        self.created_at = data['created_at']
        self.updated_at = data['updated_at']

    @classmethod
    def get_all(cls):
        query = "SELECT * FROM paitings;"
        results =  connectToMySQL(cls.db).query_db(query)
        paintings = []
        for x in results:
            paintings.append( cls(x) )
        return paintings
        
    @classmethod
    def save(cls,data):
        query = "INSERT INTO paintings (title, description, price, created_at, updated_at, painted_by, user_id) VALUES (%(title)s,%(description)s,%(price)s, NOW(), NOW(), %(painted_by)s,%(user_id)s);"
        return connectToMySQL(cls.db).query_db(query, data)
    
    @classmethod
    def get_painting(cls,data):
        query = "SELECT * FROM paintings WHERE id = %(id)s;"
        results = connectToMySQL(cls.db).query_db(query,data)
        return cls( results[0] )

    @classmethod
    def update(cls, data):
        query = "UPDATE paintings SET title=%(title)s, description=%(description)s, price=%(price)s, updated_at=NOW() WHERE id = %(id)s;"
        return connectToMySQL(cls.db).query_db(query,data)
    
    @classmethod
    def delete(cls,data):
        query = "DELETE FROM paintings WHERE id = %(id)s;"
        return connectToMySQL(cls.db).query_db(query,data)

    @staticmethod
    def validate_painting(painting):
        is_valid = True
        if len(painting['title']) < 2:
            is_valid = False
            flash("Title must be at least 2 characters","painting")
        if len(painting['description']) < 10:
            is_valid = False
            flash("Description must be at least 10 characters","painting")
        if float(painting['price']) <= 0:
            is_valid = False
            flash("Please enter a price greater than 0","painting")
        return is_valid
