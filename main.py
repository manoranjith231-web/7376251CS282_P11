# P11 - Creature Index (Pokedex-style)
# Uses core Python only. No external libraries are required.

DATA_FILE = "creatures.txt"
TEAM_FILE = "team.txt"
VALID_TYPES = ["Fire", "Water", "Grass", "Electric", "Rock"]
TEAM = []


def load_creatures():
    """Read creature records from the pipe-separated text data file."""
    creatures = []
    try:
        file = open(DATA_FILE, "r", encoding="utf-8")
    except OSError:
        print("Error: creatures.txt was not found. Keep it beside main.py.")
        return creatures

    with file:
        lines = file.readlines()

    for line_number, line in enumerate(lines, 1):
        line = line.strip()
        if not line or line.startswith("#") or line.startswith("No|"):
            continue

        fields = line.split("|")
        if len(fields) != 8:
            print("Skipping invalid record on line", line_number)
            continue

        try:
            creature = {
                "no": fields[0].strip().zfill(3),
                "name": fields[1].strip(),
                "type": fields[2].strip().title(),
                "hp": int(fields[3]),
                "attack": int(fields[4]),
                "defence": int(fields[5]),
                "speed": int(fields[6]),
                "evolves_to": fields[7].strip()
            }
        except ValueError:
            print("Skipping record with invalid statistics on line", line_number)
            continue

        if creature["type"] not in VALID_TYPES:
            print("Skipping record with unknown type on line", line_number)
            continue

        creatures.append(creature)

    return creatures


CREATURES = load_creatures()


def find_creature(value):
    value = value.strip().lower()
    for creature in CREATURES:
        if creature["no"] == value.zfill(3) or creature["name"].lower() == value:
            return creature
    return None


def print_creature(creature):
    evolution = creature["evolves_to"] if creature["evolves_to"] else "None"
    print(
        creature["no"], creature["name"],
        "| Type:", creature["type"],
        "| HP:", creature["hp"],
        "| Attack:", creature["attack"],
        "| Defence:", creature["defence"],
        "| Speed:", creature["speed"],
        "| Evolves to:", evolution
    )


def view_all():
    print("\n--- ALL CREATURES ---")
    for creature in CREATURES:
        print_creature(creature)
    print("Total creatures:", len(CREATURES))


def search_creature():
    value = input("Enter creature number or name: ")
    creature = find_creature(value)
    if creature:
        print_creature(creature)
    else:
        print("Creature not found.")


def filter_by_type():
    creature_type = input("Enter type (Fire/Water/Grass/Electric/Rock): ").strip().title()
    if creature_type not in VALID_TYPES:
        print("Invalid type. Choose from:", ", ".join(VALID_TYPES))
        return

    found = False
    for creature in CREATURES:
        if creature["type"] == creature_type:
            print_creature(creature)
            found = True
    if not found:
        print("No creatures found for that type.")


def compare_creatures():
    first = find_creature(input("Enter first creature number or name: "))
    second = find_creature(input("Enter second creature number or name: "))
    if not first or not second:
        print("Creature not found. Please check the number or name.")
        return

    stats = ["hp", "attack", "defence", "speed"]
    total_first = 0
    total_second = 0
    print("\n--- STAT COMPARISON ---")
    for stat in stats:
        a = first[stat]
        b = second[stat]
        total_first += a
        total_second += b
        if a > b:
            result = first["name"] + " is higher"
        elif b > a:
            result = second["name"] + " is higher"
        else:
            result = "Tie"
        print(stat.title() + ":", first["name"], a, "|", second["name"], b, "->", result)

    print("Total:", first["name"], total_first, "|", second["name"], total_second)
    if total_first > total_second:
        print("Higher total:", first["name"])
    elif total_second > total_first:
        print("Higher total:", second["name"])
    else:
        print("Both have the same total.")


def show_evolution_chain():
    creature = find_creature(input("Enter starting creature number or name: "))
    if not creature:
        print("Creature not found.")
        return

    print("\n--- EVOLUTION CHAIN ---")
    visited = []
    while creature and creature["no"] not in visited:
        print_creature(creature)
        visited.append(creature["no"])
        next_number = creature["evolves_to"]
        if not next_number:
            break
        creature = find_creature(next_number)
    if creature and creature["no"] in visited and creature["evolves_to"]:
        print("Evolution loop detected; chain stopped.")
    elif creature is None:
        print("Next evolution record was not found.")


def type_is_effective(attacker_type, defender_type):
    return (
        (attacker_type == "Fire" and defender_type == "Grass")
        or (attacker_type == "Water" and defender_type == "Fire")
        or (attacker_type == "Grass" and defender_type == "Water")
        or (attacker_type == "Electric" and defender_type == "Water")
        or (attacker_type == "Rock" and defender_type == "Fire")
    )


def battle_creatures():
    first = find_creature(input("Enter first creature number or name: "))
    second = find_creature(input("Enter second creature number or name: "))
    if not first or not second:
        print("Creature not found. Please check the number or name.")
        return
    if first["no"] == second["no"]:
        print("Choose two different creatures.")
        return

    hp_first = first["hp"]
    hp_second = second["hp"]
    attacker_is_first = first["speed"] >= second["speed"]

    print("\nBattle:", first["name"], "vs", second["name"])
    turn = 1
    while hp_first > 0 and hp_second > 0:
        if attacker_is_first:
            attacker, defender = first, second
            defender_hp = hp_second
        else:
            attacker, defender = second, first
            defender_hp = hp_first

        damage = attacker["attack"] - (defender["defence"] // 2)
        if damage < 1:
            damage = 1

        if type_is_effective(attacker["type"], defender["type"]):
            damage *= 2
            effectiveness = " (super effective)"
        else:
            effectiveness = ""

        if attacker_is_first:
            hp_second = max(0, hp_second - damage)
            defender_hp = hp_second
        else:
            hp_first = max(0, hp_first - damage)
            defender_hp = hp_first

        print("Turn", turn, ":", attacker["name"], "attacks for", damage,
              effectiveness + ".", defender["name"], "HP:", defender_hp)

        if hp_first <= 0 or hp_second <= 0:
            break

        attacker_is_first = not attacker_is_first
        turn += 1

    if hp_first <= 0:
        print(first["name"], "fainted. Winner:", second["name"])
    else:
        print(second["name"], "fainted. Winner:", first["name"])


def save_team():
    try:
        with open(TEAM_FILE, "w", encoding="utf-8") as file:
            file.write("Team creature numbers\\n")
            for number in TEAM:
                file.write(number + "\\n")
        print("Team saved to team.txt.")
    except OSError:
        print("Could not save team.txt. Check folder permissions.")


def load_saved_team():
    """Load a previously saved team when the program starts."""
    try:
        with open(TEAM_FILE, "r", encoding="utf-8") as file:
            lines = file.readlines()
    except OSError:
        return

    for line in lines:
        number = line.strip()
        if number.isdigit():
            number = number.zfill(3)
            if find_creature(number) and number not in TEAM and len(TEAM) < 6:
                TEAM.append(number)


def manage_team():
    while True:
        print("\n--- TEAM ---")
        print("1. Add creature")
        print("2. View team")
        print("3. Save team to team.txt")
        print("4. Return to main menu")
        choice = input("Enter choice: ").strip()

        if choice == "1":
            creature = find_creature(input("Enter creature number or name: "))
            if not creature:
                print("Creature not found.")
            elif creature["no"] in TEAM:
                print("That creature is already in your team.")
            elif len(TEAM) >= 6:
                print("Team is full. Maximum is 6 creatures.")
            else:
                TEAM.append(creature["no"])
                print(creature["name"], "added to your team.")
        elif choice == "2":
            if not TEAM:
                print("Your team is empty.")
            else:
                for number in TEAM:
                    creature = find_creature(number)
                    if creature:
                        print_creature(creature)
                print("Team size:", len(TEAM), "/ 6")
        elif choice == "3":
            save_team()
        elif choice == "4":
            break
        else:
            print("Invalid choice. Enter a number from 1 to 4.")


def main():
    if not CREATURES:
        print("No creature records loaded. Check creatures.txt and restart.")
        return

    load_saved_team()
    while True:
        print("\n========== CREATURE INDEX ==========")
        print("1. View all creatures")
        print("2. Search creature")
        print("3. Filter by type")
        print("4. Compare two creatures")
        print("5. Show evolution chain")
        print("6. Battle two creatures")
        print("7. Build/view team")
        print("8. Exit")
        choice = input("Enter your choice: ").strip()

        if choice == "1":
            view_all()
        elif choice == "2":
            search_creature()
        elif choice == "3":
            filter_by_type()
        elif choice == "4":
            compare_creatures()
        elif choice == "5":
            show_evolution_chain()
        elif choice == "6":
            battle_creatures()
        elif choice == "7":
            manage_team()
        elif choice == "8":
            print("Goodbye!")
            break
        else:
            print("Invalid choice. Enter a number from 1 to 8.")


if __name__ == "__main__":
    main()
