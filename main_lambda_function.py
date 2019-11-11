# Python 3.7 runtime

import json
import re
import traceback

def lambda_handler(event, context):
    indexHead = """
    <head>
        <title>Create your own virtual assistant in 2 hours</title>
        <meta charset="utf-8">
        <meta content="width=device-width,initial-scale=1,minimal-ui" name="viewport">
        <script async src="https://www.googletagmanager.com/gtag/js?id=UA-147552064-1"></script>
        <script>
            window.dataLayer = window.dataLayer || [];
            function gtag() { dataLayer.push(arguments); }
            gtag('js', new Date());
            gtag('config', 'UA-147552064-1');
        </script>
        <link rel="shortcut icon" href="https://core.telegram.org/favicon.ico?3">
        <link rel="stylesheet" href="https://unpkg.com/vue-material@beta/dist/vue-material.min.css">
        <link rel="stylesheet" href="https://unpkg.com/vue-material@beta/dist/theme/default.css">
        <link rel="stylesheet" href="https://fonts.googleapis.com/css?family=Fira+Code:300,400,500,700&display=swap">
        <link rel="stylesheet" href="https://cdnjs.cloudflare.com/ajax/libs/codemirror/5.32.0/codemirror.min.css" />
    </head>
    """

    indexBody = """
    <body>
        <div>
            <h3 id="logo">OneMoreThing</h3>
            <h1>Create your own virtual assistant in 2 hours</h1>
        </div>
        <div id="app">
            <md-tabs>
                <md-tab v-for="question in questions" :key=question.name v-bind:md-label=question.name+question.status>
                    <doctest-activity v-bind:ui-items=question.uiItem v-bind:question-name=question.name  @questionhandler="toggleQuestionStatus" />
                </md-tab>
            </md-tabs>
        </div>
    </body>
    """

    indexScriptsAfterBody = """
    <script src="https://unpkg.com/vue"></script>
    <script src="https://unpkg.com/vue-material@beta"></script>
    <script src="https://cdnjs.cloudflare.com/ajax/libs/codemirror/5.32.0/codemirror.min.js"></script>
    <script src="https://cdnjs.cloudflare.com/ajax/libs/codemirror/5.48.4/mode/python/python.min.js"></script>
    <script src="https://cdn.jsdelivr.net/npm/vue-codemirror@4.0.6/dist/vue-codemirror.min.js"></script>
    <script>
    Vue.use(VueMaterial.default);
    Vue.use(window.VueCodemirror);
    """

    vueComponent = """
    Vue.component('doctest-activity', {
        props: ['uiItems', 'questionName'],
        data: function () {
            return {
                answer: { jsonFeedback: '', htmlFeedback: '', textFeedback: '', isComplete: false },
                uiItem: this.uiItems,
                cmOptions: {
                    mode: "python",
                    lineNumbers: true,
                    tabSize: 4,
                    scrollbarStyle: "null"
                },
                cmReadOnly: {
                    mode: "python",
                    lineNumbers: true,
                    tabSize: 4,
                    readOnly: true
                }
            }
        },
        methods: {
            postContents: function () {
                // comment: leaving the gatewayUrl empty - API will post back to itself
                var gatewayUrl = '';
                if (this.questionName == 'Step 7') {
                    gatewayUrl = 'https://l96mngjhpc.execute-api.us-east-1.amazonaws.com/default/Create_NewEntry_GoogleSheet';
                } else if (this.questionName == 'Step 8') {
                    gatewayUrl = 'https://hki0p9f7rh.execute-api.us-east-1.amazonaws.com/default/Query_GoogleSheet';
                }
                this.$set(this, 'answer', {jsonFeedback: '',htmlFeedback: '',textFeedback: '', isComplete: false});
                fetch(gatewayUrl, {
                    method: "POST",
                    headers: {
                        'Accept': 'application/json',
                    },
                    body: JSON.stringify({ userToken: "ABCDE", shown: { 0: this.uiItem[0].vModel }, editable: { 0: this.uiItem[1].vModel }, hidden: { 0: "" } })
                }).then(response => {
                    return response.json()
                }).then(data => {
                    this.answer = JSON.parse(JSON.stringify(data))
                    // emit 'questionhandler' to update status of question
                    return this.$emit('questionhandler', { data, questionName: this.questionName })
                })
            }
        },
        template:
            `<div class="md-layout md-gutter">
                <div id="cardGroupCreator" class="md-layout-item md-size-100">
                    <md-card>
                        <md-card-header>
                            <md-card-header-text>
                                <div class="md-title">{{uiItem[2].header}}</div>
                            </md-card-header-text>
                        </md-card-header>
                        <md-card-content>
                            <md-field v-html="uiItem[2].vModel" />
                        </md-card-content>
                    </md-card>
                </div>
                <div id="cardGroupCreator" class="md-layout-item md-size-100">
                    <md-card>
                        <md-card-header>
                            <md-card-header-text>
                                <div class="md-title">{{uiItem[0].header}}</div>
                                <div class="md-subhead">{{uiItem[0].subHeader}}</div>
                            </md-card-header-text>
                        </md-card-header>
                        <md-card-content>
                            <md-field>
                                <codemirror class="editableTextarea" v-model="uiItem[0].vModel" :options="cmReadOnly"></codemirror>
                            </md-field>
                        </md-card-content>
                    </md-card>
                    <md-card>
                        <md-card-header>
                            <md-card-header-text>
                                <div class="md-title">{{uiItem[1].header}}</div>
                                <div class="md-subhead">{{uiItem[1].subHeader}}</div>
                            </md-card-header-text>
                                <md-card-media>
                                    <md-button class="md-raised md-primary" v-on:click="postContents">Submit</md-button>
                                </md-card-media>
                        </md-card-header>
                        <md-card-content>
                            <md-field>
                                <codemirror class="editableTextarea" v-model="uiItem[1].vModel" :options="cmOptions"></codemirror>
                            </md-field>
                        </md-card-content>
                    </md-card>
                </div>
                <div id="cardGroupPreview" class="md-layout-item md-size-100">
                    <md-card>
                        <md-card-header>
                            <md-card-header-text>
                                <div class="md-title">Output</div>
                                <div class="md-subhead">Test results</div>
                            </md-card-header-text>
                        </md-card-header>
                        <md-card-content>
                            <md-field>
                                <md-tabs>
                                    <md-tab id="tab-htmlResults" md-label="HTML results">
                                        <div v-html="answer.htmlFeedback"></div>
                                    </md-tab>
                                    <md-tab id="tab-jsonResults" md-label="JSON results">
                                        <md-textarea v-model="answer.jsonFeedback" readonly></md-textarea>
                                    </md-tab>
                                    <md-tab id="tab-textResults" md-label="Text results">
                                        <md-textarea v-model="answer.textFeedback" readonly></md-textarea>
                                    </md-tab>
                                </md-tabs>
                            </md-field>
                        </md-card-content>
                    </md-card>
                </div>
            </div>
        `
    })
    """

    vueApp = """
    new Vue({
        el: '#app',
        data: function () {
            return {
                questions: [
                    {
                        name: "Step 0", uiItem: [
                            { header: "Tests", subHeader: '', vModel: "assert True" },
                            { header: "Editable Code Block", subHeader: 'Your code goes below', vModel: "# What question do you have after watching this video?\\ndef return_your_question():\\n\\treturn 'YOUR_QUESTION'" },
                            { header: "What You Will Learn in This Path?", vModel: '<div class="videoContainer"><iframe width="560" height="315" src="https://www.youtube.com/embed/7Ivw-KDh_0k" frameborder="0" allow="accelerometer; autoplay; encrypted-media; gyroscope; picture-in-picture" allowfullscreen></iframe></div>' }
                        ], status: " 💬"
                    },
                    {
                        name: "Step 1", uiItem: [
                            { header: "Tests", subHeader: '', vModel: "assert True" },
                            { header: "Editable Code Block", subHeader: 'Your code goes below', vModel: "# Do you have any questions about this activity?\\ndef return_your_question():\\n\\treturn 'YOUR_QUESTION'" },
                            { header: "Introduction to Chatbot", vModel: '<div><h3>What is chatbot and what is it for?</h3><blockquote><p>"A computer program designed to simulate conversation with human users, especially over the Internet."Research has shown that people use chatbot for below purposes:</p><ul><li>Productivity. Chatbots provide the assistance or access to information quickly and efficiently.</li><li>Entertainment. Chatbots amuse people by giving them funny tips, they also help killing time when users have nothing to do.</li><li>Social and relational factors. Chatbots fuel conversions and enhance social experiences. Chatting with bots also helps to avoid loneliness, gives a chance to talk without being judged and improves conversational skills.</li><li>Curiosity. The novelty of chatbots sparks curiosity. People want to explore their abilities and to try something new.</li></ul></blockquote><h3>Why is chatbot important?</h3><blockquote><p>Online chatbots save time and effort by automating customer support. Gartner forecasts that by 2020, over <strong>85%</strong> of customer interactions will be handled without a human. This is critical for the continuous evolving of ecommerce. However, the opportunities provided by chatbot systems go far beyond giving responses to customers\\' inquiries. They are also used for other business tasks, like collecting information about users, helping to organize meetings and reducing overhead costs. There is no wonder that size of the chatbot market is growing exponentially.</p></blockquote></div>' }
                        ], status: " 💬"
                    },
                    {
                        name: "Step 2", uiItem: [
                            { header: "Tests", subHeader: '', vModel: "assert YOUR_TOKEN, 'Test failed. Please enter your api token.'\\n\\nresponse = lambda_handler({}, {})\\nassert response.status_code == 200, 'Test failed. GET response returned with not ok.'\\n\\ndata = response.json()\\nassert data['ok'], \\"Test failed. 'ok' should be True.\\"\\nassert data['result']['is_bot'], \\"Test failed. 'is_bot' should be True.\\"" },
                            { header: "Editable Code Block", subHeader: 'Your code goes below', vModel: "from botocore.vendored import requests\\n\\n# TO DO PART I\\n# YOUR_TOKEN EXAMPLE\\n# YOUR_TOKEN = '123456:ABC-DEF1234ghIkl-zyx57W2v1u123ew11'\\n\\nYOUR_TOKEN = ''\\n\\n# TO DO PART II\\n# Using the 'getMe' method here to get a simple response from the API\\ndef lambda_handler(event, context):\\n\\turl = f'https://api.telegram.org/bot{YOUR_TOKEN}/'\\n\\tresponse = requests.get(url)\\n\\n\\treturn response" },
                            { header: "Get ChatBot Info", vModel: '<div><ol><li><p>Register your Telegram account at <a href="https://web.telegram.org/#/login">https://web.telegram.org/#/login</a></p></li><li><p>Search for BotFather </p></li><li><p>Talk to him (He will show you how to create your first bot and get the token for API)<img alt="image" src="https://drive.google.com/uc?export=view&amp;id=11P2IkO4FSy3QPgX04eWeSAAZlIU5GdHX"></p></li><li><p>Once you get the token, it will be used for the testing in this step. You will also need to understand the getMe method in the API<br>    <strong>getMe</strong>  </p><blockquote><ul><li>A simple method for testing your bot\\'s auth token. Requires no parameters. Returns basic information about the bot in form of a User object.  </li><li>Refer to the detailed manual here: <a href="https://core.telegram.org/bots/api#getme">https://core.telegram.org/bots/api#getme</a></li></ul></blockquote></li><li>Modify the <strong>#TO DO part</strong> in the code to pass the test</li></ol></div>' }
                        ], status: " 💬"
                    },
                    {
                        name: "Step 3", uiItem: [
                            { header: "Tests", subHeader: '', vModel: "assert YOUR_TOKEN, 'Test failed. Please enter your api token.'\\n\\nresponse = lambda_handler({}, {})\\nassert response.status_code == 200, 'Test failed. GET response returned with not ok.'\\n\\ndata = response.json()\\nassert data['ok'], \\"Test failed. 'ok' should be True.\\"\\nassert data['result'][0]['message']['chat']['id'], \\"Test failed. chat id should exist.\\"\\nassert data['result'][0]['message']['text'], \\"Test failed. text should exist.\\"" },
                            { header: "Editable Code Block", subHeader: 'Your code goes below', vModel: "from botocore.vendored import requests\\n\\n# TO DO PART I\\n# YOUR_TOKEN EXAMPLE\\n# YOUR_TOKEN = '123456:ABC-DEF1234ghIkl-zyx57W2v1u123ew11'\\n\\nYOUR_TOKEN = ''\\n\\ndef lambda_handler(event, context):\\n\\t# TO DO PART II\\n\\t# Using the 'getUpdates' method here to check the chat id\\n\\turl = f'https://api.telegram.org/bot{YOUR_TOKEN}/'\\n\\tresponse = requests.get(url)\\n\\n\\treturn response" },
                            { header: "Get Chat ID", vModel: '<div><ol><li>Say Hello to your bot!</li></ol><ul><li>Type "Hello!" to the bot you just created. (This is only requried if you have not chatted with your bot yet, if you have already chatted with your bot you can jump to next step)</li></ul><ol start="2"><li><p>Add in your token into the code block and run it. It should return the chat id for your chat. </p></li><li><p>You will need to understand the getUpdate method in the API.<br><strong>Getting updates</strong></p><blockquote><ul><li>There are two mutually exclusive ways of receiving updates for your bot: the <strong><em>getUpdates</em></strong> method on one hand and <strong><em>Webhooks</em></strong> on the other. Incoming updates are stored on the server until the bot receives them either way, but they will not be kept longer than 24 hours. Regardless of which option you choose, you will receive JSON-serialized Update objects as a result.</li><li>Refer to the offical manual of getUpdates in telegram API documentation if you have any further questions. <a href="https://core.telegram.org/bots/api#getting-updates">https://core.telegram.org/bots/api#getting-updates</a>  </li></ul></blockquote></li><li><p>Please keep the chat ID for upcoming test in Step 4.</p></li><li>Modify the <strong>#TO DO part</strong> in the code to pass the test</li></ol></div>' }
                        ], status: " 💬"
                    },
                    {
                        name: "Step 4", uiItem: [
                            { header: "Tests", subHeader: '', vModel: "assert YOUR_TOKEN, 'Test failed. Please enter your api token.'\\nassert YOUR_CHAT_ID, 'Test failed. Please enter your chat id.'\\n\\nsampleEvent = {\\n\\t\\"body\\": json.dumps({\\n\\t\\t\\"message\\": {\\n\\t\\t\\t\\"chat\\": {\\n\\t\\t\\t\\t\\"id\\": YOUR_CHAT_ID,\\n\\t\\t\\t\\t\\"first_name\\": \\"Test\\",\\n\\t\\t\\t\\t\\"last_name\\": \\"User\\",\\n\\t\\t\\t\\t\\"type\\": \\"private\\"\\n\\t\\t\\t},\\n\\t\\t\\t\\"text\\": \\"Hello My 1st ChatBot!\\"\\n\\t\\t}\\n\\t})\\n}\\n\\nresponse = lambda_handler(sampleEvent, {})\\nassert response.status_code == 200, 'Test failed. GET response returned with not ok.'\\n\\ndata = response.json()\\nassert data['ok'], \\"Test failed. 'ok' should be True.\\"\\nassert str(data['result']['chat']['id']) == YOUR_CHAT_ID, \\"Test failed. chat id should be identical to YOUR_CHAT_ID.\\"\\nassert data['result']['text'] == 'You said: Hello My 1st ChatBot!', \\"Test failed. text seems to be wrong.\\"" },
                            { header: "Editable Code Block", subHeader: 'Your code goes below', vModel: "from botocore.vendored import requests\\n\\n# TO DO PART I\\n# YOUR_TOKEN EXAMPLE\\n# YOUR_TOKEN = '123456:ABC-DEF1234ghIkl-zyx57W2v1u123ew11'\\n# Your_CHAT_ID was obtained fromt the previous step, revist the previous step if you didnt save it\\n\\nYOUR_TOKEN = ''\\nYOUR_CHAT_ID = ''\\n\\ndef send_message(chat_id, text):\\n\\tresponse_text = f'You said: {text}'\\n\\n\\tdata = {\\n\\t\\t\\"chat_id\\": chat_id,\\n\\t\\t\\"text\\": response_text\\n\\t}\\n\\t# TO DO PART II\\n\\t# Using the sendMessage method here to send a message to the bot and get feedback from the bot\\n\\turl = f'https://api.telegram.org/bot{YOUR_TOKEN}/'\\n\\tresponse = requests.post(url=url, data=data)\\n\\n\\treturn response\\n\\ndef lambda_handler(event, context):\\n\\t# TODO implement\\n\\tmessage = json.loads(event['body'])\\n\\tchat_id = message['message']['chat']['id']\\n\\ttext = message['message']['text']\\n\\tresponse = send_message(chat_id, text)\\n\\n\\treturn response" },
                            { header: "Send a message to the bot and the bot will give feedback", vModel: '<div><ol><li>Send a message such as "Hello My 1st ChatBot!" to your bot.  </li><li><p>You will need to understand the sendMessage method in the API.<br> <strong>sendMessage</strong>  </p><blockquote><ul><li>Use this method to send text messages. On success, the sent Message is returned.</li><li>Refer to the official documentation from Telegram API here if needed: <a href="https://core.telegram.org/bots/api#sendmessage">https://core.telegram.org/bots/api#sendmessage</a></li></ul></blockquote></li><li>In our test case here, you will receive a successful response of "You said: Hello My 1st ChatBot!" if everything goes well.</li><li>Remember to get your chat id from "STEP 3 GET CHAT ID" if you didnt save the chat id.  </li><li>Modify the <strong>#TO DO part</strong> in the code to pass the test</li></ol></div>' }
                        ], status: " 💬"
                    },
                    {
                        name: "Step 5", uiItem: [
                            { header: "Tests", subHeader: '', vModel: "assert YOUR_TOKEN, 'Test failed. Please enter your api token.'\\nassert YOUR_CHAT_ID, 'Test failed. Please enter your chat id.'\\n\\nsampleEvent = {\\n\\t\\"body\\": json.dumps({\\n\\t\\t\\"message\\": {\\n\\t\\t\\t\\"chat\\": {\\n\\t\\t\\t\\t\\"id\\": YOUR_CHAT_ID,\\n\\t\\t\\t\\t\\"first_name\\": \\"Test\\",\\n\\t\\t\\t\\t\\"last_name\\": \\"User\\",\\n\\t\\t\\t\\t\\"type\\": \\"private\\"\\n\\t\\t\\t},\\n\\t\\t\\t\\"text\\": \\"/cute\\",\\n\\t\\t\\t\\"entities\\": [\\n\\t\\t\\t\\t{\\n\\t\\t\\t\\t\\t\\"offset\\": 0,\\n\\t\\t\\t\\t\\t\\"length\\": 5,\\n\\t\\t\\t\\t\\t\\"type\\": \\"bot_command\\"\\n\\t\\t\\t\\t}\\n\\t\\t\\t]\\n\\t\\t}\\n\\t})\\n}\\n\\nresponse = lambda_handler(sampleEvent, {})\\nassert response.status_code == 200, 'Test failed. GET response returned with not ok.'\\n\\ndata = response.json()\\nassert data['ok'], \\"Test failed. 'ok' should be True.\\"\\nassert str(data['result']['chat']['id']) == YOUR_CHAT_ID, \\"Test failed. chat id should be identical to YOUR_CHAT_ID.\\"\\nassert data['result']['photo'], \\"Test failed. photo should exist.\\"" },
                            { header: "Editable Code Block", subHeader: 'Your code goes below', vModel: "from botocore.vendored import requests\\n\\n# TO DO part I\\n# YOUR_TOKEN EXAMPLE\\n# YOUR_TOKEN = '123456:ABC-DEF1234ghIkl-zyx57W2v1u123ew11'\\n# Your_CHAT_ID was obtained fromt the step 3, revist the previous steps if you didnt save it\\n\\nYOUR_TOKEN = ''\\nYOUR_CHAT_ID = ''\\n\\ndef get_url():\\n\\tcontents = requests.get('https://random.dog/woof.json').json()\\n\\turl = contents['url']\\n\\treturn url\\n\\n# Use regex to filter out those 3 types of pictures ('jpg','jpeg','png') only\\ndef get_image_url():\\n\\tallowed_extension = ['jpg','jpeg','png']\\n\\tfile_extension = ''\\n\\n\\twhile file_extension not in allowed_extension:\\n\\t\\turl = get_url()\\n\\t\\tfile_extension = re.search(\\"([^.]*)$\\",url).group(1).lower()\\n\\n\\treturn url\\n\\ndef send_photo(chat_id):\\n\\tdata = {\\n\\t\\t\\"chat_id\\": chat_id,\\n\\t\\t\\"photo\\": get_image_url()\\n\\t}\\n\\t# TO DO part II\\n\\t# Using the sendPhoto method here to send the photo recieved from the public API to the chat\\n\\turl = f'https://api.telegram.org/bot{YOUR_TOKEN}/'\\n\\tresponse = requests.post(url=url, data=data)\\n\\n\\treturn response\\n\\ndef lambda_handler(event, context):\\n\\tmessage = json.loads(event['body'])\\n\\tchat_id = message['message']['chat']['id']\\n\\ttext = message['message']['text']\\n\\tentity_type = message['message']['entities'][0]['type']\\n\\n\\tif entity_type == 'bot_command':\\n\\t\\tif text == '/cute':\\n\\t\\t\\tresponse = send_photo(chat_id)\\n\\n\\treturn response" },
                            { header: "Get a cute dog picture", vModel: '<div><ol><li><p>We have learned to send message to the chatbot and get feedback, in this step we are going to use bot_command to trigger a specific type of event in the chatbot</p></li><li><p>A public API is used to get a random cute dog picture and we will use the sendPhoto method to send it to the chat</p></li><li>You will need to understand the sendPhoto method in the API.<br><strong>sendPhoto</strong><blockquote><ul><li>Use this method to send photos. On success, the sent Message is returned.</li><li>Detailed documentation for the sendPhoto method can be found here: <a href="https://core.telegram.org/bots/api#sendphoto">https://core.telegram.org/bots/api#sendphoto</a>  </li></ul></blockquote></li></ol><ol start="4"><li>The bot_command for entity_type is set to be "/cute" to trigger the event</li></ol><p><img alt="image" src="https://drive.google.com/uc?export=view&amp;id=1vP3EMjxx3lZwk7ASJq1XQ2dlVbPlhb0h"></p><ol start="5"><li>Modify the <strong>#TO DO part</strong> in the code to pass the test</li></ol></div>' }
                        ], status: " 💬"
                    },
                                        {
                        name: "Step 6", uiItem: [
                            { header: "Tests", subHeader: '', vModel: "assert YOUR_TOKEN, 'Test failed. Please enter your api token.'\\nassert YOUR_CHAT_ID, 'Test failed. Please enter your chat id.'\\nassert REPLY_KEYBOARD, 'Test failed. Please create your two-line keyboard with four options'\\n\\nsampleEvent = {\\n\\t\\"body\\": json.dumps({\\n\\t\\t\\"message\\": {\\n\\t\\t\\t\\"chat\\": {\\n\\t\\t\\t\\t\\"id\\": YOUR_CHAT_ID,\\n\\t\\t\\t\\t\\"first_name\\": \\"Test\\",\\n\\t\\t\\t\\t\\"last_name\\": \\"User\\",\\n\\t\\t\\t\\t\\"type\\": \\"private\\"\\n\\t\\t\\t},\\n\\t\\t\\t\\"text\\": \\"/menu\\",\\n\\t\\t\\t\\"entities\\": [\\n\\t\\t\\t\\t{\\n\\t\\t\\t\\t\\t\\"offset\\": 0,\\n\\t\\t\\t\\t\\t\\"length\\": 5,\\n\\t\\t\\t\\t\\t\\"type\\": \\"bot_command\\"\\n\\t\\t\\t\\t}\\n\\t\\t\\t]\\n\\t\\t}\\n\\t})\\n}\\n\\nresponse = lambda_handler(sampleEvent, {})\\nassert response.status_code == 200, 'Test failed. GET response returned with not ok.'\\n\\ndata = response.json()\\nassert data['ok'], \\"Test failed. 'ok' should be True.\\"\\nassert str(data['result']['chat']['id']) == YOUR_CHAT_ID, \\"Test failed. chat id should be identical to YOUR_CHAT_ID.\\"\\nassert data['result']['text'] == 'Here is menu', \\"Test failed. text seems to be wrong.\\"" },
                            { header: "Editable Code Block", subHeader: 'Your code goes below', vModel: "from botocore.vendored import requests\\n\\n# TO DO PART I\\n# YOUR_TOKEN EXAMPLE\\n# YOUR_TOKEN = '123456:ABC-DEF1234ghIkl-zyx57W2v1u123ew11'\\n\\nYOUR_TOKEN = ''\\nYOUR_CHAT_ID = ''\\n\\n# TO DO PART II\\n# TO DO Create your two-line keyboard with four options:\\n# \\"Repeat after me\\", \\"Show me a cute dog\\"\\n# \\"Create a new data\\", \\"Query my data\\"\\nREPLY_KEYBOARD = {}\\n\\ndef send_message(chat_id):\\n\\tresponse_text = 'Here is menu'\\n\\n\\tdata = {\\n\\t\\t\\"chat_id\\": chat_id,\\n\\t\\t\\"text\\": response_text,\\n\\t\\t\\"reply_markup\\" : json.dumps(REPLY_KEYBOARD)\\n\\t}\\n\\n\\turl = f'https://api.telegram.org/bot{YOUR_TOKEN}/sendMessage'\\n\\tresponse = requests.post(url=url, data=data)\\n\\n\\treturn response\\n\\ndef lambda_handler(event, context):\\n\\t# TODO implement\\n\\tmessage = json.loads(event['body'])\\n\\tchat_id = message['message']['chat']['id']\\n\\ttext = message['message']['text']\\n\\tentity_type = message['message']['entities'][0]['type']\\n\\n\\tif entity_type == 'bot_command':\\n\\t\\tif text == '/menu':\\n\\t\\t\\tresponse = send_message(chat_id)\\n\\n\\treturn response" },
                            { header: "Interface options for Chat Bots", vModel: '<div><h3><strong>Overview</strong></h3><p>The main and the most natural way to communicate with a bot is to write them messages in natural language. However, in some cases it is more useful to provide a user an opportunity to select from predefined options or provide a form to fill in.</p><p><img alt="alt text" src="https://s3.amazonaws.com/gs-bot-images/Guides+image/serverless-webviews-using-gupshup/17626044_283918708702158_8986183537380032512_n.png"></p><p>(The picture is obtained from: <a href="https://www.gupshup.io/developer/docs/bot-platform/guide/serverless-webviews-using-gupshup">Gupshup</a>)</p><p>Telegram provides several interface solutions to simplify communication with bots: 1.   Custom keyboards. 2.   Inline keyboards. </p><h3><strong>Custom keyboard</strong></h3><p>Some typical use cases could be captured as a customized keyboard. This type of keyboards defines standard user reauests and simplify interaction process. There is no need to type a request, a user can simply select from predefined oprions and get necessary information.</p><p><img alt="alt text" src="https://sun9-34.userapi.com/c855420/v855420592/12e936/JNceBumHxMo.jpg"></p><p>(The picture is obtained from: <a href="https://core.telegram.org/bots#keyboards">core.telegram.org</a>)</p><h3><strong>Inline keyboard</strong></h3><p>There are some cases, when there is no need to send messages to the bot. For example, when a user wants to change some settings, go to any other page or look through search results. In such situations inline keyboard is a good solution. This type of keyboards provides a set of buttons integrated directly to the message they belong to. Pressing these buttons does not generate any messages sent to the chat, but triggers some functions like an update of the message text.</p><p><img alt="alt text" src="https://sun9-45.userapi.com/c854216/v854216592/13ab50/XwmouQdRAuo.jpg"></p><p>(The picture is obtained from: <a href="https://core.telegram.org/bots#keyboards">core.telegram.org</a>)</p><h3><strong>How to add a custom keyboard to your Digital Assistant?</strong></h3><p>The object "ReplyKeyboardMarkup" represents a custom keyboard with reply options. This object has 4 fields: 1 mandatory and 3 optional (the detailed description of the fields you can find <a href="https://core.telegram.org/bots/api/#replykeyboardmarkup">here</a>). </p><p>The object "ReplyKeyboardMarkup" should innclude information about predefined options (buttons). Buttons are defined as an array of arrays, where each new line defines new line in menu.</p><p>Example of defining the keyboard:</p><pre><code># one-line keyboard\\nreply_keyboard={"keyboard": [["Cute pic", "Weather", "Report"]], "resize_keyboard": True}\\n# two-line keyboard\\nreply_keyboard={"keyboard": [["Cute pic", "Weather"], ["Report"]], "resize_keyboard": True}\\n# Boolean field "resize_keyboard" adjusts the keybord to appropriate size</code></pre><p>To add a custom keyboard to your Chat Bot, you need to add special field "reply_markup" to any message you send to the user. </p><p>Now add a custom keyboard to your digital assistant. Do not forget to convert object into json. </p><ul><li>On success, you should see below menu in your telegram chatbot.</li></ul><span><img src="https://drive.google.com/uc?export=view&amp;id=1BHecUjj32mXDCXpGPzxiEZZjTz3TQvHL" width="600"></span><ul><li>Modify the <strong>#TO DO part</strong> in the code to pass the test</li></ul></div>' }
                        ], status: " 💬"
                    },
                                        {
                        name: "Step 7", uiItem: [
                            { header: "Tests", subHeader: '', vModel: "URL, shouldContain, amazonaws\\nURL, shouldContain, execute-api\\nGET, , response.body, shouldContain, new entry in google spreadsheet" },
                            { header: "Editable Code Block", subHeader: 'Your code goes below', vModel: "" },
                            { header: "Create your own Lambda function integrated with Google Sheet", vModel: '<div style="min-height: 200px;"><p>(If you have some prior experience in AWS lambda function, please skip this section) If you are new to the AWS Console, follow along these step-by-step instructions to create your very first lambda function.</p><p><a href="https://docs.google.com/presentation/d/1ZOeIJHmhwWF3docGCzR4PUA7NIIsBnriggW-smBgdew/edit?usp=sharing">AWS LAMBDA FUNCTION 2019</a></p><p>Once you\\'ve deployed your first lambda function. Please follow the following step by step instructions to create your very first Google Sheet Integrated AWS Lambda function. This function is to create new data entry in google sheet by lambda function.</p><p><a href="https://docs.google.com/presentation/d/1YKAV6EEk3OVfTP7t7NXeEef6MdqXSAqd5-n-jXOIff8/edit?usp=sharing">Google Sheet Integrated AWS LAMBDA FUNCTION</a></p><p>Once completed, copy and paste your API link in the editable box below for verification.</p><p>All the best! Happy Coding!</p></div>' }
                        ], status: " 💬"
                    },
                    {
                        name: "Step 8", uiItem: [
                            { header: "Tests", subHeader: '', vModel: "URL, shouldContain, amazonaws\\nURL, shouldContain, execute-api\\nGET, , response.body, shouldContain, query in google spreadsheet" },
                            { header: "Editable Code Block", subHeader: 'Your code goes below', vModel: "" },
                            { header: "Create your own Lambda function to query Google Sheet data", vModel: '<div style="min-height: 200px;"><p>Please follow the following step by step instructions to create your second Google Sheet Integrated AWS Lambda function. This function is to query google sheet data by lambda function.</p><p><a href="https://docs.google.com/presentation/d/1-l8bOIAbYJ1WVtjz9IvioAzRRK3mo4kwhZfVGwQUipU/edit?usp=sharing">Google Sheet Integrated AWS LAMBDA FUNCTION</a></p><p>Once completed, copy and paste your API link in the editable box below for verification.</p><p>All the best! Happy Coding!</p></div>' }
                        ], status: " 💬"
                    },
                    {
                        name: "Step 9", uiItem: [
                            { header: "Tests", subHeader: '', vModel: "assert (int(return_your_rating()) in list(range(1, 11))), 'You raiting should be from 1 to 10.'" },
                            { header: "Editable Code Block", subHeader: 'Your code goes below', vModel: "# Please give us your rating! It can be from 1 to 10.\\ndef return_your_rating():\\n\\treturn '10'" },
                            { header: "What do you think about the path?", vModel: '<div style="min-height: 200px;"><p>How likely are you to recommend this path to co-worker or friend?</p></div>' }
                        ], status: " 💬"
                    }
                ]
            }
        },
        methods: {
            toggleQuestionStatus(response) {
                const { data, questionName } = response
                if (data.htmlFeedback) {
                    const searchText = data.htmlFeedback

                    if (searchText.search("error") !== -1 || searchText.search(/#ff9999/) !== -1) {
                            this.questions.find(item => item.name === questionName).status = " 😡"
                    } else {
                        if (searchText.search("passed") !== -1) {
                            this.questions.find(item => item.name === questionName).status = " 😊"
                        }
                    }
                }
            }
        }
    })
    </script>
    """

    style = """
    <style lang="scss" scoped>
        body {
            font-family: 'Fira Code', monospace;
        }

        #logo {
            margin: 20px;
            font-weight: 200;
        }

        .md-card {
            width: 90%;
            margin: 20px;
            display: inline-block;
            vertical-align: top;
            min-height: 200px;
        }

        .md-card-content {
            padding-bottom: 16px !important;
        }

        button {
            display: block;
            margin: 20px 60px 20px 60px;
            width: 200px !important;
        }

        #cardGroupCreator {
            display: flex;
            flex-direction: column;
        }

        #cardGroupPreview .md-card {
            width: 90%;
        }

        #cardGroupPreview .md-tab {
            height: 100%;
        }

        textarea {
            font-size: 1rem !important;
            min-height: 175px !important;
        }

        .md-tabs {
            width: 100%;
        }

        .md-tab {
            overflow-x: auto;
        }

        .md-tab::-webkit-scrollbar {
            width: 0px;
        }

        html {
            width: 95%;
            margin: auto;
            mix-blend-mode: darken;
        }

        h1 {
            padding: 20px;
            margin: auto;
            text-align: center;
        }

        .md-content {
            min-height: 300px;
        }

        .md-tabs-container, .md-tabs-container .md-tab textarea, .md-tabs-content {
            height: 100% !important;
        }

        .md-field {
            margin: 0px;
            padding: 0px;
        }

        .md-tabs-navigation {
            justify-content: center !important;
        }

        .md-card-media {
            width: 400px !important;
        }

        .md-button {
            margin: 10px !important;
        }

        .cm-s-default {
            height: 100%;
        }

        .md-card-header {
            padding: 0 16px 16px 16px;
        }

        .videoContainer {
            position: relative;
            height: 0;
            padding-top: 56.25%;
            width: 100%;
        }

        .videoContainer iframe {
            position: absolute;
            top: 0;
            left: 0;
            border: 0;
            width: 100%;
            height: 100%;
        }
    </style>
    """

    indexPage=f"""
    <!DOCTYPE html>
    <html>
    {indexHead}
    {indexBody}
    {indexScriptsAfterBody}
    {vueComponent}
    {vueApp}
    {style}
    </html>
    """

    method = event.get('httpMethod',{})

    if method == 'GET':
        return {
            "statusCode": 200,
            "headers": {
            'Content-Type': 'text/html',
            },
            "body": indexPage
        }

    if method == 'POST':
        bodyContent = event.get('body',{})
        parsedBodyContent = json.loads(bodyContent)
        answer = parsedBodyContent["shown"]["0"]
        solution = parsedBodyContent["editable"]["0"]

        compiled = compile(solution + '\n' + answer, 'submitted code', 'exec')

        global YOUR_TOKEN
        global YOUR_CHAT_ID
        global data
        global response

        YOUR_TOKEN = ''
        YOUR_CHAT_ID = ''
        data = {}
        response = None

        results = None
        errors = None

        try:
            exec(compiled, globals())
        except Exception as e:
            errors = f'{type(e).__name__}: {e}'

        if not errors:
            results = 'Hurray! You have passed the test case.'
            htmlResults = f'{results}<br>'
            textResults = f'{results}\n'

            if data:
                htmlResults = htmlResults + f'The response of your function is {json.dumps(data)}'
                textResults = textResults + f'The response of your function is {json.dumps(data)}'
        else:
            results = 'An error has occured. Do look through the error message below to understand the cause.'
            htmlResults = f'{results}<br>{errors}'
            textResults = f'{results}\n{errors}'

        return {
            "statusCode": 200,
            "headers": {
                "Content-Type": "application/json"
            },
            "body": json.dumps({
                "isComplete": True,
                "jsonFeedback": json.dumps({'errors': f'{errors}'}),
                "htmlFeedback": htmlResults,
                "textFeedback": textResults
            })
        }