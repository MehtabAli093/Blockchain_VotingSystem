# Blockchain-Based Secure Voting System

A tamper-proof, transparent, and secure voting system built using Python Flask, MongoDB, and a custom SHA-256 blockchain with Proof-of-Work.

## Overview

The Blockchain-Based Secure Voting System is a prototype developed to enhance the integrity of digital voting processes. Leveraging blockchain technology, it ensures secure voter authentication, prevents double voting, and provides tamper-proof vote storage with real-time result visibility. The system features a user-friendly, mobile-responsive interface built with Tailwind CSS and is designed for scalability and transparency.

This project was developed by Mehtab Ahmed  as a Semester Project for the Department of Cyber Security at FAST NUCES.

## Features

- **Secure Voter Authentication**: SHA-256 hashed passwords and CSRF protection for safe login.
- **Tamper-Proof Vote Storage**: Custom SHA-256 blockchain with Proof-of-Work (difficulty=3) ensures vote immutability.
- **Double Voting Prevention**: MongoDB voter flags and blockchain checks enforce one-vote-per-user.
- **Real-Time Results**: Candidate dashboard displays live vote counts and historical trends.
- **User-Friendly Interface**: Mobile-responsive frontend built with HTML5, Tailwind CSS, and JavaScript.
- **Auditability**: Public blockchain explorer for transparent vote verification.

## Technologies Used

- **Backend**: Python Flask
- **Database**: MongoDB (collections for voters, candidates, blocks)
- **Blockchain**: Custom SHA-256 with Proof-of-Work
- **Frontend**: HTML5, Tailwind CSS, JavaScript
- **Security**: SHA-256 hashing, CSRF protection
- **Development Environment**: Python 3.8+, MongoDB Community Edition

## Prerequisites

Before setting up the project, ensure you have the following installed:

- Python 3.8 or higher
- MongoDB Community Edition
- A web browser (e.g., Chrome, Firefox)

Hardware requirements:
- PC with 4GB RAM, 2GHz processor, and 256GB storage

## Setup Instructions

1. **Clone the Repository**:
   ```bash
   git clone https://github.com/MehtabAli093/Blockchain_VotingSystem.git
   cd Blockchain_VotingSystem
   ```

2. **Create a Virtual Environment**:
   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```

3. **Install Dependencies**:
   ```bash
   pip install -r requirements.txt
   ```

   Example `requirements.txt`:
   ```
   flask==2.0.1
   pymongo==4.3.3
   ```

4. **Configure MongoDB**:
   - Install and start MongoDB locally or use a cloud instance (e.g., MongoDB Atlas).
   - Update the MongoDB connection string in the application configuration (e.g., in `config.py` or environment variables).

5. **Run the Application**:
   ```bash
   python app.py
   ```
   - Access the application at `http://localhost:5000` in your browser.

## Usage

1. **Voter Registration**:
   - Navigate to the registration page to create a voter account with secure credentials.

2. **Login and Vote**:
   - Log in with your credentials.
   - Cast your vote, which triggers block mining and addition to the blockchain.

3. **View Results**:
   - Access the candidate dashboard to view live vote counts and historical trends.
   - Use the blockchain explorer to verify vote integrity.

4. **Database Management**:
   - MongoDB stores voter data, candidate information, and blockchain blocks.
   - Use a MongoDB client (e.g., MongoDB Compass) to inspect the database.
## Contact

For questions or support, contact:
- Mehtab Ahmed
- mehtabahmed093@gmail.com
*Developed for the Department of Cyber Security, FAST NUCES, May 2025.*
