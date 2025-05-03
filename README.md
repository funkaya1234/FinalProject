### Metadata
**Author:** Kaya Oguz
**Project Name:** Monte Carlo Simulator


### Synopsis


#### Installation
```bash
pip install monte-carlo
```

#### Usage
```python
from MonteCarlo import Die, Game, Analyzer

die1 = Die(np.array([1, 2, 3, 4, 5, 6]))
die2 = Die(np.array([1, 2, 3, 4, 5, 6]))

game = Game([die1, die2])
game.play(10)

analyzer = Analyzer(game)

face_counts = analyzer.n_faces_per_roll()
print("Face counts per roll:", face_counts)

combination_counts = analyzer.n_combinations()
print("Combination counts:", combination_counts)

```



# API Description

## 1. Die
   - Docstring: This class is for creating the die. You can input the faces of the die and assign weights to them. The weight of any face can be adjusted, the die can be rolled a specified number of times, and the faces and weights can be shown.

### Methods:
- __init__(self, faces):
   - Description: Initializes a Die object with the faces of the die.
   - Parameters:
     - faces: A numpy array representing the faces of the die. The values must be distinct.

- adjust_weight(self, face_value, adjusted_weight):
   - Description: Changes the weight of a single face of the die.
   - Parameters:
     - face_value: The face value (could be a number or string).
     - adjusted_weight: The new weight (int or float).

- roll_die(self, n_rolls=1):
   - Description: Rolls the die one or more times, considering the face weights.
   - Parameters:
     - n_rolls: An integer for how many times the die should be rolled. Defaults to 1.
   - Returns:
     - A Python list containing the outcomes of the rolls.

- show_die(self):
   - Description: Displays the current state of the die (faces and their weights).
   - Returns:
     - A Pandas DataFrame with faces as the index and weights as a column.


## 2. Game
   - Docstring: This class is for playing a dice game with multiple dice. You can roll the dice together and display the results in either wide or narrow format.

### Methods:
- __init__(self, similar_dice):
   - Description: Initializes a new set of dice for the game.
   - Parameters:
     - similar_dice: A list of already instantiated Die objects.

- play(self, n_rolls):
   - Description: Rolls the dice a specified number of times and records the results.
   - Parameters:
     - n_rolls: An integer specifying how many times the dice should be rolled.

- disp_results(self, form=wide):
   - Description: Displays the results of the most recent play.
   - Parameters:
     - form: A string specifying the format to return the data frame in. Can be either wide or narrow. Defaults to wide.
   - Returns:
     - A Pandas DataFrame with the results of the rolls in the specified format (wide or narrow).


## 3. Analyzer
   - Docstring: This class is for analysis on a game. It includes methods for finding the number of jackpots, faces per roll, combinations, and permutations.

### Methods:
- __init__(self, game):
   - Description: Initializes the object with a Game object.
   - Parameters:
     - game: An object representing the Game. This must be an instantiated Game object.

- n_jackpots(self):
   - Description: Computes the number of jackpots in the game. A jackpot is a result where all faces rolled are the same.
   - Returns:
     - An integer representing the number of jackpots.

- n_faces_per_roll(self):
   - Description: Computes the count of each face value rolled in each event.
   - Returns:
     - A Pandas DataFrame in wide format with the roll number as the index, columns for each possible face value, and values showing the count of each face value rolled.

- n_combinations(self):
   - Description: Computes the distinct combinations of faces rolled, along with their counts.
   - Returns:
     - A Pandas DataFrame with a MultiIndex where each level represents a combination of faces rolled, and a column showing the count of how often each combination occurred.

- n_permutations(self):
   - Description: Computes the distinct permutations of faces rolled, along with their counts.
   - Returns:
     - A Pandas DataFrame with a MultiIndex where each level represents a permutation of faces rolled, and a column showing the count of how often each permutation occurred.


## Attributes:
- **Analyzer**:
  - game: The Game object passed during initialization to be analyzed.

- **Die**:
  - faces: A numpy array containing the faces of the die.
  - weights: A numpy array for the weights for each face.
  - _die: A Pandas DataFrame containing the faces and their weights.

- **Game**:
  - dice: A list of Die objects used in the game.
  - results: A Pandas DataFrame storing the results of each roll (in wide format).
