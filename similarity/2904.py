import tensorflow as tf
from tensorflow.keras import layers

# Word2Vec modeli
class Word2Vec(tf.keras.Model):
    def __init__(self, vocab_size, embedding_dim):
        super(Word2Vec, self).__init__()
        self.target_embedding = layers.Embedding(vocab_size,
                                          embedding_dim,
                                          name="w2v_embedding")
        self.context_embedding = layers.Embedding(vocab_size,
                                           embedding_dim)

    def call(self, pair):
        target, context = pair
        # target: (batch, dummy?)  # The dummy axis doesn't exist in TF2.7+
        # context: (batch, context)
        if len(target.shape) == 2:
            target = tf.squeeze(target, axis=1)
        # target: (batch,)
        word_emb = self.target_embedding(target)
        # word_emb: (batch, embed)
        context_emb = self.context_embedding(context)
        # context_emb: (batch, context, embed)
        dots = tf.einsum('be,bce->bc', word_emb, context_emb)
        # dots: (batch, context)
        return dots

# Metindeki kelime benzerliklerini hesapla
def calculate_similarity(text):
    # Metni uygun şekilde işle ve tokenize et
    tokens = text.split()
    token_ids = [word_index[word] for word in tokens if word in word_index]
    
    # Modelin target_embedding katmanını al
    embedding_layer = word2vec_model.target_embedding
    
    # Her kelimenin gömülmesini al
    word_embeddings = embedding_layer(tf.constant(token_ids))
    
    # Her kelime gömülmelerinin ortalamasını al
    text_embedding = tf.reduce_mean(word_embeddings, axis=0)
    
    # Tüm kelime gömülmelerini içeren bir matris oluştur
    all_word_embeddings = embedding_layer.weights[0]
    
    # Metindeki her kelimenin gömülmesi ile tüm kelimelerin gömülmeleri arasındaki benzerliği hesapla
    similarities = tf.keras.metrics.cosine_similarity(all_word_embeddings, text_embedding)
    
    return similarities

# Eğitim sırasında tanımlanan değişkenler
vocab_size = 10000
embedding_dim = 128

# Eğitilmiş modeli yükle
word2vec_model = Word2Vec(vocab_size,embedding_dim)
word2vec_model.load_weights('word2vec_model_weights.h5')

# Metindeki kelime benzerliklerini hesapla ve göster
text = "bir metin içindeki kelime benzerliklerini hesapla"
similarities = calculate_similarity(text)
print(similarities)
