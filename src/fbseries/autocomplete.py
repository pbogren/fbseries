"""A function for autocompleting."""


def autocomplete(query, word_list):
    """Find longest common substring of items starting with query."""
    filtered_list = [
        word
        for word
        in sorted(word_list)
        if word.lower().startswith(query.lower())
    ]
    print(f"filtered: {filtered_list}")
    # Skip some steps if possible
    if not filtered_list:
        return ""
    if len(filtered_list) == 1:
        return filtered_list[0]

    # The first word in the sorted list is the shortest one and the only
    # possible match for a longest common substring.
    first_word = filtered_list.pop(0)
    start = len(query)
    for index, letter in enumerate(first_word[start:], start=start):
        if not letter_in_all(index, letter, filtered_list):
            substring = first_word[:index]
            break
    else:
        # No break -> first_word is a substr of every word in the list::
        substring = first_word

    return substring


def letter_in_all(index, letter,  words):
    """Check if every string in words has letter att position index."""
    for word in words:
        if word[index].lower() != letter.lower():
            return False
    else:
        return True
