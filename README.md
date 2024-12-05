# test-SDO
Test de candidature - Réalisation d’un mini-projet  Dans le cadre de notre processus de recrutement, nous vous invitons à réaliser un mini-projet, à livrer dans un délai d’une semaine.  Ce projet consiste en la création d’une application web TO-DO LIST

Here is a README file based on your instructions:

---

# Project Setup Instructions

This guide provides step-by-step instructions to execute the project, including setting up the backend server and frontend client.

---

## **Prerequisites**
Ensure you have the following installed on your machine:
- **Python 3.9+**
- **Node.js 16+ and npm**
- **MySQL Database**
- **pip** (Python package installer)
- **Alembic** (for database migrations)
- **Uvicorn** (ASGI server)

---

## **Backend Setup**

1. **Clone the Repository**  
   ```bash
   git clone <repository-url>
   cd server
   ```

2. **Install Python Dependencies**  
   Use the `requirements.txt` file to install the required dependencies:  
   ```bash
   pip install -r requirements.txt
   ```

3. **Configure the Database**  
   Update the `app/.env` file with your database and JWT configuration:  
   ```dotenv
   # Database configuration
   DB_USER=<your-database-username>
   DB_PASSWORD=<your-database-password>
   DB_HOST=localhost
   DB_PORT=<your-database-port>
   DB_NAME=<your-database-name>

   # JWT configuration
   SECRET_KEY=<your-secret-key>
   ALGORITHM=HS256
   ACCESS_TOKEN_EXPIRE_MINUTES=30
   ```

4. **Alembic Configuration**  
   Update the `alembic.ini` file:  
   ```ini
   sqlalchemy.url = mysql+pymysql://<DB_USER>:<DB_PASSWORD>@<DB_HOST>:<DB_PORT>/<DB_NAME>
   ```

5. **Run Database Migrations**  
   Navigate to the migrations folder and apply the existing migrations:  
   ```bash
   alembic upgrade head
   ```

6. **Start the Backend Server**  
   Run the server using Uvicorn:  
   ```bash
   uvicorn app.app:app --reload
   ```

7. **Verify Backend Setup**  
   - Access the default route: [http://127.0.0.1:8000](http://127.0.0.1:8000)  
   - API documentation is available at [http://127.0.0.1:8000/docs](http://127.0.0.1:8000/docs).  

   > **Note:** The `/users` endpoint is not configured as it is intended for admin use.

---

## **Frontend Setup**

1. **Navigate to the Client Folder**  
   ```bash
   cd ..
   cd client
   ```

2. **Install Dependencies**  
   Use npm to install the required packages:  
   ```bash
   npm install
   npm audit fix --force
   ```

3. **Run the Frontend Development Server**  
   Start the frontend server:  
   ```bash
   npm run dev
   ```

4. **Verify Frontend Setup**  
   - Access the frontend at [http://localhost:3000](http://localhost:3000).

---

## **Testing the Project**
- Use Postman or manual HTTP requests to test the backend endpoints.
- Interact with the frontend through your browser to validate its functionality.

---

Let me know if you need further assistance!
