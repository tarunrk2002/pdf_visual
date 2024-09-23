from flask import Flask, request, jsonify

app = Flask(__name__)

@app.route('/post-data', methods=['POST'])
def handle_post():
    
    data = request.get_json()  
    
    if not data:
        return jsonify({"error": "No data provided"}), 400
    
    
    print(f"Received data: {data}")
    
    
    name = data.get('name')
    age = data.get('age')
    
    
    return jsonify({"message": f"Received name: {name}, age: {age}"}), 200
app.run(debug=True)