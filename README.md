# LiveKit Assistant

Demo Video
[![Demo Video](https://static-assets-v2.s3.us-east-2.amazonaws.com/uploads/1743155746229_Screenshot%202025-03-28%20at%201.39.24%C3%A2%C2%80%C2%AFPM.png)](https://youtu.be/Y7uTbt1ITQA)

Admin - Configure Interviewer Screen
![Admin - Configure Interviewer Screen](https://static-assets-v2.s3.us-east-2.amazonaws.com/uploads/1743155848750_Screenshot%202025-03-28%20at%201.36.40%C3%A2%C2%80%C2%AFPM.png)

Admin - View Results Screen
![Admin - View Results Screen](https://static-assets-v2.s3.us-east-2.amazonaws.com/uploads/1743155990011_results.png)

First, create a virtual environment, update pip, and install the required packages:

```
$ python3 -m venv .venv
$ source .venv/bin/activate
$ pip install -U pip
$ pip install -r requirements.txt
```

You need to set up the following environment variables:

```
LIVEKIT_URL=...
LIVEKIT_API_KEY=...
LIVEKIT_API_SECRET=...
DEEPGRAM_API_KEY=...
OPENAI_API_KEY=...
```

Then, run the assistant:

```
$ python3 assistant.py download-files
$ python3 assistant.py start
```

Finally, you can load the [hosted playground](https://agents-playground.livekit.io/) and connect it.