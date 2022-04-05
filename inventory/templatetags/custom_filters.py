from django import template

register = template.Library()

@register.filter
def getValueFromKey(dict, key):
    return dict.get(key) # use .get so func returns "None" if key is absent; dict[key] would return a KeyError in this case


# <MenuItem: Steak>: 'Not enough inventory. You only have 15.00 Grams of Eggs left.'