import re
import numpy as np
from gensim.models import Word2Vec

# Load Word2Vec model
w2v_model = Word2Vec.load("models/word2vec_withString10-200-300.model")
embedding_dim = w2v_model.vector_size  # should be 300

def tokenize_code(code):
    return re.findall(r'\b\w+\b', code)

def preprocess_code_sliding_window(file_path, maxlen=200, stride=100):
    with open(file_path, "r") as f:
        code = f.read()

    tokens = tokenize_code(code)

    vectorized = []
    for token in tokens:
        if token in w2v_model.wv:
            vectorized.append(w2v_model.wv[token])
        else:
            vectorized.append(np.zeros(embedding_dim))

    chunks = []
    for start in range(0, len(vectorized), stride):
        end = start + maxlen
        chunk = vectorized[start:end]

        if len(chunk) < maxlen:
            chunk.extend([np.zeros(embedding_dim)] * (maxlen - len(chunk)))

        chunks.append(np.array(chunk))

        if end >= len(vectorized):
            break

    return chunks
