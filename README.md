# API Development and Documentation Final Project

## Trivia App

Udacity is invested in creating bonding experiences for its employees and students. A bunch of team members got the idea to hold trivia on a regular basis and created a webpage to manage the trivia app and play the game, but their API experience is limited and still needs to be built out.

That's where you come in! Help them finish the trivia app so they can start holding trivia and seeing who's the most knowledgeable of the bunch. The application must:

1. Display questions - both all questions and by category. Questions should show the question, category and difficulty rating by default and can show/hide the answer.
2. Delete questions.
3. Add questions and require that they include question and answer text.
4. Search for questions based on a text query string.
5. Play the quiz game, randomizing either all questions or within a specific category.

Completing this trivia app will give you the ability to structure plan, implement, and test an API - skills essential for enabling your future applications to communicate with others.

## Starting and Submitting the Project

[Fork](https://help.github.com/en/articles/fork-a-repo) the project repository and [clone](https://help.github.com/en/articles/cloning-a-repository) your forked repository to your machine. Work on the project locally and make sure to push all your changes to the remote repository before submitting the link to your repository in the Classroom.

## About the Stack

We started the full stack application for you. It is designed with some key functional areas:

### Backend

The [backend](./backend/README.md) directory contains a partially completed Flask and SQLAlchemy server. You will work primarily in `__init__.py` to define your endpoints and can reference models.py for DB and SQLAlchemy setup. These are the files you'd want to edit in the backend:

1. `backend/flaskr/__init__.py`
2. `backend/test_flaskr.py`

> View the [Backend README](./backend/README.md) for more details.

### Frontend

The [frontend](./frontend/README.md) directory contains a complete React frontend to consume the data from the Flask server. If you have prior experience building a frontend application, you should feel free to edit the endpoints as you see fit for the backend you design. If you do not have prior experience building a frontend application, you should read through the frontend code before starting and make notes regarding:

1. What are the end points and HTTP methods the frontend is expecting to consume?
2. How are the requests from the frontend formatted? Are they expecting certain parameters or payloads?

Pay special attention to what data the frontend is expecting from each API response to help guide how you format your API. The places where you may change the frontend behavior, and where you should be looking for the above information, are marked with `TODO`. These are the files you'd want to edit in the frontend:

1. `frontend/src/components/QuestionView.js`
2. `frontend/src/components/FormView.js`
3. `frontend/src/components/QuizView.js`

By making notes ahead of time, you will practice the core skill of being able to read and understand code and will have a simple plan to follow to build out the endpoints of your backend API.

> View the [Frontend README](./frontend/README.md) for more details.

## API reference

### Getting Started
- Base URL: At present this app can only be run locally and is not hosted as a base URL. The backend app is hosted at the default, `http://127.0.0.1:5000/`, which is set as a proxy in the frontend configuration. 
- Authentication: This version of the application does not require authentication or API keys. 

### Error Handling
Errors are returned as JSON objects in the following format:
```
{
    "success": False, 
    "error": 400,
    "message": "bad request"
}
```
The API will return three error types when requests fail:
- 400: Bad Request
- 404: Resource Not Found
- 422: Not Processable 

### Endpoints

`GET '/categories'`
- General 
    - Fetches a dictionary of categories in which the keys are the ids and the value is the corresponding string of the category
    - Request Arguments: None
    - Returns: An object with a single key, `categories`, that contains an object of `id: category_string` key: value pairs and a success value.
- Sample URL
    -`curl http://127.0.0.1:5000/categories`

```json
{
    "categories": {
        "1": "Science",
        "2": "Art",
        "3": "Geography",
        "4": "History",
        "5": "Entertainment",
        "6": "Sports"
    },
    "success": true
}

```

---

`GET '/questions'`
- General 
    - Fetches a paginated set of questions, a total number of questions, all categories and current category string
    - Request Arguments: None
    - Returns: An object with 10 paginated questions, total questions, object including all categories, current category string and a success value
- Sample URL
    -`curl http://127.0.0.1:5000/questions`
    - Optionally append: `/?page=1`
    - The questions object here shows a list of two questions 

```json
{
    "categories": {
        "1": "Science",
        "2": "Art",
        "3": "Geography",
        "4": "History",
        "5": "Entertainment",
        "6": "Sports"
    },
    "current_category": null,
    "questions": [
        {
            "answer": "Apollo 13",
            "category": 5,
            "difficulty": 4,
            "id": 2,
            "question": "What movie earned Tom Hanks his third straight Oscar nomination, in 1996?"
        },
        {
            "answer": "Tom Cruise",
            "category": 5,
            "difficulty": 4,
            "id": 4,
            "question": "What actor did author Anne Rice first denounce, then praise in the role of her beloved Lestat?"
        }
    ],
    "success": true,
    "total_questions": 19
}

```

---

`DELETE '/questions/int:id'`
- General 
    - Deletes a specified question from database using the id of the question
    - Request Arguments: `id` integer type
    - Returns: An JSON object which contain id of deleted question, message and success value 
- Sample URL
    -`curl http://127.0.0.1:5000/questions/38 -X DELETE`

```json
{
    "deleted": 38,
    "message": "Question deleted successfully",
    "success": true
}

```

---

`POST '/questions'`
- General 
    - Creates a new question 
    - Request Arguments: Question object which contain question and answer text, difficulty score and category
    - Returns: A JSON object which contains a single new_question object, message and success value
- Sample URL
    -`curl -H "Content-Type: application/json" -d '{"question": "What is your name?", "answer": "Adetola Oyebode", "difficulty": 1, "category": 0}' -X POST http://127.0.0.1:5000/questions`

```json
{
    "message": "Question created successfully",
    "new_question": {
        "answer": "Adetola Oyebode",
        "category": 5,
        "difficulty": 1,
        "id": 44,
        "question": "What is your name?"
    },
    "success": true
}

```

---

`POST '/questions/search'`
- General 
    - Fetches a specific question based on a search query
    - Request Arguments: JSON object which contains search query
    - Returns: An array of question(s) for whom search query is a substring of the question and success value
- Sample URL
    -`curl -H "Content-Type: application/json" -d '{"search_term": "1930"}' -X POST http://127.0.0.1:5000/questions/search`

```json
{
    "questions": [
        {
            "answer": "Uruguay",
            "category": 6,
            "difficulty": 4,
            "id": 26,
            "question": "Which country won the first ever soccer World Cup in 1930?"
        }
    ],
    "success": true
}

```

---

`GET '/categories/int:id/questions'`
- General 
    - Fetches a specific question based on category
    - Request Arguments: id - integer
    - Returns: JSON object which contains the question for the specified category, total questions, current category and success value
- Sample
    -`curl http://127.0.0.1:5000/categories/3/questions`

```json
{
    "current_category": "Geography",
    "questions": [
        {
            "answer": "Lake Victoria",
            "category": 3,
            "difficulty": 2,
            "id": 13,
            "question": "What is the largest lake in Africa?"
        },
        {
            "answer": "The Palace of Versailles",
            "category": 3,
            "difficulty": 3,
            "id": 14,
            "question": "In which royal palace would you find the Hall of Mirrors?"
        },
        {
            "answer": "Agra",
            "category": 3,
            "difficulty": 2,
            "id": 15,
            "question": "The Taj Mahal is located in which Indian city?"
        }
    ],
    "success": true,
    "total_questions": 3
}

```

---

`POST '/quizzes'`
- General
    - Fetches random questions based on a specified category including all
    - Request Argument: None
    - Returns: A random question object of specified category and success value
- Sample
    - `curl 'http://127.0.0.1:5000/quizzes'`

```json
{
    "question": {
        "answer": "Apollo 13",
        "category": 5,
        "difficulty": 4,
        "id": 2,
        "question": "What movie earned Tom Hanks his third straight Oscar nomination, in 1996?"
    },
    "success": true,
    "total_questions": 19
}

```


