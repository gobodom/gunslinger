import cmd, math, random

def plural(number, name):
    if number > 1:
        name += 's'
    return str(number) + ' ' + name

class Whatever(cmd.Cmd):
  
    def __init__(self):
        super().__init__()
        self.pistol1 = Gun("pistol", ".22 bullet", 6, 6, 50)
        self.pistol2 = Gun("pistol", ".38 bullet", 6, 6, 100)
        self.you = Human("Chud")
        self.enemy = Human("Bud")
        self.you.get_gun(self.pistol1)
        self.enemy.get_gun(self.pistol2)

    def check_gun(self):
        print("Your gun has {} bullets.".format(self.you.gun.ammo_number))

    def do_check(self, line):
        self.check_gun()

    def do_quit(self, line):
  	    '''quit 
  	    quits'''
  	    return True

    def do_attack(self, line):
        if self.enemy.is_alive():
            result = self.you.attack(self.enemy)
            if result == -2:
                print("Your " + self.you.gun.name + " misfired.")
            elif result == -1:
                print("Your {} is out of bullets.".format(self.you.gun.name))
            elif result == 0:
                print("Bang! You fire your {} at {} but miss.".format(self.you.gun.name, self.enemy.name))
                self.check_gun()
            else: 
                print("Bang! You fire your {} at {} and hit him.".format(self.you.gun.name, self.enemy.name))
                self.enemy.wound(result)
                self.check_gun()
            if self.enemy.is_alive():
                result = self.enemy.attack(self.you)
                if result == -2:
                    print("{}'s {} misfired.".format(self.enemy.name, self.enemy.gun.name))
                elif result == -1:
                    if self.enemy.bullets > 0:
                        print("{} reloads his {}".format(self.enemy.name, self.enemy.gun.name))
                        available = self.enemy.bullets
                        self.enemy.bullets = available - self.enemy.gun.load(available)
                    else:
                       print("{}'s {} is out of bullets.".format(self.enemy.name, self.enemy.gun.name))
                elif result == 0:
                    print("Bang! {} fires his {} at you but misses.".format(self.enemy.name, self.enemy.gun.name))
                else:
                    print("Bang! {} fires his {} at you and hits.".format(self.enemy.name, self.enemy.gun.name))
                    self.you.wound(result)
                    if not self.you.is_alive():
                        print("You die.")
                        return True
            else:
                print("{} dies.".format(self.enemy.name))
        else:
            print("{} is already dead.".format(self.enemy.name))
 
        
    def do_practice(self, line):
        if self.you.gun.ammo_number == 0:
            print("You practic drawing your {}.".format(self.you.gun.name))
        else:
            self.you.gun.fire()
            self.you.skill_guns.practice()
            print("You practice drawing and shooting your {}.".format(self.you.gun.name))
        self.you.skill_fastdraw.practice() 
        self.check_gun()

    def do_load(self, line):
        num_loaded = self.you.gun.load(self.you.bullets)
        self.you.bullets -= num_loaded
        print("You load {} into your {}".format(plural(num_loaded, self.you.gun.ammo_type), self.you.gun.name))
        self.check_gun()
        


class Gun(object):
    def __init__(self, style, ammo_type, ammo_number, ammo_capacity, distance):
        self.name = ammo_type + " " + style
        self.style = style
        self.ammo_type = ammo_type
        self.ammo_number = ammo_number
        self.ammo_capacity = ammo_capacity
        self.distance = distance

    def fire(self):
        if (self.ammo_number == 0):          
            return -1
        else: 
            self.ammo_number -= 1
            return 1

    def load(self, available):
        bullets = self.ammo_capacity - self.ammo_number
        if bullets > available:
            bullets = available
        self.ammo_number += bullets
        return bullets


class Skill(object):
    def __init__(self, name):
        self.name = name
        self.theory = 0
        self.xp = 0

    def rank(self):
        return math.log10(self.xp+1) + math.log10(self.theory+1)

    def addxp(self, amount):
        self.xp += amount

    def check(self, difficulty):
        result = self.rank() - difficulty + random.gauss(0,1)
        if result < 0:
            result = 0
        self.addxp(difficulty)
        return result

    def practice(self):
        self.addxp(1)

class Human(object):
    def __init__(self, name):
        self.name = name
        self.health = 100
        self.skill_guns = Skill("Guns")
        self.skill_fastdraw = Skill("Fastdraw")
        
    def wound(self, amount):
        self.health -= amount
        print(self.health)

    def heal(self, amount):
        self.health = self.health + amount
        if self.health > 100:
            self.health = 100

    def get_gun(self, gun):
        self.gun = gun
        self.bullets = 6

    def is_alive(self):
        return self.health > 0

    def attack(self, target):
        result = self.gun.fire()
        if result == 1:
            result = (self.skill_guns.check(1)) * 100
        return result
        
if __name__ == '__main__':
    Whatever().cmdloop()
    while True:
        {}
