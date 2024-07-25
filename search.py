import csv
import sys


# Maps names to a set of corresponding person_ids
names = {}
# Maps person_ids to a dictionary of: name, birth, movies (a set of movie_ids)
people = {}
# Maps movie_ids to a dictionary of: title, year, stars (a set of person_ids)
movies = {}
class Node:
    def __init__(self, state, parent = None, action = None) -> None:
        self.state = state
        self.parent = parent
        self.action = action
        
class StackFrontier():
    def __init__(self):
        self.frontier = []
        
    def add(self, node):
        self.frontier.append(node)
        
    def contains_state(self, state):
        return any(node.state == state for node in self.frontier)

    def empty(self):
        return len(self.frontier) == 0

    def remove(self):
        if self.empty():
            raise Exception("empty frontier")
        else:
            node = self.frontier[-1]
            self.frontier = self.frontier[:-1]
            return node
        
class QueueFrontier(StackFrontier):
    def remove(self):
        if self.empty():
            raise Exception("empty frontier")
        else:
            node = self.frontier[0]
            self.frontier = self.frontier[1:]
            return node
        
def load_data(data_dir):
    """
    Load data from CSV files into memory.
    """
    # Load people
    with open(f"{data_dir}/people.csv", encoding="utf-8") as f:
        reader = csv.DictReader(f)
        for row in reader:
            people[row["id"]] = {
                "name": row["name"],
                "birth": row["birth"],
                "movies": set()
            }
            # Add to names
            if row["name"].lower() not in names:
                names[row["name"].lower()] = { row["id"] }
            else:
                names[row["name"].lower()].add(row["id"])

    # Load movies
    with open(f"{data_dir}/movies.csv", encoding="utf-8") as f:
        reader = csv.DictReader(f)
        for row in reader:
            movies[row["id"]] = {
                "title": row["title"],
                "year": row["year"],
                "stars": set()
            }

    # Load stars
    with open(f"{data_dir}/stars.csv", encoding="utf-8") as f:
        reader = csv.DictReader(f)
        for row in reader:
            try:
                people[row["person_id"]]["movies"].add(row["movie_id"])
                movies[row["movie_id"]]["stars"].add(row["person_id"])
            except KeyError:
                pass
            
            
def shortest_path(source: int, target: int):
    """
    Returns the shortest list of (movie_id, person_id) pairs that connect the person with id source to the person with id target.

    If no possible path, returns None.
    """

    node = Node(state=source) # state: person_id, action: movie_id
    explored = set() # set of person_id

    frontier = QueueFrontier()
    frontier.add(node)

    while (not frontier.empty()):
        node = frontier.remove()
        explored.add(node.state)

        for action, state in neighbors_for_person(node.state):
            if not frontier.contains_state(state) and state not in explored:
                child = Node(state, node, action)
                frontier.add(child)

                if (child.state == target):
                    return recover(child)

    return None

def recover(node: Node):
    """
    Returns the nodes as a list of (action, state)
    """
    solution = []
    while (node.parent is not None):
        solution.append((node.action, node.state))
        node = node.parent
    solution.reverse()
    return solution


def person_id_for_name(name):
    """
    Returns the IMDB id for a person's name, resolving ambiguities as needed.
    """
    person_ids = list(names.get(name.lower(), set()))
    if len(person_ids) == 0:
        return None
    elif len(person_ids) > 1:
        print(f"Which '{name}'?")
        for person_id in person_ids:
            person = people[person_id]
            name = person["name"]
            birth = person["birth"]
            print(f"ID: {person_id}, Name: {name}, Birth: {birth}")
        try:
            person_id = input("Intended Person ID: ")
            if person_id in person_ids:
                return person_id
        except ValueError:
            pass
        return None
    else:
        return person_ids[0]


def neighbors_for_person(person_id):
    """
    Returns a set of (movie_id, person_id) pairs for people who starred with a given person_id.
    """
    movie_ids = people[person_id]["movies"]
    neighbors = set()
    for movie_id in movie_ids:
        for person_id in movies[movie_id]["stars"]:
            neighbors.add((movie_id, person_id))
    return neighbors

def main():
    if len(sys.argv) > 2: sys.exit("Usage: python degrees.py [directory]")
    directory = sys.argv[1] if len(sys.argv) == 2 else "large"

    # Load data from files into memory
    print("Loading data...")
    load_data(directory)
    print("Data loaded.")

    source = person_id_for_name(input("Name: "))
    if source is None:
        sys.exit("Person not found.")
    target = person_id_for_name(input("Name: "))
    if target is None:
        sys.exit("Person not found.")

    path = shortest_path(source, target)

    if path is None:
        print("Not connected.")
    else:
        degrees = len(path)
        print(f"{degrees} degrees of separation.")
        path = [(None, source)] + path
        for i in range(degrees):
            person1 = people[path[i][1]]["name"]
            person2 = people[path[i+1][1]]["name"]
            movie = movies[path[i+1][0]]["title"]
            print(f"{i + 1}: {person1} and {person2} starred in {movie}")
            
if __name__ == "__main__":
    main()