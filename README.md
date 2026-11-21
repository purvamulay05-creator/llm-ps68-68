# 📧 Marketing Email Generator

An AI-powered web application that helps small businesses create professional promotional marketing emails for festivals, special occasions, and offers.

## 📌 Problem Statement

Small businesses often struggle to create attractive and professional marketing emails due to limited time, resources, and access to professional copywriters.

This project provides an AI-powered solution that automatically generates two unique promotional email variations based on business details and the selected marketing tone.

## ✨ Features

- Enter shop or business name.
- Specify a festival or special occasion.
- Provide promotional offers and discounts.
- Select an email tone such as Friendly, Professional, Exciting, Creative, Persuasive, or Festive.
- Generate two unique marketing email variations using Google Gemini AI.
- View generated email subjects and formatted email content.
- Download generated emails as a text file.
- Simple and user-friendly Streamlit interface.

## 🛠️ Technologies Used

- **Python** – Application development
- **Streamlit** – Web application interface
- **Google Gemini API** – AI-powered email generation
- **Google Gen AI SDK** – Communication with Gemini
- **python-dotenv** – Secure environment variable management

## ⚙️ How to Run the Project

### 1. Clone the repository

```bash
git clone YOUR_GITHUB_REPOSITORY_URL
```

### 2. Open the project folder

```bash
cd Marketing_Email_Generator
```

### 3. Create a virtual environment

```bash
python -m venv venv
```

### 4. Activate the virtual environment

Windows:

```bash
venv\Scripts\activate
```

### 5. Install dependencies

```bash
pip install -r requirements.txt
```

### 6. Configure the Gemini API key

Create a `.env` file in the project folder and add:

```env
GEMINI_API_KEY=gemini_api_key
GEMINI_MODEL=gemini-3.5-flash-lite
```


### 7. Run the application

```bash
streamlit run app.py
```

The application will open in your browser.

## 📸 Screenshots

Add your application screenshots in a folder named `screenshots`.

- Application homepage
- User input form
- Generated email variations
- Download option

## 🚀 Future Enhancements

- Support for multiple languages.
- More customizable email templates.
- Direct email sending integration.
- Download emails in PDF format.
- Additional AI-powered marketing suggestions.

## 👩‍💻 Project Information

**Project:** Marketing Email Generator  
**Developer:** Purva Manoj Mulay   
**Roll Number:** 68 
**Class:** LY-CORE-01
**Enrollment Number:** ADT23SOCB0813

---

Developed using Python, Streamlit, and Google Gemini AI.