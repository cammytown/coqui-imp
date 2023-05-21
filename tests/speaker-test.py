import os
import sys
from TTS.api import TTS
from coqui_imp import CoquiImp

# If --list-models
if("--list-models" in sys.argv):
    models = TTS.list_models()
    print("Available models:")
    print("\n".join(models))
    exit()

# Get the directory of this script
script_dir = os.path.dirname(os.path.abspath(__file__))

# Create output directory if it doesn't exist
output_dir = f"{script_dir}/output"
os.makedirs(output_dir, exist_ok=True)

# My (Cammy's) personal quasi-order of preference for TTS models:
# - tts_models/en/ljspeech/overflow - natural, high quality, one (female) voice
# - tts_models/en/ljspeech/tacotron2-DDC - fairly natural, high quality
# - tts_models/en/ljspeech/glow-tts - high quality, sometimes unnatural
# - tts_models/en/ljspeech/fast_pitch - odd, lots of artifacts, but natural
# - tts_models/en/ljspeech/tacotron2-DCA - basically worse version of DDC
# - tts_models/en/ek1/tacotron2 - natural, poor quality
# - tts_models/en/ljspeech/speedy-speech-wn - fairly natural, with artifacts
# - tts_models/en/vctk/sc-glow-tts
# - tts_models/en/sam/tacotron-DDC - good for a robot voice

# # If --test-every-model
# if("--test-every-model" in sys.argv):
#     models = TTS.list_models()

#     # For each model
#     for model in models:
#         imp = CoquiImp(model_name = model,
#                        gpu = True)
#         imp.say("Hello, world!",
#                 output_path = f"{output_dir}/2_glow-gpu.wav")

model_name = "tts_models/en/ljspeech/fast_pitch"
# model_name = "tts_models/en/ljspeech/overflow"
# model_name = "tts_models/en/ljspeech/glow-tts"
# model_name = "tts_models/en/vctk/sc-glow-tts"

imp = CoquiImp(model_name = model_name,
               gpu = True)

# Remove tts_models and replace / with _
model_dirname = model_name.replace("tts_models/", "").replace("/", "_")
output_model_dir = f"{output_dir}/{model_dirname}"

# Create the output directory if it doesn't exist
os.makedirs(output_model_dir, exist_ok=True)

speech = "You see, human society has come under the thumb of an evil known as Capitalism and is being gradually destroyed by its actions."

# If multiple speakers:
if imp.tts.speakers:
    # For each speaker, say text
    for speaker in imp.tts.speakers:
        filename = speaker.replace(" ", "_") + ".wav"
        output_path = f"{output_model_dir}/{filename}"

        imp.say(speech,
                speaker = speaker,
                output_path = output_path)
else:
    # Say text with only speaker
    imp.say(speech,
            output_path = f"{output_model_dir}/output.wav")
