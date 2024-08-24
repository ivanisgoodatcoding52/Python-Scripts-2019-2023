import random

class Character:
    def __init__(self, name, health, attack, defense):
        self.name = name
        self.health = health
        self.attack = attack
        self.defense = defense

    def take_damage(self, damage):
        self.health -= damage

    def attack_target(self, target):
        damage = random.randint(1, self.attack)
        target.take_damage(damage)
        print(f"{self.name} attacks {target.name} for {damage} damage.")

    def use_item(self, item):
        if item == "health_potion":
            heal_amount = random.randint(10, 20)
            self.health += heal_amount
            print(f"{self.name} uses a health potion and heals for {heal_amount} HP.")
        else:
            print(f"{self.name} doesn't know how to use {item}.")

def main():
    # Create characters
    player = Character("Player", 100, 20, 10)
    enemy = Character("Enemy", 50, 15, 5)

    print("A wild enemy appears!")

    while player.health > 0 and enemy.health > 0:
        print("\nPlayer Stats:")
        print(f"Health: {player.health}")
        print("\nOptions:")
        print("1. Attack")
        print("2. Use Item")
        print("3. Run")

        choice = input("Enter your choice (1/2/3): ")

        if choice == '1':
            player.attack_target(enemy)
        elif choice == '2':
            item = input("Enter the item you want to use (health_potion): ")
            player.use_item(item)
        elif choice == '3':
            escape_chance = random.random()
            if escape_chance > 0.5:
                print("You successfully ran away!")
                break
            else:
                print("You failed to run away. The enemy attacks you!")
                enemy.attack_target(player)
        else:
            print("Invalid choice. Try again.")

        # Enemy's turn to attack
        if enemy.health > 0:
            enemy.attack_target(player)

    # Determine the winner
    if player.health > 0:
        print("You defeated the enemy! Victory!")
    else:
        print("You were defeated by the enemy. Game Over.")

if __name__ == "__main__":
    main()
