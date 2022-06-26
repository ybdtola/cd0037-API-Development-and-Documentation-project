import os
from unicodedata import category
from flask import Flask, request, abort, jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_cors import CORS
import random

from models import setup_db, Question, Category

QUESTIONS_PER_PAGE = 10

def create_app(test_config=None):
    # create and configure the app
    app = Flask(__name__)
    setup_db(app)

    """
    @TODO: Set up CORS. Allow '*' for origins. Delete the sample route after completing the TODOs
    """
    # CORS(app, resources={r"/api/*": {"origins": "*"}})
    CORS(app)


    @app.after_request
    def after_request(response):
        response.headers.add('Access-Control-Allow-Headers', 'Content-Type,Authorization,true')
        response.headers.add('Access-Control-Allow-Methods', 'GET,PUT,POST,DELETE,OPTIONS')
        return response


    @app.route('/categories')
    def get_categories():

        categories = Category.query.all()
        
        if(len(categories) == 0 ):
            abort(404)
        else:
            categories_dict = {}
            for category in categories:
                categories_dict[category.id] = category.type
            return jsonify({
                'success': True,
                'categories': categories_dict
            })

        

    @app.route('/questions')
    def get_questions_per_page():

        page = request.args.get('page', 1, type=int)
        start = (page - 1) * QUESTIONS_PER_PAGE
        end = start + QUESTIONS_PER_PAGE

        current_questions = Question.query.order_by(Question.id).slice(start, end).all()

        if(len(current_questions) == 0):
            abort(404)
        else:
            formatted_questions = [question.format() for question in current_questions]
            total_questions = Question.query.count()
            categories = Category.query.all()
            categories_dict = {}
            for category in categories:
                categories_dict[category.id] = category.type
            return jsonify({
                'success': True,
                'questions': formatted_questions,
                'total_questions': total_questions,
                'categories': categories_dict,
                'current_category': None
            })
    
    
    
    @app.route('/questions/<int:question_id>', methods=['DELETE'])
    def delete_question(question_id):

        question = Question.query.get(question_id)

        if question is None:
            abort(404)
        else:
            question.delete()
            return jsonify({
                'success': True,
                'deleted': question_id,
                'message': 'Question deleted successfully'
            })


    @app.route('/questions', methods=['POST'])
    def add_question():

        body = request.get_json()

        new_question = body.get('question')
        new_answer = body.get('answer')
        new_difficulty = body.get('difficulty')
        new_category = body.get('category')
        search_term = body.get('searchTerm')

        try:
            if search_term:
                # category = Category.query.get(id)

                questions = Question.query.filter(Question.question.ilike('%' + search_term + '%')).all()
                formatted_questions = [question.format() for question in questions]
                # category_question = [question.category for question in questions]

                
                # id = category_question[0]
                # category = Category.query.filter_by(id=id).all()
                # category_id = [category_name.type for category_name in category]
                # print(category_id)
                # cc = category_id[0]
                # total_questions = len(formatted_questions)
                return jsonify({
                    'success': True,
                    'questions': formatted_questions,
                    # 'total_questions': total_questions,
                    # 'current_category': cc
                })
                
            else:

                if new_question is None or new_answer is None:
                    abort(400)

                newquestion = Question(question=new_question, answer=new_answer, difficulty=new_difficulty, category=new_category)

                newquestion.insert()

                new_question_query = Question.query.filter_by(question=new_question).all()
                
                for question in new_question_query:
                    new_question_query = question.format()

                return jsonify({
                    'success': True,
                    'new_question': new_question_query,
                    'message': 'Question created successfully'
                })
        except:
            abort(422)


    @app.route('/questions/search', methods=['POST'])
    def search_questions():

        page = request.args.get('page', 1, type=int)
        start = (page - 1) * QUESTIONS_PER_PAGE
        end = start + QUESTIONS_PER_PAGE

        body = request.get_json()
        search_term = body.get('searchTerm', '')
        # category = Category.query.get(id)
        questions = Question.query.filter(Question.question.ilike('%' + search_term + '%')).all()
        formatted_questions = [question.format() for question in questions]

        if(len(formatted_questions) == 1):
            category_question = [question.category for question in questions]
            id = category_question[0]
            category = Category.query.filter_by(id=id).all()
            category_id = [category_name.type for category_name in category]
            cc = category_id[0]
            total_questions = len(formatted_questions)
            return jsonify({
                'success': True,
                'questions': formatted_questions,
                'total_questions': total_questions,
                'current_category': cc
            })
        else:
            return jsonify({
                'success': True,
                'questions': formatted_questions
            })
        
    
    @app.route('/categories/<int:id>/questions')
    def get_questions_by_category(id):
        category = Category.query.get(id)
        if category is None:
            abort(404)
        questions = Question.query.filter(Question.category == id).all()
        formatted_questions = [question.format() for question in questions]
        total_questions = Question.query.filter(Question.category == id).count()
        return jsonify({
            'success': True,
            'questions': formatted_questions,
            'total_questions': total_questions,
            'current_category': category.type
        })


    @app.route('/quizzes', methods=['POST'])
    def get_quiz_questions():
        try:
            body = request.get_json()

            previous_question = body.get('previous_questions', '')
            quiz_category = body.get('quiz_category', '')

            if (previous_question is None) or (quiz_category is None):
                abort(404)

            if quiz_category['id'] == 0:
                questions = Question.query.all()
            else:
                questions = Question.query.filter_by(
                        category=quiz_category['id']).all()

            formatted_questions = [question.format() for question in questions]
            total_questions = len(formatted_questions)
            random_question = random.choice(formatted_questions)
            return jsonify({
                'success': True,
                'question': random_question,
                'total_questions': total_questions
            })
        except:
            abort(422)


    @app.errorhandler(400)
    def bad_request(error):
        return jsonify({
            "success": False,
            "error": 400,
            "message": "Bad Request"
        })

    @app.errorhandler(404)
    def not_found(error):
        return jsonify({
            "success": False,
            "error": 404,
            "message": "Resource Not Found"
        })

    @app.errorhandler(405)
    def method_not_allowed(error):
        return jsonify({
            "success": False,
            "error": 405,
            "message": "Method Not Allowed"
        })
   
    @app.errorhandler(422)
    def unprocessible(error):
        return jsonify({
            "success": False,
            "error": 422,
            "message": "Unprocessible Entity"
        })
    return app

