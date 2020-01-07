import fastText
from gensim.models.wrappers import FastText 

ft_model = FastText.load_fasttext_format('/opt/PhD/Work/LSTM/fasttext/cc.hi.300.bin')

def get_vector(word):
    print(ft_model.get_word_vector(word))

get_vetor('हमारी')
