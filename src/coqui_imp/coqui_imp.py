from TTS.api import TTS
from playsound import playsound

class CoquiImp:
    tts: TTS
    auto_select_count: int = 0
    verbose: bool = False

    def __init__(self, model_name: str = None):
        if(not model_name):
            # List available models and choose the first one
            # model_name = TTS.list_models()[0]
            # model_name = "tts_models/en/ljspeech/tacotron2-DCA"
            # model_name = "tts_models/en/ljspeech/vits"
            model_name = "tts_models/en/ljspeech/glow-tts"

        # Init TTS
        self.tts = TTS(model_name)

    def say(self,
            message: str,
            output_path: str = "coqui_output.wav",
            speaker: str = None,
            # language: str = None
    ):
        if __debug__ and self.verbose:
            print('CoquiImp saying: ' + message)

        if(not speaker):
            speaker = self.tts.speakers[0]

        # Run TTS
        # If multi-voice:
        if(self.tts.speakers):
            self.tts.tts_to_file(text=message,
                            speaker=speaker,
                            language=self.tts.languages[0],
                            file_path=output_path)
        else:
            self.tts.tts_to_file(text=message,
                            file_path=output_path)

        # Play the output file:
        playsound(output_path)

    #@REVISIT naming
    def auto_select_speaker(self):
        # if self.tts:
        #@REVISIT only for multi-speaker TTS:
        #@TODO obviously tts.tts is bad; revisit
        if(self.tts.speakers):
            speaker_index = self.auto_select_count % len(self.tts.speakers)
            self.auto_select_count += 1

            return self.tts.speakers[speaker_index]
        # else:
            # return None
