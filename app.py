import time

from flask import Flask, render_template, request, redirect, url_for, session, flash
from flask_wtf import CSRFProtect

from models import User, Voter, Candidate
from blockchain import Blockchain, blocks_collection  # Import blocks_collection
from datetime import datetime
import hashlib

app = Flask(__name__)
app.secret_key = 'ProDark16093333$$$'
# csrf = CSRFProtect(app)
app.config['TEMPLATES_AUTO_RELOAD'] = True

blockchain = Blockchain()
blockchain = Blockchain(difficulty=3)  # Initialize with PoW difficulty

# Helper functions
def get_candidates():
    return Candidate.collection.find({}, {'password': 0})

def get_voter(username):
    return Voter.collection.find_one({'username': username}, {'password': 0})


# Routes
@app.route('/')
def index():
    return render_template('index.html')


@app.route('/login', methods=['GET'])
def login():
    if 'username' in session:
        if session['role'] == 'voter':
            return redirect(url_for('voter_dashboard'))
        else:
            return redirect(url_for('candidate_dashboard'))
    return render_template('login.html')


@app.route('/handle_login', methods=['POST'])
def handle_login():
    username = request.form.get('username')
    password = request.form.get('password')
    role = request.form.get('role')

    if role == 'voter':
        voter = User.verify_voter(username, password)
        if voter:
            session['username'] = username
            session['role'] = 'voter'
            return redirect(url_for('voter_dashboard'))
    elif role == 'candidate':
        candidate = User.verify_candidate(username, password)
        if candidate:
            session['username'] = username
            session['role'] = 'candidate'
            return redirect(url_for('candidate_dashboard'))

    flash('Invalid credentials or role', 'danger')
    return redirect(url_for('login'))


@app.route('/register', methods=['GET'])
def register():
    return render_template('register.html')


@app.route('/handle_register', methods=['POST'])
def handle_register():
    username = request.form.get('username')
    password = request.form.get('password')
    full_name = request.form.get('full_name')
    role = request.form.get('role')
    party = request.form.get('party')

    if role == 'voter':
        success, message = Voter.register(username, password, full_name)
    elif role == 'candidate':
        if not party:
            flash('Party is required for candidates', 'danger')
            return redirect(url_for('register'))
        success, message = Candidate.register(username, password, full_name, party)

    if success:
        flash(message, 'success')
        return redirect(url_for('login'))
    else:
        flash(message, 'danger')
        return redirect(url_for('register'))


@app.route('/voter/dashboard')
def voter_dashboard():
    if 'username' not in session or session['role'] != 'voter':
        return redirect(url_for('login'))

    voter = Voter.collection.find_one(
        {'username': session['username']},
        {'password': 0}
    )

    if not voter:
        flash('Voter not found', 'danger')
        return redirect(url_for('login'))

    return render_template('voter/dashboard.html',
                           voter_has_voted=voter['has_voted'],
                           candidates_count=Candidate.collection.count_documents({}),
                           total_votes=blockchain.chain[-1].index if blockchain.chain else 0)


@app.route('/vote')
def vote_page():
    if 'username' not in session or session['role'] != 'voter':
        return redirect(url_for('login'))

    voter = get_voter(session['username'])
    if voter['has_voted']:
        return redirect(url_for('voter_dashboard'))

    return render_template('voter/vote.html',
                           candidates=get_candidates(),
                           voter_has_voted=False)


@app.route('/submit_vote', methods=['POST'])
def submit_vote():
    if 'username' not in session or session['role'] != 'voter':
        return redirect(url_for('login'))

    voter_username = session['username']
    if Voter.has_voted(voter_username):
        flash('You have already voted', 'warning')
        return redirect(url_for('voter_dashboard'))

    candidate_username = request.form.get('candidate_username')
    candidate = Candidate.collection.find_one({'username': candidate_username})
    if not candidate:
        flash('Candidate not found', 'danger')
        return redirect(url_for('vote_page'))

    # Prepare vote data
    vote_data = {
        'voter': voter_username,
        'candidate': candidate_username,
        'timestamp': str(datetime.utcnow())
    }

    # Mine the block (this will take a few seconds due to PoW)
    start_time = time.time()
    blockchain.add_block(vote_data)
    mining_time = round(time.time() - start_time, 2)

    # Update voter and candidate records
    Voter.collection.update_one(
        {'username': voter_username},
        {'$set': {'has_voted': True}}
    )
    Candidate.increment_vote_count(candidate_username)

    flash(f'Vote mined in {mining_time}s! Transaction added to blockchain.', 'success')
    return redirect(url_for('voter_dashboard'))


@app.route('/candidate/dashboard')
def candidate_dashboard():
    if 'username' not in session or session['role'] != 'candidate':
        return redirect(url_for('login'))

    candidate = Candidate.collection.find_one({'username': session['username']})
    total_candidates = Candidate.collection.count_documents({})

    # Simple rank calculation (for demo purposes)
    candidates_by_votes = list(Candidate.collection.find().sort('votes_received', -1))
    rank = next((i + 1 for i, c in enumerate(candidates_by_votes)
                 if c['username'] == session['username']), 0)

    return render_template('candidate/dashboard.html',
                           candidate=candidate,
                           rank=rank,
                           total_candidates=total_candidates)


@app.route('/candidate/results')
def candidate_results():
    if 'username' not in session or session['role'] != 'candidate':
        return redirect(url_for('login'))

    candidate = Candidate.collection.find_one({'username': session['username']})
    all_blocks = blockchain.get_all_blocks()

    # Filter votes for this candidate and group by date
    votes_by_date = {}
    for block in all_blocks[1:]:  # Skip genesis block
        if block['data'].get('candidate') == session['username']:
            # Convert datetime to date string (YYYY-MM-DD format)
            if isinstance(block['timestamp'], str):
                # If timestamp is already a string
                vote_date = block['timestamp'][:10]
            else:
                # If timestamp is datetime object
                vote_date = block['timestamp'].strftime('%Y-%m-%d')
            votes_by_date[vote_date] = votes_by_date.get(vote_date, 0) + 1

    # Convert to timeline format
    votes_timeline = [{'date': date, 'votes': count}
                      for date, count in votes_by_date.items()]

    total_votes = blocks_collection.count_documents({}) - 1  # Subtract genesis block

    # Calculate vote percentage
    vote_percentage = round((candidate['votes_received'] / total_votes) * 100, 2) if total_votes > 0 else 0

    return render_template('candidate/results.html',
                           candidate=candidate,
                           vote_percentage=vote_percentage,
                           votes_timeline=votes_timeline)


@app.route('/blocks')
def view_blocks():
    chain = blockchain.get_all_blocks()
    return render_template('blocks.html',
                           chain=chain,
                           chain_length=len(chain))


@app.route('/logout')
def logout():
    session.clear()
    flash('You have been logged out', 'success')
    return redirect(url_for('index'))


if __name__ == '__main__':
    app.run(debug=True, port=5000)