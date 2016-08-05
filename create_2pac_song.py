from train import *


_VOCABULARY_SIZE = int(os.environ.get('VOCABULARY_SIZE', '5000'))


song_lyrics = get_lyrics()
song_lyrics = insert_special_token(song_lyrics)
tokenized_sentences = tokenize_song_to_word(song_lyrics)
vocabulary = create_vocabulary(_VOCABULARY_SIZE, tokenized_sentences)
index_to_word = map_index_to_word(vocabulary)
word_to_index = map_word_to_index(index_to_word)
replace_word_not_in_vocabulary(word_to_index,tokenized_sentences)


num_sentences = 40
senten_min_length = 4
model = getModel(tokenized_sentences, word_to_index)
song = ""
for i in range(num_sentences):
    sent = []
    # We want long sentences, not sentences with one or two words
    while len(sent) < senten_min_length:
        sent = generate_sentence(model,word_to_index, index_to_word)
    print " ".join(sent)
    for word in sent:
        song += word + " "
    song += "\n"

newSong = open ("outputsong.txt", "wb")
newSong.write(song)
newSong.close()



