To-Do List API
The To-Do List API is a robust and secure backend service for managing to-do lists with user authentication and data privacy. It offers the following features:

Features

User Authentication:
User registration with username and password.
User login with JWT (JSON Web Token) token generation.
Token validation ensures secure authentication.

To-Do List Operations:
Create: Create new to-do lists.
Read: View your own to-do lists.
Update: Modify existing to-do lists.
Delete: Delete your to-do lists.
To-Do Item Operations:
Perform CRUD (Create, Read, Update, Delete) operations on individual to-do items within your lists.

Data Isolation:
Strict data isolation ensures that users can only access and manage their own to-do lists and items.

JWT Token Security:
Robust JWT token security:
Token signing prevents tampering.
Expiration times enhance security.
Token refresh mechanism for secure user sessions.
