# Fifa-Sniper
A Fifa 21 Sniper designed to buy players at a max price you set, and even has the option to sell the player afterwards!

# Questions & Answers
Q. Can you get banned for using this?
A. Probably. It's not my fault if you do. Although I have never got banned using it.
 
Q. How do I get my auth token?
A. Login via the web app, and use (Inspect Element > Network) or something like Fiddler to get the auth0. (It's very long) (Check authtoken example.txt)

Q. How much coins have you made?
A. ![image](https://user-images.githubusercontent.com/70807878/137012264-964a1bd7-247c-4680-977b-a16db843d8b7.png)


Note: Fifa 22 web app is out now, this code should be used just to give you a rough idea on how it was done. I am still learning, so obviously room for adjustment!

# Images :)

![Login](https://user-images.githubusercontent.com/70807878/137010816-df8c108c-f523-420f-bc14-3ef4067e037a.png)
After you input your Auth Token, you are then prompted to begin searching.

![Search](https://user-images.githubusercontent.com/70807878/137011029-edb27dac-5485-4683-ad7a-b6dcfbb29068.png)
In this case, we searched for Messi. Any player with any sort of 'Messi' in their name will display, along with their rating, but mainly the ID(player id) we need to search!

![Targetting player](https://user-images.githubusercontent.com/70807878/137011291-b1475d36-ea3d-45a3-94ba-622c85f5fa93.png)
These images are bad and old, sorry. Anyways, it then asks who you would like to snipe, in this case it was ID 200949 (which was some Silva player, I don't remember). You then set the max price you would pay for this player. Then you can finally see it begins to search, it's pretty quick too. Although you can't see it buy in this image, it keeps searching until it will find the player for $7100 or less! 

![Targetted player](https://user-images.githubusercontent.com/70807878/137011823-04c09b7b-bf0e-4fdf-839b-36ac234ef75f.png)
And boom, we managed to buy him for $6900! 


# Some other stuff
It uses a sexy players.json file I have scraped whilst using the web app. This has all the players in Fifa 21, along with their information.

Nothing else really, hope it's helpful.

I'm not responsible if you get banned. Using third-party software like this is a huge advantage and not allowed on Fifa.








