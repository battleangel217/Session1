import os
import django
import random, time
import django.db
from django.db.models import Max, Min

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'session1.settings')
django.setup()

from games.models import Room, Player

class MafiaVoteout():
    def __init__(self, code_no=0, username=''):
        self.code_no = code_no
        self.username = username

    
    #The menu method
    def menu(self):
        print("MAIN MENU\n1.) Create room\n2.) Join room\n\n")
        try:
            option = int(input(">"))
        except ValueError:
            print("Please enter the correct option")
            self.menu()
        if option == 1:
            self.create_room()
        elif option == 2:
            self.join_room()
        else:
            print("Please choose a valid option!!")
            self.menu()

        
    #A method that enables users to creates a room
    def create_room(self):
        self.username = input("Username: ")
        
        #Generates a random 6-digit room code 
        self.code_no = random.randint(100000, 999999)
        try:
            Room.objects.create(name = self.username ,code = self.code_no)
        except django.db.utils.IntegrityError:
            print("A room with that username already exists")
            self.create_room()

        print("ROOM CODE CREATED SUCCESSFULLY")

        #Automatically adds player to the room he just created
        Player.objects.create(username=self.username, room_id=self.code_no)
        self.lobby1()


    #A method that enables users to join a room
    def join_room(self):
        self.username = input("Username: ")
        print("Please enter the room code of the game you want to join")
        try:
            self.code_no = int(input("> "))
        except ValueError:
            print("Invalid option\nPlease enter either option 1 or 2")
            self.join_room()


        rooms = Room.objects.all()

        #Iterates to check if the game has started or not. Players can't join an ongoing match
        for i in rooms:
            if i.code == self.code_no:
                if i.started != "Closed":
                    print(f"You joined {i.name} room\n\n")
                    Player.objects.create(username=self.username, room_id=self.code_no)
                    self.lobby2()
                    return
                else:
                    print("Game room has already started!")
                    self.join_room()
                    return
        
        print('Room not found')
        self.join_room()
        

    #A lobby for only the admin
    def lobby1(self):
        
        #Filter only players in the room and counts them
        complete = Player.objects.filter(room_id=self.code_no).count()
        print(f"ROOM CODE: {self.code_no}")
        print("Waiting for players(minimum of 3 player)...")
        n = complete

        #A loop that checks if they are up to 3 players and updates the players that a joining till they are up to three
        while complete < 3:
            complete = Player.objects.filter(room_id=self.code_no).count()

            #Checks if the number of players present are the same as the pervious number when the loop last ran
            if n != complete:

                #Filters players between the previous number of players and the current
                new = Player.objects.filter(room_id=self.code_no).order_by('id')[n:complete]
                for i in new:
                    print(f"{i.username} joined")
                
                #Asigns a new value for n
                n = complete

            #Wait one second to avoid overworking the cpu. n\b: Without this the loop runs as fast as the pc cpu
            time.sleep(1)
        
        print("Press any key to start")
        input()

        #Updates the room status to close so no more players can join
        room_status = Room.objects.get(code=self.code_no)
        room_status.started = "Closed"
        room_status.save()

        #Filters the players in the room
        players = Player.objects.filter(room_id=self.code_no)

        #Gets the id of the first and last players present in the room
        first = players.order_by('id').first().id
        last = players.order_by('-id').first().id

        #Chooses a random number from the first to the last id and assigns the player as the mafia
        chosen = random.randint(first, last)
        mafia_chosen = Player.objects.get(id = chosen)
        mafia_chosen.status="Mafia"
        mafia_chosen.save()
        self.game()


    #Lobby for the players that joined
    def lobby2(self):
        complete = Player.objects.count()
        start = Room.objects.get(code = self.code_no).started


        n = complete
        print(f"ROOM CODE: {self.code_no}")
        print("Waiting for players to join")

        #Go and read the comments in lobby1
        for i in Player.objects.filter(room_id=self.code_no):
            if i.username == self.username:
                print("You joined")
                continue
            print(f"{i.username} joined")

        #Continuously updates players that joining till the admin starts the game
        while start == "Open":
            complete = Player.objects.filter(room_id=self.code_no).count()
            if n != complete:
                new = Player.objects.filter(room_id=self.code_no).order_by('id')[n:complete]
                for i in new:
                    print(f"{i.username} joined")

                n = complete
            start = Room.objects.get(code = self.code_no).started
            time.sleep(1)

        self.game()
        return
        

    #A method that commences the whole game
    def game(self):
        players = Player.objects.filter(room_id=self.code_no)
        print("\n\nThe mafia is being choosen...")        

        if players.get(status="Mafia").username == self.username:
            print("You are now the mafia. Survive to win 🔥")
        else:
            print("The mafia is among you. Good luck eliminating him")



        #Begin the voting rounds and checks of they are up to 2 players still available. If not the game ends and the mafia wins
        while True:
            current_room = Room.objects.get(code=self.code_no)
            current_room.done_voting = "False"
            current_room.save()
            players = Player.objects.filter(room_id=self.code_no)

            #Resets all the votes and submitted status
            for i in players:
                i.vote = 0
                i.save()
            players = Player.objects.filter(room_id=self.code_no)

            for i in players:
                i.submitted="False"
                i.save()

            #The main voting starts
            while current_room.done_voting == "False":
                current_room = Room.objects.get(code=self.code_no)

                #Filters the players that have not yet voted
                players_yet_to_vote = players.filter(submitted="False")
                for i in players_yet_to_vote:
                    if i.username == self.username:
                        print("\n\nIt's voting time. Here are all the players, enter the numeber of who you think is the mafia.")

                        #Print the players in the room
                        for i in players:
                            print(f"{i.id}.) {i.username}")
                        
                        try:
                            playersvote = int(input("Vote: "))
                        except ValueError:
                            print("Please enter a number from the onces above")
                            self.game()
                            
                        print(f"You voted for {players.get(id=playersvote).username} as the mafia")
                        lose = players.get(id=playersvote)
                        lose.vote += 1
                        lose.save()
                        
                        print("waiting for all players to finish voting...\nHope you don't get eliminated")

                #Changes your status to someone that has voted
                done = Player.objects.get(username=self.username)
                done.submitted = "True"
                done.save()
                n=0
                players_yet_to_vote = players.filter(submitted="False")

                #Checks if the are players that have not voted
                for i in players_yet_to_vote:
                    if i.submitted == "False":
                        n+=1
                    else:
                        pass
                if n == 0:
                    current_room.done_voting = "True"
                    current_room.save()
                else:
                    time.sleep(1)


            time.sleep(2)
            players = Player.objects.filter(room_id=self.code_no)
            print("\n\nHere is the vote count")
            for i in players:
                print(f"{i.username}: {i.vote}")

            #Gets the player with the highest vote count
            out = players.aggregate(Max('vote'))['vote__max']
            losers = players.filter(vote=out)

            #Checks if there is a tie
            if losers.count() > 1:
                print("The vote resulted in a tie")
            else:
                #Else eliminate the player with the highest value
                for i in losers:
                    if i.username == self.username:
                        print("You have been eliminated")
                        time.sleep(3)
                        i.delete()
                        exit()
                        
                    else:
                        print(f"{i.username} has been eliminated")
                        time.sleep(5)


                #Checks if the mafia still exist
                if players.filter(status="Mafia").exists():
                    print("That was not the mafia. 😂😂")
                else:
                    #Ends game if the mafia has been eliminated
                    print("You guys eliminated the mafia!! You winn")
                    Room.objects.get(code=self.code_no).delete()
                    exit()

                #Game ends if they are only 2 players left
                players = Player.objects.filter(room_id=self.code_no)
                if players.count() == 2:
                    if players.get(status="Mafia").username == self.username:
                        print("You win! 🎉🎊")
                        if players.first() == self.username:
                            Room.objects.get(code=self.code_no).delete()
                        exit()
                    else:
                        print(f"{players.get(status="Mafia").username} was the mafia! 😂\nYou lose")
                        exit()
                




begin = MafiaVoteout()
begin.menu()            

        