# LiveKit Assistant

[![Demo Video](https://drive.google.com/file/d/1orXwHBIkRkn8uSH18Ul2klb4AlqvTMmh/view?usp=sharing)](https://drive.google.com/file/d/1lL5JB6ycCZGO12aHRqxhRqex7Twm966_/view?usp=sharing)

![Admin - Configure Interviewer Screen](https://drive.google.com/file/d/1JrHB6Jg95_gtqsn59uat6hb7tgjZVtum/view?usp=sharing)

![Admin - View Results Screen](https://drive.google.com/file/d/1UH_BgcPsbfuHL6OVGwhhzBuWrYlIgol4/view?usp=sharing)

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