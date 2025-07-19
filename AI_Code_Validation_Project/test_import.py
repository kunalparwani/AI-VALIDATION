from keras.models import load_model
# or from keras.models import load_model
from scripts import myutils

model = load_model(
    "models/LSTM_model_command_injection_gcbt.h5",
    custom_objects={'f1_loss': myutils.f1_loss, 'f1':myutils.f1}
)

print("Model loaded successfully")