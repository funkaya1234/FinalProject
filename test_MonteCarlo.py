import unittest
import numpy as np
import pandas as pd
from MonteCarlo import Die, Game, Analyzer

class TestDie(unittest.TestCase):
    
    def test_initialization(self):
        """
        Tests the initialization of a Die object.

        This test checks the creation of a Die object with valid and invalid input faces. 
        - For valid faces, it ensures the weights are initialized to 1 
          and the internal die representation is a DataFrame with the faces as the index.
        - For duplicate faces, a ValueError should be raised.
        - For face types that are not numpy arrays, a TypeError should be raised.
        """
        faces = np.array([1, 2, 3, 4, 5, 6])
        die = Die(faces)
        self.assertTrue(np.array_equal(die.weights, np.ones(len(faces))))
        self.assertIsInstance(die._die, pd.DataFrame)
        self.assertTrue(np.array_equal(die._die.index, faces))
        
        faces = np.array([1, 2, 3, 3, 5, 6])
        with self.assertRaises(ValueError):
            Die(faces)
    
        faces = [1, 2, 3, 4, 5, 6]
        with self.assertRaises(TypeError):
            Die(faces)
    
    def test_adjust_weight(self):
        """
        Tests the adjustment of a die's face weights.

        This test checks that the `adjust_weight` method updates the weight for a specific face. 
        It also ensures that invalid indices or incorrect weight types raise appropriate exceptions.
        - For adjusted weights that are not int or float or not castable as numeric, a TypeError should be raised.
        - For adjusting a weight that is not in the faces, an IndexError should be raised.
        """
        faces = np.array([1, 2, 3, 4, 5, 6])
        die = Die(faces)
        die.adjust_weight(1, 2)
        self.assertEqual(die._die.loc[1, 'weight'], 2)
        
        faces = np.array([1, 2, 3, 4, 5, 6])
        die = Die(faces)
        
        with self.assertRaises(IndexError):
            die.adjust_weight(7, 2)
    
        faces = np.array([1, 2, 3, 4, 5, 6])
        die = Die(faces)
        with self.assertRaises(TypeError):
            die.adjust_weight(1, "An Incorrect weight (not int or float, not castable as numeric)")
    
    def test_roll_die(self):
        """
        Tests the rolling of the die.

        This test verifies that the roll_die method returns a valid result. The results of multiple rolls 
        should always be one of the faces on the die. When calling the function, the default should be one roll.
        """
        faces = np.array([1, 2, 3, 4, 5, 6])
        die = Die(faces)

        results = die.roll_die(10)
        self.assertTrue(all(result in faces for result in results))
        
        result = die.roll_die()  
        self.assertEqual(len(result), 1)
        self.assertEqual(type(result), list)

    
    def test_show_die(self):
        """
        Tests the display of the die's state.

        This test checks that the showdie method returns the current state of the die as a DataFrame. 
        The index of the DataFrame should correspond to the die faces, and the weight column should 
        contain the initial weight values.
        """
        faces = np.array([1, 2, 3, 4, 5, 6])
        die = Die(faces)
        die_state = die.show_die()
        self.assertIsInstance(die_state, pd.DataFrame)
        self.assertTrue(np.array_equal(die_state.index, faces))
        self.assertTrue(np.array_equal(die_state['weight'], np.ones(len(faces))))


class TestGame(unittest.TestCase):
    
    def test_initialization(self):
        """
        Tests the initialization of the Game class.
        
        Verifies that the Game object correctly initializes with the provided dice
        and ensures that the faces of the dice match the expected values.
        Also tests the case where the dice have mismatched faces, which should raise a ValueError.
        """
        faces = np.array([1, 2, 3, 4, 5, 6])
        die1 = Die(faces)
        die2 = Die(faces)
        game = Game([die1, die2])
        self.assertEqual(len(game.dice), 2)
        self.assertTrue(np.array_equal(game.dice[0].faces, faces))
        self.assertTrue(np.array_equal(game.dice[1].faces, faces))
    
        faces1 = np.array([1, 2, 3, 4, 5, 6])
        faces2 = np.array([1, 2, 3, 4, 7, 8])
        die1 = Die(faces1)
        die2 = Die(faces2)
        with self.assertRaises(ValueError):
            Game([die1, die2])
    
    def test_play(self):
        """
        Tests the play method of the Game class.
        
        Verifies that after calling the play method, the results are stored in a pandas DataFrame.
        Ensures that the number of rolls corresponds to the specified number of rolls.
        """
        faces = np.array([1, 2, 3, 4, 5, 6])
        die1 = Die(faces)
        die2 = Die(faces)
        game = Game([die1, die2])
        game.play(5)
        self.assertIsInstance(game.results, pd.DataFrame)
        self.assertEqual(len(game.results), 5)
    
    def test_disp_results(self):
        """
        Tests the disp_results method of the Game class.
        
        Verifies that the results can be displayed in wide or narrow.
        Ensures that the output format matches has the right column names and index.
        Also tests that an invalid format raises a ValueError.
        """
        faces = np.array([1, 2, 3, 4, 5, 6])
        die1 = Die(faces)
        die2 = Die(faces)
        game = Game([die1, die2])
        game.play(5)
        results_wide = game.disp_results(form="wide")
        self.assertIsInstance(results_wide, pd.DataFrame)
        self.assertTrue(all(results_wide.index == [1, 2, 3, 4, 5]))
        self.assertListEqual(list(results_wide.columns), ['Die 1', 'Die 2'])
    
        faces = np.array([1, 2, 3, 4, 5, 6])
        die1 = Die(faces)
        die2 = Die(faces)
        game = Game([die1, die2])
        game.play(5)
        results_narrow = game.disp_results(form="narrow")
        self.assertIsInstance(results_narrow, pd.DataFrame)
        self.assertTrue(isinstance(results_narrow.index, pd.MultiIndex))
        self.assertEqual(results_narrow.index.names, ['roll', 'die'])
        self.assertEqual(list(results_narrow.columns), ['outcome'])
    
        faces = np.array([1, 2, 3, 4, 5, 6])
        die1 = Die(faces)
        die2 = Die(faces)
        game = Game([die1, die2])
        game.play(5)
        with self.assertRaises(ValueError):
            game.disp_results(form="not a valid form (not narrow or wide)")




class TestAnalyzer(unittest.TestCase):

    def test_initialize_analyzer(self):
        """
        Tests the initialization of the Analyzer class.
        
        Verifies that the Analyzer object is correctly initialized with a Game object.
        Ensures that a ValueError is raised if a non-Game object is passed to the Analyzer.
        """
        die1 = Die(np.array([1, 2, 3, 4, 5, 6]))
        die2 = Die(np.array([1, 2, 3, 4, 5, 6]))
        game = Game([die1, die2])
        game.play(5)
        
        analyzer = Analyzer(game)
        self.assertIsInstance(analyzer, Analyzer)
        
        with self.assertRaises(ValueError):
            Analyzer("passed value (not a game object)")
            
    def test_n_jackpots(self):
        """
        Tests the n_jackpots method of the Analyzer class.
        
        Verifies that the n_jackpots method returns an integer value representing the number of jackpots
        that occurred during the game and tests the method on sample data.
        """
        die1 = Die(np.array([1, 2, 3, 4, 5, 6]))
        die2 = Die(np.array([1, 2, 3, 4, 5, 6]))
        game = Game([die1, die2])
        game.play(5)
        
        analyzer = Analyzer(game)
        jackpots = analyzer.n_jackpots()
        self.assertIsInstance(jackpots, int)
        
        
        die1 = Die(np.array([1, 2, 3, 4, 5, 6]))
        die2 = Die(np.array([1, 2, 3, 4, 5, 6]))
        game = Game([die1, die2])

        game.results = pd.DataFrame({
            'Die1': [1, 2, 3, 1, 5],
            'Die2': [1, 2, 4, 1, 6]
        })

        expected_jackpots = 3
        analyzer = Analyzer(game)
        jackpots = analyzer.n_jackpots()

        self.assertEqual(jackpots, expected_jackpots)

        
        
    def test_n_faces_per_roll(self):
        """
        Tests the n_faces_per_roll method of the Analyzer class.
        
        Verifies that the n_faces_per_roll method returns a DataFrame with the count of faces rolled for each
        roll. Ensures the values are numeric and that the index is labeled Roll Number and tests the method on sample data.
        """
        die1 = Die(np.array([1, 2, 3, 4, 5, 6]))
        die2 = Die(np.array([1, 2, 3, 4, 5, 6]))
        game = Game([die1, die2])
        game.play(5)
        
        analyzer = Analyzer(game)
        face_counts_df = analyzer.n_faces_per_roll()
        self.assertIsInstance(face_counts_df, pd.DataFrame)
        self.assertEqual(face_counts_df.index.name, "Roll Number")
        
        die1 = Die(np.array([1, 2, 3, 4, 5, 6]))
        die2 = Die(np.array([1, 2, 3, 4, 5, 6]))
        game = Game([die1, die2])
        
        known_results = pd.DataFrame({
            'Die1': [1, 2, 3, 4, 5],
            'Die2': [6, 5, 4, 3, 2]
        })
        game.results = known_results
        
        analyzer = Analyzer(game)
        face_counts_df = analyzer.n_faces_per_roll()
        
        expected_data = {
            1: [1, 0, 0, 0, 0, 1],  
            2: [0, 1, 0, 0, 1, 0],  
            3: [0, 0, 1, 1, 0, 0],  
            4: [0, 0, 1, 1, 0, 0],  
            5: [0, 1, 0, 0, 1, 0]   
        }
        
        expected_df = pd.DataFrame(expected_data).T
        expected_df.index.name = 'Roll Number'
        expected_df.columns = [1, 2, 3, 4, 5, 6]

        pd.testing.assert_frame_equal(face_counts_df, expected_df)
        
        
    def test_n_combinations(self):
        """
        Tests the n_combinations method of the Analyzer class.
        
        Verifies that the n_combinations method returns a DataFrame showing the number of possible combinations
        for each roll and that the Number column is included in the result and tests the method on sample data.
        """
        die1 = Die(np.array([1, 2, 3, 4, 5, 6]))
        die2 = Die(np.array([1, 2, 3, 4, 5, 6]))
        game = Game([die1, die2])
        game.play(5)
        
        analyzer = Analyzer(game)
        combinations_df = analyzer.n_combinations()
        self.assertIsInstance(combinations_df, pd.DataFrame)
        self.assertTrue("Number" in combinations_df.columns)
        
        die1 = Die(np.array([1, 2, 3, 4, 5, 6]))
        die2 = Die(np.array([1, 2, 3, 4, 5, 6]))
        game = Game([die1, die2])
        
        known_results = pd.DataFrame({
            'Die1': [1, 2, 3, 4, 5],
            'Die2': [6, 6, 6, 6, 6]
        })
        game.results = known_results
        
        analyzer = Analyzer(game)
        combinations_df = analyzer.n_combinations()
        
        expected_data = {
            (1, 6): 1,
            (2, 6): 1,
            (3, 6): 1,
            (4, 6): 1,
            (5, 6): 1,
        }
        expected_df = pd.DataFrame.from_dict(expected_data, orient='index', columns=['Number'])
        expected_df.index.name = 'Combination'

        pd.testing.assert_frame_equal(combinations_df, expected_df)
    def test_n_permutations(self):
        """
        Tests the n_permutations method of the Analyzer class.
        
        Verifies that the n_permutations method returns a DataFrame with the number of permutations for each roll and tests the method on sample data.
        """
        die1 = Die(np.array([1, 2, 3, 4, 5, 6]))
        die2 = Die(np.array([1, 2, 3, 4, 5, 6]))
        game = Game([die1, die2])
        known_results = pd.DataFrame({
            'Die1': [1, 2, 1, 2, 1],
            'Die2': [6, 6, 6, 6, 6]
        })
        game.results = known_results
        expected_data = {
            (1, 6): 3,
            (2, 6): 2,
        }
        expected_df = pd.DataFrame.from_dict(expected_data, orient='index', columns=['Count'])
        expected_df.index.name = 'Permutation'
        analyzer = Analyzer(game)
        permutations_df = analyzer.n_permutations()
        pd.testing.assert_frame_equal(permutations_df, expected_df)
if __name__ == '__main__':
    unittest.main(verbosity=3)

