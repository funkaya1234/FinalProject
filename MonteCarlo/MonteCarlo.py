import random
import pandas as pd
import numpy as np

class Die:
    """
    This is a class for creating the die. There are methods to be able to 
    input the faces of the die and assign weights to them. The weight of any face can be adjusted, 
    the die can be rolled a specified number of times, and the faces and weights of the die
    can be shown.
    
    The attributes include:
    - faces, a numpy array (faces of the die)
    - weights, a numpy array (weights for each face)
    - _die, a Pandas Data Frame, Dataframe of the faces and weights.
    """
    def __init__(self, faces):
        """
        Initializer for the die.

        This takes a NumPy array of faces as an argument. Throws a `TypeError` if
        not a NumPy array.

        The array’s data type `dtype` may be strings or numbers.

        The array’s values must be distinct. Tests to see if the values are
        distinct and raises a `ValueError` if not.

        Internally initializes the weights to 1.0 for each face.

        Saves both faces and weights in a private data frame with faces in
        the index.
        
        Input arguments:
        - faces, a numpy array (faces of the die)

        """
        if type(faces) == np.ndarray:
            if len(faces) != len(np.unique(faces)):
                raise ValueError("Faces must contain only unique values.")
            else:
                self.faces = faces
                self.weights = np.ones(len(faces))
                self._die = pd.DataFrame({'weight': self.weights}, index=self.faces)
        else:
            raise TypeError("Faces must be a NumPy array")
            
            
    def adjust_weight(self, face_value, adjusted_weight):
        """
        Changes the weight of a single face of the die.

        This takes two arguments: the face value whose weight is to be changed 
        and the new weight.

        Checks to see if the face passed is a valid value, i.e., if it is in 
        the die array. If not, raises an `IndexError`.

        Checks to see if the new weight is a valid type, i.e., if it is numeric 
        (integer or float) or castable as numeric. If not, raises a `TypeError`.

        Updates the weight of the specified face in the private data frame.

        Input arguments:
        - face_value, the face of the die whose weight is to be changed.
        - adjusted_weight, the new weight to assign to the face (int or float), castable as numeric.

        """
        if face_value in self._die.index:
            if type(adjusted_weight) != int and type(adjusted_weight) != float:
                try:
                    adjusted_weight = float(adjusted_weight)
                except ValueError:
                    raise TypeError("Weight must be castable as numeric (int or float)")
            self._die.loc[face_value, 'weight'] = adjusted_weight
        else:
            raise IndexError("Face value not in die")

            
    def roll_die(self, n_rolls=1):
        """
        Rolls the die one or more times.

        Takes a parameter specifying the number of times the die is to be rolled.
        Defaults to 1 roll if no parameter is provided.

        Performs a random sample with replacement from the private die data frame, 
        applying the weights of each face during sampling.

        Returns a Python list of outcomes from the rolls.

        Does not store these results internally.

        Input arguments:
        - rolls, an integer specifying the number of rolls to perform (default is 1).

        Returns:
        - A list of outcomes from the rolls. (list)
        """
        results = []
        for i in range(n_rolls):
            result = self._die.sample(weights=self._die['weight']).index[0]
            results.append(result)
        return results
    
    def show_die(self):
        """
        Shows the current state of the die.

        Returns a copy of the private die data frame, which includes 
        the faces and their corresponding weights.

        Returns:
        - A pandas DataFrame containing the current state of the die with 
          faces as the index and weights as a column.
        """
        return self._die.copy()

class Game:
    """
    This is a class for playing a game for the dice. There are methods to be able to 
    roll multiple dice together and display results in wide or narrow data frame form.
    
    Attributes:
    - dice (list of instantiated dice from die class): A collection of Die objects used in the game.
    - results (pd.DataFrame): A DataFrame storing the results of each roll.
    """
    def __init__(self, similar_dice):
        """
        Initializes a new set of dice.

        Takes a parameter specifying a list of already instantiated similar dice. 

        Input arguments:
        - dice_list, a list containing previously instantiated Die objects.

        """
        
        reference_faces = similar_dice[0].faces
        for die in similar_dice:
            if not np.array_equal(die.faces, reference_faces):
                raise ValueError("All dice must have the same faces.")

        self.dice = similar_dice

    
    
    def play(self, n_rolls):
        """
        Rolls the dice a specified number of times.

        Takes an integer parameter specifying how many times the dice should 
        be rolled. Each roll will result in a random face being selected for 
        each die in the set. The results of all rolls are saved to a private 
        data frame in wide format.

        The data frame will have the roll number as the index, columns for 
        each die (using its list index as the column name), and the face rolled 
        for that die in each roll as the corresponding cell value.

        Input arguments:
        - rolls, an integer specifying the number of rolls to perform.
        """
        results = []
        for die in self.dice:
            result = die.roll_die(n_rolls)
            results.append(result)

        self.results = pd.DataFrame(results).T
        self.results.index += 1
        self.results.index.name = "Roll"
        
        columns = []
        for i in range(len(self.results.columns)):
            columns.append("Die " + str(i + 1))
        self.results.columns = columns
            
    
    def disp_results(self, form="wide"):
        """
        Returns the results of the most recent play.

        This method returns a copy of the private play data frame to the user. 
        The data frame can be returned in either wide or narrow format, with 
        the default being wide format.

        In wide format, the data frame has the roll number as the index, 
        columns for each die (using its list index as the column name), and 
        the face rolled for that die in each roll as the corresponding cell value.

        In narrow format, the data frame will have a `MultiIndex`, comprising 
        the roll number and the die number (in that order), with a single column 
        showing the outcomes (i.e., the face rolled) for each roll.

        Input arguments:
        - form (optional), a string specifying the format to return the data frame in. 
          Can be either 'wide' or 'narrow' (default is wide).

        Returns:
        - A copy of the play data frame in the specified format (Pandas DataFrame).
        """

        if form == "wide":
            return self.results.copy()
        elif form == "narrow":
            DataFrame_narrow = self.results.stack().reset_index()
            DataFrame_narrow.columns = ["roll", "die", "outcome"]
            narrow_results = DataFrame_narrow.set_index(["roll", "die"])
            return narrow_results
        else:
            raise ValueError("Must be wide or narrow form")

class Analyzer:
    """
    This is a class for doing analysis on a game. There are methods to be able to 
    find the number of, jackpots, faces per roll, combinations, and permutations.

    Attributes:
    - game (instantiated game object from game class): The game to be analyzed.
    """
    def __init__(self, game):
        """
        Initializes the object with a Game object.

        Takes a parameter specifying a Game object. If the passed value is 
        not a Game object, a ValueError will be raised.

        Input arguments:
        - game, an object representing a Game.

        """
        if type(game) is Game:
            self.game = game
        else:
            raise ValueError("Not a Game object")

    
    def n_jackpots(self):
        """
        Computes the number of jackpots in the game.

        A jackpot is defined as a result where all faces rolled are the same, 
        for example, all ones for a six-sided die.

        This method counts how many times the game resulted in a jackpot and 
        returns the total number of jackpots.

        Returns:
        - An integer representing the number of jackpots.
        """
        n_jackpots = 0
        for roll in self.game.results.values:
            if len(set(roll)) == 1:
                n_jackpots += 1

        return n_jackpots

    
    def n_faces_per_roll(self):
        """
        Computes the count of each face value rolled in each event.

        This method calculates how many times a given face is rolled in each 
        event. For example, if a roll of five dice results in all sixes, the 
        counts for this roll would be 5 for the face value '6' and 0 for the 
        other face values.

        Returns a data frame
        - index corresponds to the roll number.
        - columns represent each possible face value.
        - values in the cells show the count of each face value rolled for each roll.

        The data frame is in wide format.

        Returns:
        - A data frame containing the counts of each face value per roll (Pandas DataFrame).
        """
        face_counts = []
        for roll in self.game.results.values:
            counts = {}
            for face in roll:
                counts[face] = counts.get(face, 0) + 1
            face_counts.append(counts)

        face_counts_df = pd.DataFrame(face_counts).fillna(0).astype(int)  # Ensure integers
        face_counts_df = face_counts_df.reindex(columns=sorted([1, 2, 3, 4, 5, 6]), fill_value=0)  # Sort columns
        face_counts_df.index = range(1, len(face_counts_df) + 1)  # Start index at 1
        face_counts_df.index.name = 'Roll Number'

        return face_counts_df



    
    def n_combinations(self):
        """
        Computes the distinct combinations of faces rolled, along with their counts.

        This method identifies all distinct combinations of faces rolled during 
        the game. The combinations are order-independent and may contain repetitions. 
        It then counts how many times each combination occurred.

        Returns a data frame
        - multiIndex where each level represents a distinct combination of faces rolled.
        - Single column showing the count of how often each combination occurred.

        Returns:
        - A data frame containing the distinct combinations and their associated counts (DataFrame).
        """

        combinations = []

        for roll in self.game.results.values:
            sorted_roll = sorted(roll)
            combinations.append(tuple(sorted_roll))

        n_combinations = {}
        for combination in combinations:
            if combination in n_combinations:
                n_combinations[combination] += 1
            else:
                n_combinations[combination] = 1

        n_combinations_df = pd.DataFrame(list(n_combinations.items()), columns=['Combination', 'Number'])
        n_combinations_df = n_combinations_df.set_index('Combination')

        return n_combinations_df



    def n_permutations(self):
        """
        Computes the distinct permutations of faces rolled, along with their counts.

        This method identifies all distinct permutations of faces rolled during 
        the game. The permutations are order-dependent and may contain repetitions. 
        It then counts how many times each permutation occurred.

        Returns a data frame
        - multiIndex where each level represents a distinct permutation of faces rolled.
        - Single column showing the count of how often each permutation occurred.

        Returns:
        - A data frame containing the distinct permutations and their associated counts (DataFrame).
        """
        permutations = []

        for roll in self.game.results.values:
            permutations.append(tuple(roll))

        n_permutations = {}
        for permutation in permutations:
            if permutation in n_permutations:
                n_permutations[permutation] += 1
            else:
                n_permutations[permutation] = 1

        n_permutations_df = pd.DataFrame(list(n_permutations.items()), columns=['Permutation', 'Count'])
        n_permutations_df = n_permutations_df.set_index('Permutation')

        return n_permutations_df


  
 
