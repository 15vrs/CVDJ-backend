# Miscellaneous helper functions for Spotify related code.

# Global variables
VALENCE_ENERGY_THRESHOLD = 0.09

# Params:   azure_cognitive emotion JSON for one person
# Returns:  dominant emotion
#           valence (0.000 to 1.000)
#           energy (0.000 to 1.000)
def format_emotion_data(emotion_json):

    A = emotion_json['anger']
    C = emotion_json['contempt']
    D = emotion_json['disgust']
    F = emotion_json['fear']
    H = emotion_json['happiness']
    N = emotion_json['neutral']
    SA = emotion_json['sadness']
    SU = emotion_json['surprise']

    # Calculate target valence
    valence = ((H+SU) - (A+C+D+F+SA) + 1) / 2 

    # Calculate target energy
    energy = (5*SU + 4*A + 3*F + 2*C + 2*D + H) / 5 

    return valence, energy

# Params:   list of audio features objects
#           target value type 
#           target value
# Returns:  None, modifies audio_features object
def prune_audio_features(audio_features, target_type, target_value):
    global VALENCE_ENERGY_THRESHOLD

    # Validate inputs
    if target_type != 'energy' and target_type != 'valence':
        return
    if audio_features == None:
        return
    if audio_features['audio_features'] == None or list(audio_features['audio_features']) == list():
        return

    # Prune
    temp = [i for i in list(audio_features['audio_features']) 
    if type(i) == type(dict()) 
    and abs(i[target_type] - target_value) < VALENCE_ENERGY_THRESHOLD]
    audio_features['audio_features'] = temp

