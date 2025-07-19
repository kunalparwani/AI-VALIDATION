import numpy as np


def predict_vulnerability(model, tokens):
    """
    Runs the given tokens through the model and returns
    a structured prediction result.
    """
    prediction = model.predict(tokens)
    predicted_class = np.argmax(prediction)

    if predicted_class == 0:
        label = "secure"
    else:
        label = "vulnerable"

    return label
