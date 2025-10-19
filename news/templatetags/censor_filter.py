from django import template

register = template.Library()

bad_words = [
    'дебил', 'урод', 'травь', 'дурак', 'мерзавец'
]


@register.filter()
def censor(value):
    if not isinstance(value, str):
        return value

    words = value.split()
    censored_words = []

    for word in words:
        clean_word = word
        word_lower = word.lower()
        is_bad = False


        for bad_word in bad_words:
            if bad_word in word_lower:
                is_bad = True
                break

        if is_bad and len(clean_word) > 1:
            censored_word = clean_word[0] + '*' * (len(clean_word) - 1)
            censored_words.append(censored_word)
        else:
            censored_words.append(clean_word)

    return ' '.join(censored_words)
