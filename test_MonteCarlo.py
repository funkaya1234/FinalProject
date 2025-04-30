import unittest
import numpy as np
import pandas as pd
from MonteCarlo import Die, Game, Analyzer

class TestDie(unittest.TestCase):
    
    def test_initialization(self):
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
        faces = np.array([1, 2, 3, 4, 5, 6])
        die = Die(faces)
        die.adjust_weight(1, 2.0)
        self.assertEqual(die._die.loc[1, 'weight'], 2.0)
        
        faces = np.array([1, 2, 3, 4, 5, 6])
        die = Die(faces)
        with self.assertRaises(IndexError):
            die.adjust_weight(7, 2.0)
    
        faces = np.array([1, 2, 3, 4, 5, 6])
        die = Die(faces)
        with self.assertRaises(TypeError):
            die.adjust_weight(1, "Incorrect weight (not int or float)")
    
    def test_roll_die(self):
        faces = np.array([1, 2, 3, 4, 5, 6])
        die = Die(faces)
        result = die.roll_die(1)
        self.assertIn(result[0], faces)
        results = die.roll_die(10)
        self.assertTrue(all(result in faces for result in results))
    
    def test_show_die(self):
        faces = np.array([1, 2, 3, 4, 5, 6])
        die = Die(faces)
        die_state = die.show_die()
        self.assertIsInstance(die_state, pd.DataFrame)
        self.assertTrue(np.array_equal(die_state.index, faces))
        self.assertTrue(np.array_equal(die_state['weight'], np.ones(len(faces))))

class TestGame(unittest.TestCase):
    
    def test_initialization(self):
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
        faces = np.array([1, 2, 3, 4, 5, 6])
        die1 = Die(faces)
        die2 = Die(faces)
        game = Game([die1, die2])
        game.play(5)
        self.assertIsInstance(game.results, pd.DataFrame)
        self.assertEqual(len(game.results), 5)
    
    def test_disp_results(self):
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
        # Initialize the analyzer within this test
        die1 = Die(np.array([1, 2, 3, 4, 5, 6]))
        die2 = Die(np.array([1, 2, 3, 4, 5, 6]))
        game = Game([die1, die2])
        game.play(5)
        
        analyzer = Analyzer(game)
        
        self.assertIsInstance(analyzer, Analyzer)  
        self.assertIsNotNone(analyzer.game) 

    def test_n_jackpots(self):
        die1 = Die(np.array([1, 2, 3, 4, 5, 6]))
        die2 = Die(np.array([1, 2, 3, 4, 5, 6]))
        game = Game([die1, die2])
        game.play(5)
        analyzer = Analyzer(game)
        
        jackpots = analyzer.n_jackpots()
        self.assertIsInstance(jackpots, int)

    def test_n_faces_per_roll(self):
        die1 = Die(np.array([1, 2, 3, 4, 5, 6]))
        die2 = Die(np.array([1, 2, 3, 4, 5, 6]))
        game = Game([die1, die2])
        game.play(5)
        analyzer = Analyzer(game)
        
        face_counts_df = analyzer.n_faces_per_roll()
        self.assertIsInstance(face_counts_df, pd.DataFrame)
        self.assertEqual(face_counts_df.index.name, "Roll Number")
        self.assertTrue(all(isinstance(val, (int, float)) for val in face_counts_df.values.flatten()))

    def test_n_combinations(self):
        die1 = Die(np.array([1, 2, 3, 4, 5, 6]))
        die2 = Die(np.array([1, 2, 3, 4, 5, 6]))
        game = Game([die1, die2])
        game.play(5)
        analyzer = Analyzer(game)
        
        combinations_df = analyzer.n_combinations()
        self.assertIsInstance(combinations_df, pd.DataFrame)
        self.assertTrue("Number" in combinations_df.columns)

    def test_n_permutations(self):
        die1 = Die(np.array([1, 2, 3, 4, 5, 6]))
        die2 = Die(np.array([1, 2, 3, 4, 5, 6]))
        game = Game([die1, die2])
        game.play(5)
        analyzer = Analyzer(game)
        
        permutations_df = analyzer.n_permutations()
        self.assertIsInstance(permutations_df, pd.DataFrame)

if __name__ == '__main__':
    unittest.main(verbosity=3)

