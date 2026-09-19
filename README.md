# AI Interview Coach

AI Interview Coach is a full-stack web application designed to help users practice for interviews in a structured and interactive way. The app allows users to choose a role, answer role-based interview questions, receive instant feedback, and track their interview performance over time.

## Features

- User registration and login
- Role-based interview question selection
- Real-time response evaluation and score updates
- Feedback suggestions for improving answers
- Interview history dashboard
- SQLite database integration for storing user and interview data
- Responsive design for better user experience

## Tech Stack

- Python
- Flask
- SQLite
- HTML
- CSS
- Bootstrap
- Jinja2 Templates

## Project Flow

1. User creates an account or logs in.
2. User selects an interview role such as Software, Data, or Marketing.
3. The app presents interview questions one by one.
4. User provides answers and receives instant feedback.
5. The application calculates a score and saves result history.
6. User can review previous interview attempts in the dashboard.

## Local Setup

### 1. Clone the repository

```bash
git clone https://github.com/YOUR_USERNAME/AI-Interview-Coach.git
cd AI-Interview-Coach
```

### 2. Create a virtual environment

```bash
python -m venv venv
```

On Windows:

```bash
venv\Scripts\activate
```

On macOS/Linux:

```bash
source venv/bin/activate
```

### 3. Install dependencies

```bash
pip install -r requirements.txt
```

### 4. Configure environment variables

Create a `.env` file using the example file:

```bash
copy .env.example .env
```

Then update the values if needed.

### 5. Run the application

```bash
python app.py
```

Open your browser and visit:

```text
http://127.0.0.1:5000/
```

## Project Structure

```text
AI-Interview-Coach/
├── app.py
├── interview.db
├── README.md
├── requirements.txt
├── .gitignore
├── .env.example
├── static/
│   └── style.css
├── templates/
│   ├── dashboard.html
│   ├── final.html
│   ├── home.html
│   ├── index.html
│   ├── login.html
│   ├── register.html
│   ├── result.html
│   └── role.html
└── venv/
```

## Future Enhancements

- Add AI-powered answer evaluation using OpenAI or Gemini API
- Add audio/video interview simulation
- Add performance analytics and charts
- Add resume/job-role matching module
- Add advanced interview scoring and personalized recommendations

## License

This project is for educational and portfolio purposes.
