from flask import Blueprint, request, jsonify
from models import db, Client, Program

api = Blueprint('api', __name__)

@api.route('/programs', methods=['GET'])
def get_programs():
    programs = Program.query.all()
    result = [{'id': p.id, 'name': p.name} for p in programs]
    return jsonify(result)

@api.route('/programs', methods=['POST'])
def create_program():
    name = request.json.get('name')
    if not name:
        return jsonify({'error': 'Program name is required'}), 400
    program = Program(name=name)
    db.session.add(program)
    db.session.commit()
    return jsonify({'message': 'Program created', 'id': program.id}), 201

@api.route('/clients', methods=['POST'])
def register_client():
    data = request.json
    client = Client(
        name=data.get('name'),
        age=data.get('age'),
        gender=data.get('gender'),
        contact=data.get('contact')
    )
    db.session.add(client)
    db.session.commit()
    return jsonify({'message': 'Client registered'}), 201

@api.route('/clients/<client_id>/enroll', methods=['PUT'])
def enroll_client(client_id):
    programs = request.json.get('programs', [])
    client = Client.query.get(client_id)
    if not client:
        return jsonify({'error': 'Client not found'}), 404
    
    # First, find all program objects from the provided program names
    program_objects = []
    for program_name in programs:
        program = Program.query.filter_by(name=program_name).first()
        if program:
            program_objects.append(program)
        else:
            # Create the program if it doesn't exist
            new_program = Program(name=program_name)
            db.session.add(new_program)
            program_objects.append(new_program)
    
    # Update the client's programs
    client.programs = program_objects
    db.session.commit()
    
    return jsonify({'message': 'Client enrolled in programs'}), 200

@api.route('/clients', methods=['GET'])
def search_clients():
    search = request.args.get('search', '')
    clients = Client.query.filter(Client.name.ilike(f'%{search}%')).all()
    result = [
        {'id': c.id, 'name': c.name, 'age': c.age, 'gender': c.gender, 'contact': c.contact}
        for c in clients
    ]
    return jsonify(result)

@api.route('/clients/<client_id>', methods=['GET'])
def get_client(client_id):
    client = Client.query.get(client_id)
    if not client:
        return jsonify({'error': 'Client not found'}), 404
    return jsonify({
        'id': client.id,
        'name': client.name,
        'age': client.age,
        'gender': client.gender,
        'contact': client.contact,
        'programs': [p.name for p in client.programs]
    })