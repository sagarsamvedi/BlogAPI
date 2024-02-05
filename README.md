# DjangoREST Blog API

This project is a robust DjangoREST API serving as the backend for a simple yet powerful blogging platform. The API offers comprehensive functionality for users to create, read, update, and delete blog posts. It also incorporates user authentication and authorization for secure access. Additionally, the API implements pagination for efficient listing, provides a way to retrieve a random blog post for public users, and features a flexible search functionality to find specific blogs by title or content.

## Features

- **User Authentication and Authorization:** Secure user registration and login, with proper authorization for CRUD operations.
- **Blog Management:** CRUD operations for creating, reading, updating, and deleting blog posts.
- **Pagination:** Efficiently navigate through paginated lists of blog posts.
- **Random Post Retrieval:** Retrieve a random blog post for a unique reading experience.
- **Search Functionality:** Easily find specific blogs by title or content.

## Technologies Used

- **DjangoREST Framework:** A powerful toolkit for building Web APIs in Django.
- **Django:** The web framework for perfectionists with deadlines.


## Getting Started

Follow these steps to get the project up and running on your local machine:

1. **Clone the Repository:**

   ```bash
   git clone https://github.com/sagarsamvedi/BlogAPI.git
   cd BlogAPI
    ```
2. **Install Dependencies:**
   ```python
   pip install -r requirements.txt
   ```
3. **python manage.py migrate**
    ```python
   python manage.py migrate
   ```
4. **Create a Superuser (Optional):**
    ```python
   python manage.py createsuperuser
   ```
5. **Run the Development Server:**
    ```python
   python manage.py runserver
   ```
6. **Access the API:**
   Open your browser and navigate to http://localhost:8000/ to explore the API using the Browsable API.

## API Endpoints
- User Registration: POST /api/account/register
- User Login: POST /api/account/login
- Create Blog Post through authenticated user: POST /api/home/blog
- Get Blog Post through authenticated user: GET /api/home/blog
- List Blog Posts with Pagination and random blogs: GET /api/home/?page=
- Search Blog Posts by Title or Content: GET /api/homme/blog/?search=

## Contributing
Contributions are welcome! If you have ideas for improvements, open issues or pull requests. Let's build a better blogging experience together.

   
