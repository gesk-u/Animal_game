# Animal_game
Software 1. Group project
### Story
You are a zookeeper from Happy Animals Zoo, and your endangered animals have been taken by a villainous mob boss named Matti, who has taken the animals to the airport to sell and distribute them to new and prospective owners all in very short time. 

But while boarding Matti's private jet, the animals escaped their pens and have now been taken to random airports. 
Matti also dropped his list of private airports where his jet frequently stops to refuel. 
     
You have pursued and followed Matti to the airport and saw this happening from afar; however, after Matti's jet has taken off, you step on a piece of paper which, upon closer inspection, is revealed to be Matti's private airport list. 
    
Armed with this list and some money, you start off on your animal adventure, where you will rescue and reclaim the endangered animals from your zoo. 
    
Your task is to first select an airport where you will start. Along this journey, you will need luck, grit, and sisu to help find the animals. 
You might come across briefcases left behind by Matti's assistants. Avoid them at all costs if you want to find animals as fast as possible but mind your resources. There are, however, good briefcases that will provide the funding you need to continue this journey. Be wise in your choices and find your animals! Good luck!

### Your Mission

* Choose an airport from Matti’s list to begin your journey.

* Search airports to find your missing animals before Matti.

* Be careful: you might stumble upon briefcases:

    - Some are traps that waste your time.

    - Others contain cash that can help you continue your mission.

Manage your resources wisely — travel costs money, and time is running out

### Hint System

If you ever get stuck, you can buy a hint using your zoo funds.
Each hint will reveal two random letters from the airport code where one of your animals is currently located.

### Your Adventure Begins

You stand at the edge of the runway, Matti’s airport list in hand.
The engines of his jet roar in the distance, fading into the clouds.
Now it’s up to you.

Choose your starting airport from Matti’s secret list, and let the chase begin...

## Database

1. This game uses the airport table from the database course.
2. The following tables were created:
   ```sql
    create table game(
    id int(11) auto_increment 
    	primary key,
    screen_name varchar(40),
    money int,
    player_range int,
    location varchar(40),
    turn_time int
    );
   ```
   ```sql
   create table animals(
   id int(11) auto_increment 
	 primary key,
   name varchar(40),
   description text
   );
   INSERT INTO animals (name, description) VALUES
    ('Black-footed ferret', 'the only North American ferret, once thought extinct, now back to sneak around in tiny socks.'),
    ('White-throated robin', 'a flashy migratory bird that winters in Africa, looking like it’s always ready for karaoke night.'),
    ('Long-tailed tree mouse', 'a rare Indonesian rodent with a tail longer than its body, basically a mouse with built-in jump rope.'),
    ('Pygmy hippopotamus', 'a shy, forest-dwelling hippo from West Africa that looks like a hippo someone left in the dryer too long.'),
    ('Timber rattlesnake', 'a venomous snake of U.S. forests that warns you with tail percussion, basically nature’s “keep back” sign.'),
    ('Short-eared dog', 'a rare Amazonian canid that looks permanently unimpressed, probably because you thought it was a fox.'),
    ('Cuban greater funnel-eared bat', 'endemic to Cuba, it has huge ears for sonar, and honestly looks like it’s trying to pick up Wi-Fi.'),
    ('Purple frog', 'an Indian frog that spends 11 months underground, coming out just to breed, like the introvert of the amphibian world.'),
    ('Andean flamingo', 'one of the rarest flamingos, feeding on tiny algae at high-altitude lakes, basically a ballerina with a filter-feeding habit.'),
    ('Andean bear', 'the only South American bear, known for its shaggy fur and eye-mask markings, like a panda who switched to goth.'),
    ('Desert warthog', 'a wild pig with giant facial warts that lives in dry Africa, kind of like a hog wearing lumpy armor.'),
    ('Angel’s chameleon', 'a tiny, leaf-shaped chameleon from Madagascar that looks like it’s playing hide-and-seek against actual leaves.'),
    ('Pygmy three-toed sloth', 'the slowest of the already slow sloths, found only on one Panamanian island, moving like it’s buffering in real life.'),
    ('Proboscis monkey', 'a big-nosed monkey from Borneo whose honker helps it attract mates, proving size really does matter (for noses).'),
    ('Loggerhead turtle', 'a massive sea turtle with a jaw strong enough to crush crabs, basically the nutcracker of the ocean.'),
    ('Snow leopard', 'a mountain-dwelling cat with thick spotted fur and a tail longer than your arm, also known as the “ghost of the mountains.”'),
    ('Wild camel', 'the only truly wild camel species, surviving China and Mongolia’s deserts, drinking water saltier than seawater like it’s fine wine.'),
    ('Tasmanian devil', 'a carnivorous marsupial with a scream like a horror soundtrack, but actually helps clean up carcasses like nature’s janitor.'),
    ('Siamese crocodile', 'a critically endangered crocodile from Southeast Asia, often mistaken for logs until it moves — surprise!'),
    ('Platypus', 'an egg-laying mammal with a duck bill, beaver tail, and venomous spur, proving Mother Nature has a sense of humor and a dark side.');
   ```
   ```sql
   create table items(
   id int(11) auto_increment 
     	primary key,
   name varchar(40),
   price int,
   quantity int
   );
   insert into items(name, price, quantity)
   values ("plastic", 125, 4),
          ("canvas", 150, 2),
          ("nylon", 175, 2),
          ("metal", 200, 1),
          ("leather", 300, 1);
   ```
   ```sql
   create table located_items(
   id int(11) auto_increment
	    primary key, 
   item_id int(11),
   game_id int(11),
   location varchar(40),
   opened tinyint(1) default 0
   );
   ```
   ```sql
   create table located_animals(
   id int(11) auto_increment
	    primary key, 
   animal_id int(11),
   game_id int(11),
   location varchar(40),
   rescued tinyint(1) default 0
   );
   ```
   ```sql
    CREATE TABLE rescued_animals (
      game_id INT,
      animal_id INT,
      PRIMARY KEY (game_id, animal_id),
      FOREIGN KEY (game_id) REFERENCES game(id),
      FOREIGN KEY (animal_id) REFERENCES animals(id)
    );
   ```



