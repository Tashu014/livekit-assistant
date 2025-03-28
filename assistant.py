import os 
import json
import asyncio
import logging

from livekit.agents import AutoSubscribe, JobContext, WorkerOptions, cli, llm
from livekit.agents.pipeline import VoicePipelineAgent
from livekit.plugins import deepgram, openai, silero

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger("ai-interviewer")


async def entrypoint(ctx: JobContext):
    await ctx.connect(auto_subscribe=AutoSubscribe.AUDIO_ONLY)
    participant = await ctx.wait_for_participant()
    candidate_id = participant.identity

    with open('admin_data/jd.json', 'r') as jd_file:
        jd_data = json.load(jd_file)
    if os.path.exists('admin_data/prompt.json') and os.path.getsize('admin_data/prompt.json') > 0:
        with open('admin_data/prompt.json', 'r') as prompt_file:
            try:
                additional_instructions = json.load(prompt_file).get('system_prompt', '')
            except json.JSONDecodeError:
                additional_instructions = ''
    else:
        additional_instructions = ''

    initial_context = llm.ChatContext().append(
        role="system",
        text=(
            f"You are an AI interviewer. You are conducting an interview for a position based on the following job description: {jd_data['job_description']}. "
            "Your interface with the user is via voice only, asking technical questions. Keep responses concise and to the point. "
            "Ask one question at a time, focusing on the job requirements, and wait for the answer. "
            "Analyze the candidate's responses and keep asking appropriate follow-up questions. "
            "Maintain a professional and encouraging demeanor throughout the interview. "
            "Avoid using unpronounceable punctuation or emojis."
            f"{additional_instructions}"
        )
    )

    vad_model = silero.VAD.load() 
    stt_model = deepgram.STT(model="nova-3-general")  
    llm_model = openai.LLM(model="gpt-4o") 
    tts_model = openai.TTS()  

    assistant = VoicePipelineAgent(
        vad=vad_model,
        stt=stt_model,
        llm=llm_model,
        tts=tts_model,
        chat_ctx=initial_context,
        allow_interruptions=True
    )

    def before_llm_callback(chat_context: llm.ChatContext):
        MAX_HISTORY = 6  
        messages = chat_context.messages
        if len(messages) > MAX_HISTORY + 1:
            system_msg = messages[0]
            recent_msgs = messages[-MAX_HISTORY:]
            new_ctx = llm.ChatContext()
            new_ctx.append(role=system_msg.role, text=system_msg.text)
            for msg in recent_msgs:
                new_ctx.append(role=msg.role, text=msg.text or "")
            assistant.chat_ctx = new_ctx
        return None

    assistant.before_llm_cb = before_llm_callback

    assistant.start(ctx.room, participant)
    candidate_responses = []
    @assistant.on("user_speech_committed")
    def on_user_speech_committed(msg: llm.ChatMessage):
        try:
            response_data = {
                'candidate_id': candidate_id,
                'response': msg.content
            }
            candidate_responses.append(response_data)
            with open('conversation_data.json', "w") as f:
                json.dump(candidate_responses, f, indent=4)
        except Exception as e:
            logger.error(f"Error saving responses: {str(e)}")

    await asyncio.sleep(1.0)
    initial_greeting = "Hello, I am an AI interviewer. Let's begin. Please tell me about yourself."
    await assistant.say(initial_greeting)

    try:
        await asyncio.Future()
    except Exception as e:
        logger.info("Interview session ended.")

if __name__ == "__main__":
    cli.run_app(WorkerOptions(entrypoint_fnc=entrypoint))