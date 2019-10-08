    import os
    import slack

    client = slack.WebClient(token=os.environ['SLACK_API_TOKEN'])

    response = client.chat_postMessage(
        channel='DD40Y5M0Q',
        text="Hello world!")
    assert response["ok"]
    assert response["message"]["text"] == "Hello world!"