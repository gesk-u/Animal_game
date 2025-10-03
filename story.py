import textwrap

#insert user name instead of Teresa
def getStory(name):
    story = f"""{name} is a happy zoo keeper and the owner of Happy Animal Zoo. Matti is sent on a mission by a mysterious and villainous boss who wants to take the endangered zoo animals and sell them as pets.
    Matti takes 8 of the endangered animals and flies them through multiple airports to take them to their new 'owners'. You 
    are on the hunt for each and every animal before it is too late. Find the animals in time!"""



    # Set column width to 80 characters
    wrapper = textwrap.TextWrapper(width=80, break_long_words=False, replace_whitespace=False)
    # Wrap text
    word_list = wrapper.wrap(text=story)



    return word_list
