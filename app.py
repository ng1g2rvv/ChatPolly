from flask import Flask, request, render_template
import logging
import openai
import os
import boto3

log_dir = './logs'
if not os.path.exists(log_dir):
    os.makedirs(log_dir)

log_file = os.path.join(log_dir, 'chat.log')
logging.basicConfig(filename=log_file, level=logging.DEBUG)

messages = [{"role": "system", "content": "You are a knowledge, nice person to chat with and brainstorm ideas together. Your name is Salli."},]

def message_history_str(messages):
    output = "\n".join([line.get("role") + ": " + line.get("content") for line in messages])
    return output

def generate_response(prompt):
    messages.append({"role": "user", "content": prompt})

    openai.api_key = os.environ['OPENAI_API_KEY']
    response = openai.ChatCompletion.create(
        model="gpt-3.5-turbo",
        messages=messages
    )
    message = response.choices[0].message
    messages.append({"role": message.role, "content": message.content.strip()})
    return message.content.strip()

# def synthesize_speech(text):
#     polly = boto3.client('polly')
#     response = polly.synthesize_speech(
#         OutputFormat='mp3',
#         Text=text,
#         VoiceId='Joanna'
#     )
#     audio_data = response['AudioStream'].read()
#     return audio_data

app = Flask(__name__, static_folder='static')

@app.route('/', methods=['GET', 'POST'])
def chatbot():
    if request.method == 'POST':
        prompt = request.form['prompt']
        print(f"User message: {prompt}")
        response = generate_response(prompt)

        # logging
        # logging.info('User: ' + prompt)
        # logging.info('Salli: ' + response)
        logging.info("Message history: " + message_history_str(messages))
        return {'prompt': prompt, 'response': response}
    return render_template('index.html')


# @app.route('/audio', methods=['POST'])
# def process_audio():
#     audio_data = request.files.get('audio')
#     audio_path = './logs/audio.ogg'
#     audio_data.save(audio_path)
#     audio_file= open(audio_path, "rb")
#     prompt_transcript = openai.Audio.translate("whisper-1", audio_file)
#     logging.info('User: ' + prompt_transcript)

#     # prompt_transcript = "test input"
#     response = generate_response(transcript)
#     response = "test response"
#     logging.info('Salli: ' + response)
    
#     # audio_data = synthesize_speech(response)
#     return {'prompt': prompt_transcript, 'response': response}


if __name__ == '__main__':
    app.run()
