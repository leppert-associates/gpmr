def format_tag(tag_name, attributes, inner="", closed=False, opened=False):
    tag = "<{tag} {attributes}"
    if closed:
        tag += "/>"
    elif opened:
        tag += ">"
    else:
        tag += ">" + inner + "</{tag}>"
    return tag.format(
        tag=tag_name,
        attributes=" ".join(['{}="{}"'.format(k, v)
                            for k, v in attributes.items()]),
    )


def format_tags(tag_name, attributes, inner="", closed=False, opened=False):
    attrs = " ".join([f"{k}=\"{v}\"" for k, v in attributes.items()])
    tag = f"<{tag_name} {attrs}"
    if closed:
        tag += "/>"
    elif opened:
        tag += ">"
    else:
        tag += f">{inner}</{tag_name}>"
    return tag


print(format_tag('H1', {'title': 'hello', 'class': 'big-header'}))
print(format_tags('H1', {'title': 'hello', 'class': 'big-header'}))

# walrus:=
# x = 2
# if (i := x*2) > 1:
#     print(i)

# a = [9, 1, 3, 4]
# if (n := len(a)) > 1:
#     print(f"List is too long ({n} elements, expected <= 10)")
