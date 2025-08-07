# BOB-assistant-Voice-lock


Voice lock for B.O.B, uses a learnt model to unlock bob,
this is in development and no where near secure.
also here is the program to make a model.

rec_1.py (is for makeing the voice files for the modle to use)
rec.py (this can be used to train the modle and make a yaml file.)

########################################################

samples = [extract_features(f) for f in files]
#model = train_hmm(samples)
#print("trained")
model = joblib.load("voice_model.pkl")

(uncommment then run, then recomment)



*ajust the path for B.O.B if needed is set open Gui for web acsses,
but can be set to open B.O.B direacly if wanted*
