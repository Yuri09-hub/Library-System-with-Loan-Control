# Library System with Loan Control

## Overview
This project is a backend system designed to manage a library environment.  
It provides functionality for managing books, users, and borrowing operations.  
The system allows users to borrow and return books while tracking loan records and maintaining book availability.

## Features

- Book management (add, update, delete books)
- User management
- Borrow and return book system
- Loan tracking
- Inventory control for books
- Loan history management
- Validation of borrowing rules

## Technologies Used

- Python
- FastAPI
- SQLAlchemy (ORM)
- SQLite / relational database
- REST API

## Project Structure

project/

├── models/ # Database models  
├── routes/ # API routes  
├── schemas/ # Data validation schemas  
├── database/ # Database configuration  
└── main.py # Application entry point  

## Installation

1. Clone the repository

git clone https://github.com/Yuri09-hub/Library-System-with-Loan-Control

2. Enter the project folder

cd Library-System-with-Loan-Control

3. Create virtual environment

python -m venv venv

4. Activate environment

venv\Scripts\activate

5. Install dependencies

pip install -r requirements.txt

## Running the API

uvicorn main:app --reload

API documentation:

http://127.0.0.1:8000/docs

## System Logic

- Books can be registered and managed by the system.
- Users can borrow available books.
- Each loan is recorded with a return deadline.
- When a book is returned, the system updates its availability automatically.

## Author

Yuri Rodrigues    
Angola
