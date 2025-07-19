from transformers import RobertaTokenizer

def preprocess_code_sliding_window(file_path, maxlen=200, stride=100):
    with open(file_path, "r") as f:
        code = f.read()

    tokenizer = RobertaTokenizer.from_pretrained("microsoft/graphcodebert-base")
    tokens = tokenizer(code, return_tensors='pt', truncation=False)

    input_ids = tokens['input_ids'][0].tolist()  # Convert tensor to list

    chunks = []
    num_tokens = len(input_ids)

    # Sliding window logic
    for start in range(0, num_tokens, stride):
        end = start + maxlen
        chunk = input_ids[start:end]

        # Pad chunk if shorter than maxlen
        if len(chunk) < maxlen:
            chunk += [tokenizer.pad_token_id] * (maxlen - len(chunk))

        chunks.append(chunk)

        if end >= num_tokens:
            break

    return chunks, tokenizer


# from transformers import RobertaTokenizer



# def preprocess_code_sliding_window(file_path, maxlen=200, stride=100):
#     with open(file_path, "r") as f:
#         code = f.read()
        

#     tokenizer = RobertaTokenizer.from_pretrained("microsoft/graphcodebert-base")
#     tokens = tokenizer(code, return_tensors='pt', truncation=False)
#     print(tokens)

#     input_ids = tokens['input_ids'][0].tolist()  # Convert tensor to list

#     chunks = []
#     num_tokens = len(input_ids)

#     # Sliding window logic
#     for start in range(0, num_tokens, stride):
#         end = start + maxlen
#         chunk = input_ids[start:end]
#         print(chunk)

#         # Pad chunk if shorter than maxlen
#         if len(chunk) < maxlen:
#             chunk += [tokenizer.pad_token_id] * (maxlen - len(chunk))

#         chunks.append(chunk)

#         if end >= num_tokens:
#             break

#     return chunks, tokenizer


# preprocess_code_sliding_window("C:\\Users\\rashm\\Desktop\\AI_Code_Validation_Project\\temp_code.py")


