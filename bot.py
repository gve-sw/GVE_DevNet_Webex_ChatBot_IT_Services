"""
Copyright (c) 2021 Cisco and/or its affiliates.
This software is licensed to you under the terms of the Cisco Sample
Code License, Version 1.1 (the "License"). You may obtain a copy of the
License at
               https://developer.cisco.com/docs/licenses
All use of the material herein must be in accordance with the terms of
the License. All rights not expressly granted by the License are
reserved. Unless required by applicable law or agreed to separately in
writing, software distributed under the License is distributed on an "AS
IS" BASIS, WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express
or implied.
"""

from flask import Flask, request, jsonify
from webexteamssdk import WebexTeamsAPI
import os
import json

# Get environment variables
WT_BOT_TOKEN = os.environ['WT_BOT_TOKEN']
WT_BOT_EMAIL = os.environ['WT_BOT_EMAIL']

# Start Flask and WT connection
app = Flask(__name__)
api = WebexTeamsAPI(access_token=WT_BOT_TOKEN)


# Getting an initial message, triggering the webhook for: Messages:created
@app.route('/', methods=['POST'])
def initial_message_received():
    raw_json = request.get_json()
    print(raw_json)

    # Customize the behaviour of the bot here
    w_room_id = raw_json['data']['roomId']
    msg_from = raw_json['data']['personEmail']
    print('Message from: ' + msg_from)

    if msg_from != WT_BOT_EMAIL:
        message = "Hi, I'm a Webex bot! I'm here to assist you with IT services.. 💻⚠ "
        api.messages.create(roomId=w_room_id, markdown=message)
        send_card(w_room_id, '000_init_card.json')

    return jsonify({'success': True})

# Getting an attachment action, triggering the webhook for: attachmentActions:created
@app.route('/attachment_action', methods=['POST'])
def attachment_action_received():
    raw_json = request.get_json()
    print(raw_json)

    service_summary = {}
    last_step = False

    # Customize the behaviour of the attachment action here

    # Getting Room and Msg information
    w_room_id = raw_json['data']['roomId']
    w_msg_id = raw_json['data']['messageId']

    # Deleting the original message since a response has been recieved
    api.messages.delete(w_msg_id)

    # Calling Webex API to get the attachment_action by id
    attach_action = api.attachment_actions.get(raw_json['data']['id'])

    # Checking if the recieved card is an action
    if('action' in attach_action.inputs):
        action = attach_action.inputs['action']

        # Handling cards' action buttons
        # 00-Initial Card responses:
        if action == 'request':
            send_card(w_room_id, '010_request.json')
        elif action == 'issue':
            send_card(w_room_id, '020_issue.json')

        # 01-Request Card responses:
        elif action == 'request-software':
            send_card(w_room_id, '011_request-software.json')
        elif action == 'request-hardware':
            send_card(w_room_id, '012_request-hardware.json')
        elif action == 'request-access':
            send_card(w_room_id, '013_request-access.json')
        elif action == 'request-accessories':
            send_card(w_room_id, '014_request-accessories.json')

        # 02- Completed Request handling:
        elif 'request-' in action:
            request_type = action.replace('request-', '')
            message = 'Your request for: ' + request_type + ' ...'
            api.messages.create(roomId=w_room_id, markdown=message)
            send_card(w_room_id, '0300_provide_information.json')

        # 02- Issue 'Computer, Printer, Software' handling:
        elif action == 'issue-computer-pc':
            send_card(w_room_id, '0211_issue-computer-pc.json')
        elif action == 'issue-computer-printing':
            send_card(w_room_id, '0212_issue-computer-printing.json')
        elif action == 'issue-computer-software':
            send_card(w_room_id, '0213_issue-computer-software.json')

        # 02- Issue 'Oracle / E-Business & Kronos' handling:
        elif action == 'issue-oracle-employee':
            send_card(w_room_id, '0221_issue-oracle-employee.json')
        elif action == 'issue-oracle-iperform':
            send_card(w_room_id, '0222_issue-oracle-iperform.json')
        elif action == 'issue-oracle-kronos':
            send_card(w_room_id, '0223_issue-oracle-kronos.json')

        # 02- Issue 'Network services' handling:
        elif action == 'issue-network-remote':
            send_card(w_room_id, '0231_issue-network-remote.json')
        elif action == 'issue-network-internet':
            send_card(w_room_id, '0232_issue-network-internet.json')
        elif action == 'issue-network-wifi':
            send_card(w_room_id, '0233_issue-network-wifi.json')

        # 02- Issue 'Portal, Website, Sharepoint, SMS' handling:
        elif action == 'issue-portal-policy':
            send_card(w_room_id, '0241_issue-portal-policy.json')
        elif action == 'issue-portal-website':
            send_card(w_room_id, '0242_issue-portal-website.json')
        elif action == 'issue-portal-intranet':
            send_card(w_room_id, '0243_issue-portal-intranet.json')
        elif action == 'issue-portal-sms':
            send_card(w_room_id, '0244_issue-portal-sms.json')

        # 03- Completed Issue handling:
        elif 'issue-' in action:
            issue = action.replace('issue-', '')
            last_step = True
            service_summary['issue'] = issue
            message = "Your report for *issue*: **" + issue + "** .." + \
                "\nPlease login to the System and report an incedent by selecting the category of your issue"
            api.messages.create(roomId=w_room_id, markdown=message)

        # Responding to unhandled responses:
        else:
            message = "Your response: '" + action + \
                "' was not recognized. Please try again.."
            api.messages.create(roomId=w_room_id, markdown=message)

    # Checking if the recieved card has userdata
    if('userdata-location' in attach_action.inputs):
        last_step = True
        service_summary['location'] = attach_action.inputs['userdata-location']
    if('userdata-email' in attach_action.inputs):
        last_step = True
        service_summary['email'] = attach_action.inputs['userdata-email']
    if('userdata-phone' in attach_action.inputs):
        last_step = True
        service_summary['phone'] = attach_action.inputs['userdata-phone']
    if('userdata-computer' in attach_action.inputs):
        last_step = True
        service_summary['computer'] = attach_action.inputs['userdata-computer']
    if('userdata-shared_folder_name' in attach_action.inputs):
        last_step = True
        service_summary['shared_folder_name'] = attach_action.inputs['userdata-shared_folder_name']
    if('userdata-shared_folder_path' in attach_action.inputs):
        last_step = True
        service_summary['shared_folder_path'] = attach_action.inputs['userdata-shared_folder_path']
    if('userdata-comments' in attach_action.inputs):
        last_step = True
        service_summary['comments'] = attach_action.inputs['userdata-comments']

    # If the card recieved is doesn't have actions or userdataa
    if(attach_action.inputs is None):
        message = 'No actions/inputs were detected. Please try again or contact support'
        api.messages.create(roomId=w_room_id, markdown=message)

    # Displaying the summary to the user
    if(last_step):
        message = '\nRequest summary:\n'
        for key in service_summary.keys():
            if service_summary[key] != '':
                message += '    - ' + key + ': ' + service_summary[key] + '\n'
        api.messages.create(roomId=w_room_id, markdown=message)

    return jsonify({'success': True})

# Getting adaptive card data from the local file
def get_json_card(filepath):
    """
    Get content of JSON card
    """
    with open('cards/'+filepath, 'r') as f:
        json_card = json.loads(f.read())
        f.close()
    return json_card

# Sending an Adaptive card message to Webex room
def send_card(room_id, card_file):
    api.messages.create(
        roomId=room_id,
        text="Card Message: If you see this your client cannot render cards",
        attachments=[{
            "contentType": "application/vnd.microsoft.card.adaptive",
            "content": get_json_card(card_file)
        }],
    )


if __name__ == "__main__":
    app.run()
