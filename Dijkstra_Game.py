# Core Algorithm: Dijkstra Algorithm
#   Details: White nodes: haven't been recorded in heapdict
#            Grey nodes: in heapdict
#            Black nodes: already popped from heapdict

# Game Rules:
# 1) You have an initial bank which shows how much money you have for now, and you are at an initial place
# 2) Each round, you get a destination which you have to go, and there is a reward for you when you reach the destination
# 3) When you reach the destination, your money will be deducted 1 dollors for 1 unit distance you travel from the last place
# 4) Of course, at the same time, you get the reward
# 5) *** ! *** Each round, you can purchase a magic tool that can show you the shortest path to travel from current place to the destination
# 6) If you have negative money which means you are bankrupt, and the game ends.
# 7) Your goal: follow the shotest path, cost less money, and get the reward

from random import randint
from collections import defaultdict
from heapdict import heapdict # pip3 install heapdict

class Game:
    def __init__(self, name, bank, places, edges):
        self.name = name
        self.bank = bank
        self.places = places
        self.edges = edges
        self.magic_tool_price = bank/3
        self.d = defaultdict(list)
        for u,v,cost in edges:
            self.d[u].append((v,cost))
            self.d[v].append((u,cost))

    def get_reward(self): # generate a random reward
        all_distance = [c for a,b,c in self.edges]
        mini,maxi = min(all_distance),max(all_distance)
        return randint(mini*3,maxi*3)

    def get_destination(self,current_place):
        destination = self.places[randint(0,len(self.places)-1)]
        while destination == current_place:
            destination = self.places[randint(0,len(self.places)-1)]
        return destination

    def show_and_make_choice(self,current_place):
        print("According to your current location, these places you can travel to next: \n")
        print(self.d[current_place])
        choices = {} # place: cost
        for a,b in self.d[current_place]:
            choices[a] = b
        inp = input("please make a choice:")
        while inp not in choices:
            inp = input("please make a choice where you can travel to: \n")
        self.bank-=choices[inp]
        print("You have made it to " + inp + ", now your bank has " + str(self.bank) + " left!")
        return inp


    def purchase_magic_tool(self,current_place,destination):
        print("Now you have a chance to purchase a magic tool, now you have " + str(self.bank) + " in your bank, and the magic tool price is " + str(self.magic_tool_price) + "\n")
        inp = input("press 'y' to purchase, press any other buttons to skip \n")
        if inp == 'y' and self.bank >= self.magic_tool_price:
            self.bank -= self.magic_tool_price
            return self.get_shortest(current_place,destination)
        return ["Fail to purchase, Good Luck"]

    def get_shortest(self,current_place,destination):
        h = heapdict() # * priority queue + dictionary: h[place] = current shortest cost from origin to here (but you can update shortest cost later)
        h[current_place] = 0
        path = {}
        popped = set()
        while h:
            v,shortest_cost = h.popitem()
            popped.add(v) # put v in black node list
            if v == destination:
                return self.get_solution_path(path,current_place,v)
            for u,cost in self.d[v]:
                newd = shortest_cost + cost
                if u not in popped and (u not in h or h[u] > newd): # put u in grey node list
                    h[u] = newd
                    path[u] = v # now comes from u can get the current shortest cost at v
        return None

    def get_solution_path(self,path,current_place,v): # backtracking the path
        if v == current_place:
            return [current_place]
        return self.get_solution_path(path,current_place,path[v]) + [v]

    def game_start(self):
        exit = False
        current_place = self.places[randint(0,len(self.places)-1)] # pick a random place to start
        while self.bank >= 0 and not exit:
            reward = self.get_reward()
            destination = self.get_destination(current_place)
            print("Here is your reward if you make it to destination: " + str(reward))
            print("Here is your current location: " + current_place)
            print("Here is your destination for this round: " + destination)
            print(self.purchase_magic_tool(current_place,destination))
            print("Now start your travel!\n")
            while current_place != destination:
                current_place = self.show_and_make_choice(current_place)
                if self.bank < 0:
                    print("Oops, you are bankrupt now, game ends!")
                    exit = True
                    break
            if exit:
                break
            self.bank+=reward
            print("Oh you make it to the destination! Here you are the reward! Now you have $",self.bank," in your bank \n")
            inp = input("still wanna keep going? press 'y' to keep going, any other buttons to end the game \n")
            if inp != 'y':
                break

if __name__ == "__main__":
    name = input("please enter your name \n")
    places = ["LosAngeles","Chicago","NewYork","Miami","Seattle","Austin","Denver"]
    edges = [["LosAngeles","Chicago",100],["LosAngeles","NewYork",300],["Chicago","NewYork",150],["NewYork","Miami",500],["Seattle","Miami",50],["NewYork","Seattle",250],["Austin","Seattle",80],["Austin","Denver",70],["Miami","Denver",30]]
    game = Game(name,1000,places,edges)
    game.game_start()
