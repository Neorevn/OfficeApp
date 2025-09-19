from flask import Blueprint, request, jsonify
import logging
from bson import json_util
import json

from database import db
from auth import admin_required

automation_bp = Blueprint('automation_bp', __name__)

# Checks for admin role
def is_admin():
    return request.headers.get('X-User-Role') == 'admin'

# Checks for user role, If user role == True then user will have view only permission
def auth_required(role='any'):
    user_role = request.headers.get('X-User-Role')
    if not user_role or (role == 'admin' and user_role != 'admin'):
        return False
    return True

@automation_bp.route('/api/automation/rules/create', methods=['POST'])
@admin_required
def create_automation_rule():
    if not is_admin():
        return jsonify({'error': 'Administrator access required'}), 403   
    data = request.get_json()
    if not data or 'trigger' not in data or 'action' not in data:
        return jsonify({'error': 'Missing trigger or action in request body'}), 400
    
    # Generate a new sequential ID for new rule
    last_rule = db.automation_rules.find_one(sort=[("id", -1)])
    new_id = (last_rule["id"] + 1) if last_rule else 1

    new_rule = {
        'id': new_id,
        'trigger': data['trigger'], # e.g., {'type': 'user_login', 'condition': {'username': 'user1'}}
        'action': data['action'],   # e.g., {'type': 'hvac_off'}
        'active': True,
        'description': data.get('description', 'Custom rule')
    }

    # Validate structure
    if 'type' not in new_rule['trigger'] or 'type' not in new_rule['action']:
        return jsonify({'error': 'Invalid rule structure. Trigger and action must have a type.'}), 400

    db.automation_rules.insert_one(new_rule)
    logging.info(f"Automation: Created new rule: {new_rule}")
    return json.loads(json_util.dumps(new_rule)), 201
    new_rule.pop('_id', None)
    return jsonify(new_rule), 201

@automation_bp.route('/api/automation/rules', methods=['GET'])
def get_all_rules():
    rules = list(db.automation_rules.find({}, {'_id': 0}))
    return jsonify(rules)

@automation_bp.route('/api/automation/rules/toggle/<int:rule_id>', methods=['POST'])
@admin_required
def toggle_rule(rule_id):
    if not is_admin():
        return jsonify({'error': 'Administrator access required'}), 403
    rule = db.automation_rules.find_one({'id': rule_id})
    if not rule:
        return jsonify({'error': 'Rule not found'}), 404
    new_active_state = not rule.get('active', False)
    db.automation_rules.update_one(
        {'_id': rule['_id']},
        {'$set': {'active': new_active_state}}
    )
    logging.info(f"Automation: Toggled rule {rule_id} to {'active' if new_active_state else 'inactive'}.")
    rule['active'] = new_active_state
    return json.loads(json_util.dumps(rule))
    rule.pop('_id', None)
    return jsonify(rule)

@automation_bp.route('/api/automation/rules/delete/<int:rule_id>', methods=['DELETE'])
@admin_required
def delete_rule(rule_id):
    if not is_admin():
        return jsonify({'error': 'Administrator access required'}), 403
    
    result = db.automation_rules.delete_one({'id': rule_id})
    
    if result.deleted_count == 0:
        return jsonify({'error': 'Rule not found'}), 404
        
    logging.info(f"Automation: Rule {rule_id} was deleted by an admin.")
    return jsonify({'status': 'success', 'message': f"Rule #{rule_id} has been deleted."})


@automation_bp.route('/api/automation/scenes/create', methods=['POST'])
@admin_required
def create_environmental_scene():
    if not is_admin():
        return jsonify({'error': 'Administrator access required'}), 403
    data = request.get_json()
    if not data or 'name' not in data or 'settings' not in data:
        return jsonify({'error': 'Missing name or settings for the scene'}), 400
    scene_name = data['name']
    if db.scenes.find_one({'_id': scene_name}):
        return jsonify({'error': f"Scene '{scene_name}' already exists."}), 409
    db.scenes.update_one({'_id': scene_name}, {'$set': {'settings': data['settings']}}, upsert=True)
    logging.info(f"Automation: Created new scene '{scene_name}' with settings: {data['settings']}")
    return jsonify({'status': 'success', 'scene_name': scene_name, 'settings': data['settings']}), 201

def process_event(event_type, event_data={}):
    logging.info(f"Automation: Processing event '{event_type}' with data: {event_data}")
    matching_rules = db.automation_rules.find({
        'trigger.type': event_type,
        'active': True
    })

    triggered_count = 0
    for rule in matching_rules:
        conditions = rule.get('trigger', {}).get('condition', {})
        is_match = True
        # Check if all conditions in the rule are met by the event data
        for key, value in conditions.items():
            event_value = event_data.get(key)
            # Robust comparison to handle type mismatches (e.g., '14' vs 14)
            if event_value is None:
                is_match = False
                break
            try:
                # Attempt to compare values of the same type
                if type(event_value)(value) != event_value:
                    is_match = False
                    break
            except (ValueError, TypeError):
                is_match = False
                break
        if is_match:
            action_type = rule.get('action', {}).get('type')
            if action_type:
                source_description = f"rule #{rule['id']} ('{rule['description']}')"
                _execute_automation_action(action_type, source_description)
                triggered_count += 1
    
    if triggered_count > 0:
        logging.info(f"Automation: Event '{event_type}' triggered {triggered_count} rule(s).")


# Actual rules
def _execute_automation_action(action, source_description):
    logging.info(f"Automation: {source_description} triggered action: '{action}'.")
    if action == 'lights_on':
        db.state.update_one({'_id': 'office'}, {'$set': {'lights_on': True}})
        logging.info("Automation: Lights turned ON by rule.")
    elif action == 'lights_off':
        db.state.update_one({'_id': 'office'}, {'$set': {'lights_on': False}})
        logging.info("Automation: Lights turned OFF by rule.")
    elif action == 'hvac_off':
        db.state.update_one({'_id': 'office'}, {'$set': {'hvac_mode': 'off'}})
        logging.info("Automation: HVAC turned OFF by rule.")
    else:
        logging.warning(f"Automation: Unknown action '{action}' requested by {source_description}.")
        return False 
    return True

@automation_bp.route('/api/automation/triggers/motion', methods=['POST'])
def trigger_motion():
    data = request.get_json()
    area = data.get('area', 'general') if data else 'general'    
    process_event('motion', {'area': area})
    return jsonify({'message': f"Motion event in '{area}' processed."}), 200

@automation_bp.route('/api/automation/rules/test/<int:rule_id>', methods=['POST'])
@admin_required
def test_rule(rule_id):
    if not is_admin():
        return jsonify({'error': 'Administrator access required'}), 403
    rule = db.automation_rules.find_one({'id': rule_id})
    if not rule:
        return jsonify({'error': 'Rule not found'}), 404
    if not rule.get('active', True):
        return jsonify({'message': f"Rule {rule_id} is inactive. Test not run."}), 200
    action = rule.get('action', {}).get('type')
    source_description = f"Test for rule #{rule_id}"
    _execute_automation_action(action, source_description)
    return jsonify({'message': f"Test triggered for rule #{rule_id}. Action '{action}' executed."}), 200

@automation_bp.route('/api/automation/energy-savings', methods=['GET'])
def get_energy_savings():
    # In a real app, this would be calculated. For now, we'll just return the placeholder.
    energy_savings = db.energy_savings.find_one({'_id': 'office'})
    if not energy_savings:
        db.energy_savings.insert_one({'_id': 'office', 'hvac_runtime_reduced_hours': 0, 'lights_off_hours': 0})
        energy_savings = db.energy_savings.find_one({'_id': 'office'})

    logging.info("Automation: Energy savings data requested.")
    return json.loads(json_util.dumps(energy_savings))
    energy_savings.pop('_id', None)
    return jsonify(energy_savings)