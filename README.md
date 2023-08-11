# RestApi

Imports: 
Importing necessary modules for application, including Flask, jsonify for JSON responses, sqlite3 for database operations, requests for making HTTP requests, and json for manual JSON serialization.

Flask App Setup:
Create a Flask app instance named app.
Define a constant DATABASE for the SQLite database file name.

Database Operations:
create_table(): This function connects to the SQLite database and creates a table named 'users' with specified columns if it doesn't already exist.
save_user(user): This function saves a user's data into the 'users' table in the database.
fetch_users_by_first_name(first_name): This function queries the database to retrieve user records that match the provided first name. It converts the rows to dictionaries and orders the keys as desired.

API Endpoints:
search_users_in_database(first_name): This function fetches users by their first name from the database or an external API. If users are found in the database, it manually serializes the data using json.dumps to ensure the desired key order is preserved in the JSON response.
/api/users Endpoint:
When accessed via POST, it expects a 'first_name' parameter in the form data. It then searches for users by that first name and returns the data as a JSON response.
When accessed via GET, it displays a simple HTML form to search for users by first name.

Home Page:
The root route '/' simply displays a link to the user search page.

App Run:
The create_table() function is called to ensure the database table is created if it doesn't exist.
The Flask app is run in debug mode when the script is directly executed.
