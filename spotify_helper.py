from spotify import search, get_audio_features

# Global variables
VALENCE_ENERGY_THRESHOLD = 0.09

# Params:   azure_cognitive emotion JSON for one person
#           n
# Returns:  list of n Spotify track objects
def track_recommendations(emotion_json, n):

    # Validate inputs
    if int(sum(emotion_json[i] for i in emotion_json.keys())) != 1:
        return

    # Reformat emotion data into spotify-queryable quantities
    emotion = max(emotion_json, key=lambda x: emotion_json[x])
    valence, energy = _format_emotion_data(emotion_json)

    # Find n track recommendations
    tracks = []
    i = 0
    while len(tracks) < n and i <= 2000:

        # Search spotify tracks for dominant emotion
        search_res = search(emotion, i)
        track_objects = list(search_res["tracks"]["items"])
        ids = [i["id"] for i in track_objects]

        # Get audio features for tracks
        if ids == list():
            break
        audio_features = get_audio_features(ids)

        # Prune audio features by target valence and energy
        _prune_audio_features(audio_features=audio_features, target_type='valence', target_value=valence)
        _prune_audio_features(audio_features=audio_features, target_type='energy', target_value=energy)

        # Add matching track objects to tracks list
        audio_features_objects = list(audio_features['audio_features'])
        ids = set([i["id"] for i in audio_features_objects])
        tracks += [i for i in track_objects if i["id"] in ids]

        # Increment offset by 50, the max limit for spotify search results  
        i += 50
    
    return tracks

# Params:   azure_cognitive emotion JSON for one person
# Returns:  dominant emotion
#           valence (0.000 to 1.000)
#           energy (0.000 to 1.000)
def _format_emotion_data(emotion_json):

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
def _prune_audio_features(audio_features, target_type, target_value):
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