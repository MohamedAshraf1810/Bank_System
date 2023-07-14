import numpy as np
from scipy.io import wavfile
from python_speech_features import mfcc
import pickle
import numpy as np
import warnings
warnings.filterwarnings("ignore")
import wave

def VoiceRec_Model(username):
    try:
        def extract_features(file_path):
            sample_rate, audio = wavfile.read(file_path)
            mfcc_features = mfcc(audio, sample_rate,nfft=1200,nfilt=30 , appendEnergy=True)
            return mfcc_features
        
        # Load the trained model from the pickle file
        with open(f'Voice_Recognition_Utilities/Models/{username}/{username}.pk', 'rb') as f:
            clf = pickle.load(f)
        # Extract features from a new audio file
        new_file_path = f'Voice_Recognition_Utilities/AuthenticationWaves/{username}/{username}.wav'
        new_features = extract_features(new_file_path)
        
        with wave.open(new_file_path,'rb') as wav_file:
            frames = wav_file.getnframes()
        print(frames)
        
        # Pad the feature vector with zeros to match the maximum length used during training
        max_len = clf.support_vectors_.shape[1] // 13
        num_missing_samples = max_len - new_features.shape[0]
        padded_new_features = np.pad(new_features, ((0, num_missing_samples), (0, 0)), mode='constant')

        # Reshape the feature vector to have two dimensions and predict the speaker
        flat_features = padded_new_features.reshape(1, -1)
        prediction_probability = clf.predict_proba(flat_features)[0]
        identified_speaker_name  = clf.predict(flat_features)[0]
        
        print("---------------------------")
        print(prediction_probability)
        print(clf.classes_)
        print("---------------------------")

        max_acc = prediction_probability.max()*100
        
        if (max_acc < 96 or identified_speaker_name == 'other'):
            identified_speaker_name = "UnKnown"
            print('The Predicted Speaker Is : ', identified_speaker_name)
            return False
        else:
            print('The Predicted Speaker Is : ', identified_speaker_name)
            print("The Model Accuracy Is = " , round(max_acc,2) , "%")
            return True

    except Exception as e:
        print(e)




# !!!!!!!!!!!!!!!
# The Return Will BE Ture Or False ONLYYYYYYYYYYYYYYYYYYYYYYYYYYYYYYYYYYY
# !!!!!!!!!!!!!!!







