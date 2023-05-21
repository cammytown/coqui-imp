from typing import Optional
from TTS.api import TTS
import simpleaudio as sa

class CoquiImp:
    tts: TTS
    auto_select_count: int = 0
    verbose: bool = False

    def __init__(self,
                 model_name: Optional[str] = None,
                 gpu: bool = False,):

        if(not model_name):
            # List available models and choose the first one
            # model_name = TTS.list_models()[0]
            # model_name = "tts_models/en/ljspeech/tacotron2-DCA"
            # model_name = "tts_models/en/ljspeech/vits"
            # tts_models/multilingual/multi-dataset/your_tts
            model_name = "tts_models/en/ljspeech/glow-tts"

        # Init TTS
        print(f"Loading TTS model: {model_name} ...")
        self.tts = TTS(model_name = model_name,
                       gpu = gpu)

    def say(self,
            text: str,
            output_path: str = "coqui_output.wav",
            speaker: Optional[str] = None,
            # language: Optional[str] = None
    ) -> sa.PlayObject:
        if __debug__ and self.verbose:
            print('CoquiImp saying: ' + text)

        args = {
            "text": text,
            "file_path": output_path,
        }

        # Run TTS
        # If multi-voice
        if(self.tts.speakers):
            if(speaker):
                args["speaker"] = speaker
            else:
                args["speaker"] = self.tts.speakers[0]

        # If multi-language
        if(self.tts.languages):
            args["language"] = self.tts.languages[0]

        self.tts.tts_to_file(**args)

        # Play the output file
        wave_obj = sa.WaveObject.from_wave_file(output_path)
        play_obj = wave_obj.play()

        return play_obj

    #@REVISIT naming
    def auto_select_speaker(self):
        # if self.tts:
        #@REVISIT only for multi-speaker TTS
        #@TODO obviously tts.tts is bad; revisit
        if(self.tts.speakers):
            speaker_index = self.auto_select_count % len(self.tts.speakers)
            self.auto_select_count += 1

            return self.tts.speakers[speaker_index]
        # else:
            # return None
