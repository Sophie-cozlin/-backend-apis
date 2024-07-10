from flask import Flask, jsonify
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.exc import SQLAlchemyError

app = Flask(__name__)

# Step 4: Configure the PostgreSQL Database Connection
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://postgres:cozlin@localhost:5432/postgres'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)

# Step 5: Create 
class Pesalink(db.Model):
    __tablename__ = 'pesalink'
    id = db.Column(db.Integer, primary_key=True)
    status = db.Column(db.String(50), nullable=False)

# Create a Route to Fetch Total Count of All Statuses
@app.route('/total_status_count', methods=['GET'])
def get_total_status_count():
    try:
        total_count = Pesalink.query.count()
        return jsonify({"total_status_count": total_count})
    except SQLAlchemyError as e:
        return jsonify({"error": str(e)}), 500
    
    # Endpoint to Fetch Count of Successful ('accp') and Failed ('rjct') Statuses
@app.route('/status_counts', methods=['GET'])
def get_status_counts():
    try:
        successful_count = Pesalink.query.filter_by(status='ACCP').count()
        failed_count = Pesalink.query.filter_by(status='RJCT').count()

        return jsonify({
            "successful_count": successful_count,
            "failed_count": failed_count
        })
    except SQLAlchemyError as e:
        return jsonify({"error": str(e)}), 500
    
if __name__ == '__main__':
    app.run(debug=True)
