import textwrap

#insert user name instead of Teresa
def getStory(name):
    story = f"""{name} is a zookeeper from Happy Animals Zoo, and your endangered animals have been taken by a villainous mob boss named Matti, who has taken the animals to the airport to sell and distribute them to new and prospective owners all in very short time. 
     But while boarding Matti's private jet, the animals escaped their pens and have now been taken to random airports. 
     Matti also dropped his list of private airports where his jet frequently stops to refuel. 
     You have pursued and followed Matti to the airport and saw this happening from afar; 
     however, after Matti's jet has taken off, you step on a piece of paper which, upon closer inspection, is revealed to be Matti's private airport list. 
     Armed with this list and some money, you start off on your animal adventure, where you will rescue and reclaim the endangered animals from your zoo. 
     Your task is to first select an airport where you will start. Along this journey, you will need luck, grit, and sisu to help find the animals. 
     You might come across briefcases left behind by Matti's assistants. Avoid them at all costs if you want to find animals as fast as possible but mind your resources.
     There are, however, good briefcases that will provide the funding you need to continue this journey. Be wise in your choices and find your animals! Good luck!"""



    # Set column width to 80 characters
    wrapper = textwrap.TextWrapper(width=80, break_long_words=False, replace_whitespace=False)
    # Wrap text
    word_list = wrapper.wrap(text=story)



    return word_list
