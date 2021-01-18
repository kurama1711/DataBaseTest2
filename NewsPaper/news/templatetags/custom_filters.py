from django import template


register = template.Library()


@register.filter(name='censor')
def censor(value):
    bad_words = ['текст', 'ещё']
    tmp_value = value
    for word in bad_words:
        tmp_value = tmp_value.replace(word, '*ОЙ*')
    return tmp_value
