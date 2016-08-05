from train import *
from diff import  *
from Tokenizer import  *
_VOCABULARY_SIZE = int(os.environ.get('VOCABULARY_SIZE', '5000'))


song_lyrics = get_lyrics()
song_lyrics = insert_special_token(song_lyrics)
tokenized_sentences = tokenize_song_to_word(song_lyrics)
vocabulary = create_vocabulary(_VOCABULARY_SIZE, tokenized_sentences)
index_to_word = map_index_to_word(vocabulary)
word_to_index = map_word_to_index(index_to_word)
replace_word_not_in_vocabulary(word_to_index,tokenized_sentences)


num_sentences = 38
senten_min_length = 6
model = getModel(tokenized_sentences, word_to_index)
song = ""
list_song = []

sent = generate_sentence(model,word_to_index, index_to_word, song_start_token, sentence_end_token)

ssent = ""
for word in sent:
    ssent += word + " "
song += ssent + "\n"
list_song.append(ssent)




print ("start iteration")
for i in range(num_sentences):
    sent = []
    ssent =""
    # We want long sentences, not sentences with one or two words
    while len(sent) < senten_min_length:
        sent = generate_sentence(model,word_to_index, index_to_word, sentence_start_token, sentence_end_token)
    print " ".join(sent)
    for word in sent:
        ssent += word + " "
    list_song.append(ssent)
    song += ssent + "\n"

print ("finish iteration")
sent = generate_sentence(model,word_to_index, index_to_word, sentence_start_token, song_end_token)
ssent = ""
for word in sent:
    ssent += word + " "
song += ssent + "\n"
list_song.append(ssent)

print (song)
newSong = open ("outputsong.txt", "wb")
newSong.write(song)
newSong.close()
diff = calculate_cosine_for_song(list_song, song_lyrics)
print (diff)




