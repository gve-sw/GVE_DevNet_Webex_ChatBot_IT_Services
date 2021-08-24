# GVE_DevNet_Webex_ChatBot_IT_Services
This is a sample Webex Chatbot showing how requesting IT services (Software, Hardware, Access, etc..) can be simplified and automated. Allowing the user to respond with button clicks, selecting from a list, filling a field, etc.. using Adaptive Cards.


## Contacts
* Rami Alfadel (ralfadel@cisco.com)


## Solution Components
* Webex Bot
* Adaptive Cards
* Python 
* Flask


## Solution Overview
This prototype is showing a sample Webex Chatbot that responds to messages by displaying list of options as: buttons, drop-down lists, fields to fill, etc.. The scenario for this speicific bot is following a general use case of opening a ticket requesting IT Services/support. 

This chatbot sample is running and can be tested by sending a message in Webex to:  
```IT-services@webex.bot```

A sample overview of the services to be requested is shown as follows:
![/IMAGES/Overview_1.png](/IMAGES/Overview_1.png)

So when a user initiates a message with this chatbot, the first response will be as follows:
![/IMAGES/Initial_msg.png](/IMAGES/Initial_msg.png)

- When the user selects "Submit a new request" button for example, the next card with its list of choices will be shown:  
![/IMAGES/New_request_ac.png](/IMAGES/New_request_ac.png)

- As the user selects the next choice (for example: Hardware request), the next customized card will be displayed, and so on:
![/IMAGES/New_request_hardware_ac.png](/IMAGES/New_request_hardware_ac.png)

- In the final prompt, the user will be asked to input the details needed, which also can be customized as well:  
![/IMAGES/Filling_info_sample.png](/IMAGES/Filling_info_sample.png)

- After the data is collected, the next action for the collected data can be customized as well. For example: sending it to the IT team via email, storing it in a file/db, opening a ticket through ticketing system's APIs, etc..  
![/IMAGES/Request_summary.png](/IMAGES/Request_summary.png)

## Installation

This Webex Chatbot prototype has been developed and deployed on [Heroku](https://www.heroku.com/) following the instructions detailed here:
https://github.com/gve-sw/WebexBot_HerokuDeployment  
- Where [bot.py](/bot.py) file has been developed in this reposetory, with [cards](/cards) folder containing customized [adaptive card](https://adaptivecards.io/) as bot responses.  
- After the application is hosted on an accessible URL, two webhooks must be created by the bot's API key, using [Webex Webhooks APIs](https://developer.webex.com/docs/api/v1/webhooks/)
    1. To detect recieiving new "messages" (which are text messages)
        - By [creating a new webhook](https://developer.webex.com/docs/api/v1/webhooks/create-a-webhook) with:
            -   resource: ```messages```
            -   event: ```created```
            -   targetUrl: matching the application's URL, and the default endpoint ```/```
                - Can be changed inside [bot.py](/bot.py)
                ```python
                # Getting an initial message, triggering the webhook for: Messages:created
                @app.route('/', methods=['POST'])
                ```
    2. To detect recieiving new "attachmentActions" (which are adaptive cards messages)
        - By [creating a new webhook](https://developer.webex.com/docs/api/v1/webhooks/create-a-webhook) with:
            -   resource: ```attachmentActions```
            -   event: ```created```
            -   targetUrl: matching the application's URL, and the endpoint for receiving attachment actions ```/attachment_action``` 
                - Can be changed inside [bot.py](/bot.py)
                ```python
                # Getting an attachment action, triggering the webhook for: attachmentActions:created
                @app.route('/attachment_action', methods=['POST'])
                ```


## Configuration/Customization

To customize the chatbot's response messages, adaptive cards used, or actions taken, changes must be done in either:
- [bot.py](/bot.py):
    - To change what actions are taken when a new message has been recieved.  
    For example, to change the initial response to any text message, edit the lines of code inside ```initial_message_received``` function:
    ```python
    message = "Hi, I'm a Webex bot! I'm here to assist you with IT services.. 💻⚠ "
    api.messages.create(roomId=w_room_id, markdown=message)
    send_card(w_room_id, '000_init_card.json')
    ```

- [cards](/cards) Folder:
    - To change how the adaptive cards look and what buttons/actions do they include.  
    For example, to customize what the initial adaptive card includes, edit [000_init_card.json](/cards/000_init_card.json) file:
    ```json
    ...
    "actions": [
        {
            "type": "Action.Submit",
            "title": "Submit a new request",
            "style": "positive",
            "data": {
                "action": "request"
            }
        },
        {
            "type": "Action.Submit",
            "title": "Report an issue",
            "style": "destructive",
            "data": {
                "action": "issue"
            }
        }
    ],
    ...
    ```
- Notice that each button/action of this adaptive card has a ```data``` element, which includes any inputs to be sent to the application's side (e.g: ```"action": "issue"```). This is to determine what has the user selected, and customize what the next action will be.
    - For example, handling the initial card buttons:  
    ```python
    # 00-Initial Card responses:
    if action == 'request':
        send_card(w_room_id, '010_request.json')
    elif action == 'issue':
        send_card(w_room_id, '020_issue.json')
    ```

## Notes

- To get started with Webex ChatBot and learn how to host it on a local server: https://developer.webex.com/blog/from-zero-to-webex-teams-chatbot-in-15-minutes

- To easily build a customized adaptive card, you can use:
    - Webex Buttons adn Cards Designer: https://developer.webex.com/buttons-and-cards-designer
    - More Adaptive Cards specifications can be found on Schema Browser: https://adaptivecards.io/explorer/


### LICENSE

Provided under Cisco Sample Code License, for details see [LICENSE](LICENSE.md)

### CODE_OF_CONDUCT

Our code of conduct is available [here](CODE_OF_CONDUCT.md)

### CONTRIBUTING

See our contributing guidelines [here](CONTRIBUTING.md)

#### DISCLAIMER:
<b>Please note:</b> This script is meant for demo purposes only. All tools/ scripts in this repo are released for use "AS IS" without any warranties of any kind, including, but not limited to their installation, use, or performance. Any use of these scripts and tools is at your own risk. There is no guarantee that they have been through thorough testing in a comparable environment and we are not responsible for any damage or data loss incurred with their use.
You are responsible for reviewing and testing any scripts you run thoroughly before use in any non-testing environment.