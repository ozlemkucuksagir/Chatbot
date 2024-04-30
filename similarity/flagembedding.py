from FlagEmbedding import FlagModel

sentences_1 = ["Example Data 1", "Example Data 2"]
sentences_2 = ["Example Data 3", "Example Data 4"]

model = FlagModel('BAAI/bge-large-en-v1.5', 
                  query_instruction_for_retrieval="Generate representation for this sentence to retrieve relevant articles:",
                  use_fp16=True) # Setting use_fp16 to True speeds up computation with a slight performance degradation

embeddings_1 = model.encode(sentences_1)
embeddings_2 = model.encode(sentences_2)

similarity = embeddings_1 @ embeddings_2.T
print(similarity)

# For short query to long passage (s2p) retrieval task, suggest using encode_queries()
# which will automatically add the instruction to each query
# Corpus in retrieval task can still use encode() or encode_corpus(), since they don't need instruction

queries = ['query_1', 'query_2']
passages = ["Example Document 1", "Example Document 2"]

q_embeddings = model.encode_queries(queries)
p_embeddings = model.encode(passages)

scores = q_embeddings @ p_embeddings.T
print(scores)
