Todo List API
Assignment: Build a Todo List API
Required Features
User signup/login
Create, read, update, delete todos
Mark todos as complete/incomplete
Basic user profile
Simple task categories
Technical Requirements
FastAPI framework
MongoDB database
Basic authentication
API documentation using FastAPI's built-in Swagger
2 basic test cases
Bonus Features (Optional)
Due date for todos
Priority levels
Basic search functionality
Installation
Clone the repository:

bash
git clone https://github.com/Vaishnavi2282/to-do-list.git
cd to-do-list
Create and activate a virtual environment:

bash
python3 -m venv venv
source venv/bin/activate  # On Windows use `venv\Scripts\activate`
Install the required dependencies:

pip install -r requirements.txt
Set up MongoDB and update the connection string in the configuration file.

Usage
Run the FastAPI application:

uvicorn main:app --reload
Access the API documentation at http://127.0.0.1:8000/docs.

Features
User Authentication
Signup: Create a new account.
Login: Authenticate and receive a token.
Todo Management
Create Todo: Add a new todo item.
Read Todos: Retrieve a list of todos.
Update Todo: Modify an existing todo item.
Delete Todo: Remove a todo item.
Mark Complete/Incomplete: Update the status of a todo.
User Profile
Basic Profile: View and edit user profile information.
Task Categories
Categories: Organize todos into simple categories.
Bonus Features
Due Date: Set a due date for todos.
Priority Levels: Assign priority levels to todos.
Search: Basic search functionality to find todos.
Testing
Run the test cases using:

pytest

Contributing
Contributions are welcome! Please open an issue or submit a pull request for any improvements or additions.

License
This project is licensed under the MIT License. See the LICENSE file for details.

Contact
For any questions or support, please open an issue in this repository.
