from flask_app.config.mysqlconnection import connectToMySQL
from flask_app.models.user import User
from flask import flash

class Score:
    db = 'project_folder'


    def __init__(self,data):
        self.id = data['id']
        self.score = data['score']
        self.user_id = data['users_id']
        self.created_at = data['created_at']
        self.updated_at = data['updated_at']
        self.user = User.get_user({"id": self.user_id})

    @classmethod
    def get_all(cls):
        query = "SELECT * FROM scores;"
        results =  connectToMySQL(cls.db).query_db(query)
        scores = []
        for x in results:
            scores.append( cls(x) )
        return scores
        
    @classmethod
    def save(cls,data):
        query = "INSERT INTO scores (score, created_at, updated_at, users_id) VALUES (%(score)s, NOW(), NOW(), %(users_id)s);"
        return connectToMySQL(cls.db).query_db(query, data)
    
    @classmethod
    def get_scores(cls,data):
        query = "SELECT * FROM scores WHERE id = %(id)s;"
        results = connectToMySQL(cls.db).query_db(query,data)
        return cls( results[0] )

    
    @classmethod
    def delete(cls,data):
        query = "DELETE FROM scores WHERE id = %(id)s;"
        return connectToMySQL(cls.db).query_db(query,data)

    @staticmethod
    def validate_option(option):
        print(option)
        is_valid = True
        if not option:
            is_valid = False
            flash("Select an answer","answer")
        if len(option.keys()) > 1:
            is_valid = False
            flash("Select only one answer","answer")
        return is_valid

class QuestionList:
    def __init__(self):
        self.questions = [
            Question(
                "In what year were the first Air Jordan sneakers released?",
                0,
                [
                    "1984",
                    "2020",
                    "1999"
                ]
            ),
            Question(
                "In a bingo game, which number is represented by the phrase “two little ducks”?",
                1,
                [
                    "30",
                    "22",
                    "29"
                ]
            ),
            Question(
                "According to Greek mythology, who was the first woman on earth?",
                2,
                [
                    "Alejandra",
                    "Elizabeth",
                    "Pandora"
                ]
            ),
            Question(
                "What is the loudest animal on Earth?",
                0,
                [
                    "The sperm whale",
                    "Bears",
                    "Elephants"
                ]
            ),
            Question(
                "What was the first toy to be advertised on television?",
                1,
                [
                    "Mickey Mouse",
                    "Mr.Potato Head",
                    "Transformers"
                ]
            )
        ]

class Question:
    
    def __init__(self, question, answer, options):
        self.question = question
        self.answer = answer
        self.options = options