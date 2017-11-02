""" A function for autocompleting"""


def autocomplete(query, word_list):
    """ Return least common denominator of strings in word_list
    beginning with 'query'.
    """
    filtered_list = [
        word
        for word
        in word_list
        if word.lower().startswith(query.lower())
    ]
    # Skip some steps if possible
    if not filtered_list:
        return ""
    if len(filtered_list) == 1:
        return filtered_list[0]
    # Find least common denominator by comparing each word
    # in the list to the first word
    index = len(query)
    shortest_word = min(map(len, filtered_list))
    first_word = filtered_list[0]
    del filtered_list[0]
    substring = ""
    done = False
    while index < shortest_word and not done:
        letter = first_word[index]
        for word in filtered_list:
            if word[index] != letter:  # found all matching letters
                substring = first_word[:index]
                done = True
                break
        index += 1
    return substring
