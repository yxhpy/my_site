from bs4 import BeautifulSoup
from django import template

register = template.Library()


@register.filter()
def get_text(html, num):
    soup = BeautifulSoup(html, 'html.parser')
    text = soup.get_text()
    return ''.join(text[0:num+1])+'.....'
