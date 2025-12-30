def count_words(text):
    text = text.lower()
    
    text = text.replace(".", "")
    text = text.replace(",", "")
    text = text.replace("!", "")
    
    words = text.split()
    
    word_dictionary = {}
    
    for word in words:
        if word in word_dictionary:
            word_dictionary[word] = word_dictionary[word] + 1
        else:
            word_dictionary[word] = 1
            
    return word_dictionary

my_text = "Яблуко груша яблуко, банан. Груша яблуко стіл стілець стіл. Яблуко яблуко."

result_dict = count_words(my_text)
print("Словник слів:", result_dict)

frequent_words = []
for word in result_dict:
    count = result_dict[word]
    if count > 3:
        frequent_words.append(word)

print("Слова, що зустрічаються більше 3 разів:", frequent_words)
print("-" * 30)
