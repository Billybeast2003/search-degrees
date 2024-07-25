# Degrees of Separation
## Introduction
This project calculates the degrees of separation between two movie stars using a breadth-first search algorithm. It utilizes movie and actor data from CSV files to build a graph where nodes represent actors and edges represent shared movie appearances. The program then finds the shortest path between two actors in this graph, indicating their degree of separation.

## Requirements
- Python 3.x
- CSV files containing data about people, movies, and stars

## Setup
1. Prepare the Data:
Ensure you have the people.csv, movies.csv, and stars.csv files in a directory.
## Usage
### Running the Program
Execute the program with the directory containing your CSV files as an optional argument. If no directory is provided, it defaults to "large_dataset".

```
python degrees.py [directory]
```
Example:
```
python degrees.py data
```
## Input Actor Names
The program will prompt you to enter the names of two actors.

- If an actor's name is ambiguous (multiple actors with the same name), you will be prompted to choose the correct actor by their ID.
## Output
The program will output the degrees of separation between the two actors.

- If a connection is found, it will display the movies through which the actors are connected.
Functions and Classes

## Example
```
$ python degrees.py data
Loading data...
Data loaded.
Name: Kevin Bacon
Name: Tom Hanks
2 degrees of separation.
1: Kevin Bacon and Tom Cruise starred in A Few Good Men
2: Tom Cruise and Tom Hanks starred in The Post
```
