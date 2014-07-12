__author__ = 'szebenyib'

from collections import OrderedDict
import hashlib
import unittest


class Evo():
    """Basically an OrderedDict of settings for the evolution.
    It helps to manage them together and keep code inside the
    evolution cleaner."""

    def __init__(self, initial_dictionary=None):
        """Creates the OrderedDict. If an initial dictionary is provided
        then it will be created from a dictionary. The valid keys are:
        CXPB, MUTPB, NGEN, N, FREQ_OF_CHECKPOINTS, PATIENCE, SEED
        If one of them is not supplied it will default to zero."""
        self.evo = {'CXPB': 0,  # Crossover probability
                    'MUTPB': 0,  # Mutation probability
                    'NGEN': 0,  # Number of generations to evolve
                    'N': 0,  # Number of individuals in population
                    'FREQ_OF_CHECKPOINTS': 0,  # How often to save
                    'PATIENCE': 0,  # How many generations to wait for improvem.
                    'SEED': 0}  # Randomization setting
        if initial_dictionary:
            for k in initial_dictionary:
                if k in self.evo:
                    self.evo[k] = initial_dictionary[k]
                else:
                    raise Exception("Unknown key: " + str(k))
        self.evo = OrderedDict(sorted(self.evo.items(), key=lambda t: t[0]))
        self.evo_hash = hashlib.md5(str(self.evo)).hexdigest()

    def __str__(self):
        """String representation."""
        return str(self.evo)

    def set(self, key, value):
        """Sets a key to a certain value."""
        if key in self.evo:
            self.evo[key] = value
            self.evo_hash = hashlib.md5(str(self.evo)).hexdigest()
        else:
            raise Exception("Unknown key: " + str(key))

    def get(self, key):
        """Gets a key-value pair from the dictionary."""
        if key in self.evo:
            return self.evo[key]
        else:
            raise Exception("Unknown key: " + str(key))

    def get_hash(self, length=None):
        """Gets the hash of the dictionary that is used to save, load,
        identify the settings for the evolutions. If a length is provided
        then only that many characters will be returned from the hash."""
        if length:
            return self.evo_hash[0:length]
        else:
            return self.evo_hash

    def print_evo(self):
        """Prints the settings from the dictionary."""
        print (" CXPB: \t\t" + str(self.evo['CXPB']) +
               "\t(crossover probability)")
        print (" MUTPB: \t" + str(self.evo['MUTPB']) +
               "\t(mutation probability)")
        print (" NGEN: \t\t" + str(self.evo['NGEN']) +
               "\t(number of generations to evolve)")
        print (" N: \t\t" + str(self.evo['N']) +
               "\t(current generation)")
        print (" FREQ_OF_CHECKPOINTS: \t" +
               str(self.evo['FREQ_OF_CHECKPOINTS']) +
               "\t(save after this many generations)")
        print (" PATIENCE: \t\t\t\t" + str(self.evo['PATIENCE']) +
               "\t(abort after this many identical best fitnesses)")
        print (" SEED: \t\t\t\t\t" + str(self.evo['SEED']) +
               "\t(randomization seed)")

    def get_limitation_rules(self):
        """Creates a limitation function that respects either a
        generation limit to reach, or a patience period (to wait for
        fitness improvement), or both.

        %:returns a tuple of a limitaion function and a string representation
        of what it does"""
        if self.get('NGEN') != 0 and self.get('PATIENCE') != 0:
            msg = ("Mode: Generation and improvement limitations " +
                   "are both active.\n")

            def conditions(generation, last_improvement_at):
                if (generation < self.get('NGEN') + 1) is not True:
                    print ("Reached generation limitation of " +
                           str(self.get('NGEN')) + ".")
                if ((generation - last_improvement_at) <= self.get(
                        'PATIENCE')) is not True:
                    print ("Reached improvement limitation of " +
                           str(self.get('PATIENCE')) + ".")
                return (generation < self.get('NGEN') + 1
                        and (generation - last_improvement_at) <=
                        self.get('PATIENCE'))
        elif self.get('NGEN') != 0:
            msg = "Mode: Only generation limitation is active.\n"

            def conditions(generation, last_improvement_at):
                if (generation < self.get('NGEN') + 1) is not True:
                    print ("Reached generation limitation of " +
                           str(self.get('NGEN')) + ".")
                return generation < self.get('NGEN') + 1
        elif self.get('PATIENCE') != 0:
            msg = "Mode: Only improvement limitation is active.\n"

            def conditions(generation, last_improvement_at):
                if ((generation - last_improvement_at) <= self.get(
                        'PATIENCE')) is not True:
                    print ("Reached improvement limitation of " +
                           str(self.get('PATIENCE')) + ".")
                return (generation - last_improvement_at) <= self.get(
                    'PATIENCE')
        else:
            msg = "Mode: No limitation is active -> please set one.\n"

            def conditions(generation, last_improvement_at):
                return False
        return conditions, msg


class Test(unittest.TestCase):
    def test_1_create_empty(self):
        evoset = Evo()
        self.assertTrue(evoset is not None)

    def test_2_create_with_good_dict(self):
        evoset = Evo({'CXPB': 0.3,
                      'MUTPB': 0.1,
                      'NGEN': 50,
                      'N': 400,
                      'FREQ_OF_CHECKPOINTS': 10,
                      'PATIENCE': 10,
                      'SEED': 64})
        self.assertTrue(evoset is not None)

    def test_3_create_with_bad_dict(self):
        with self.assertRaises(Exception):
            evoset = Evo({'CXP': 0.3})

    def test_4_get_good_key(self):
        evoset = Evo()
        self.assertTrue(evoset.get('CXPB') == 0)

    def test_5_get_bad_key(self):
        evoset = Evo()
        with self.assertRaises(Exception):
            evoset.get('CXP')

    def test_6_set_good_key(self):
        evoset = Evo()
        evoset.set('CXPB', 0.5)
        self.assertTrue(evoset.get('CXPB') == 0.5)

    def test_7_set_bad_key(self):
        evoset = Evo()
        with self.assertRaises(Exception):
            evoset.set('CXP', 0.5)

    def test_8_get_hash_unlimited(self):
        evoset = Evo()
        self.assertEquals(evoset.get_hash(), '4b6fb5316ecce934ead5d99426386602')

    def test_9_get_hash_limited(self):
        evoset = Evo()
        self.assertEquals(evoset.get_hash(8), '4b6fb531')

    def test_10_str_evo(self):
        evoset = Evo()
        self.assertEquals(str(evoset),
                          ("OrderedDict([('CXPB', 0), ('FREQ_OF_CHECKPOINTS'" +
                           ", 0), ('MUTPB', 0), ('N', 0), ('NGEN', 0), ('PATI" +
                           "ENCE', 0), ('SEED', 0)])"))

    def test_11_get_limitation_rules(self):
        evoset = Evo()
        self.assertEquals(evoset.get_limitation_rules()[1],
                          "Mode: No limitation is active -> please set one.\n")
        evoset.set('NGEN', 10)
        evoset.set('PATIENCE', 0)
        self.assertEquals(evoset.get_limitation_rules()[1],
                          "Mode: Only generation limitation is active.\n")
        evoset.set('NGEN', 0)
        evoset.set('PATIENCE', 10)
        self.assertEquals(evoset.get_limitation_rules()[1],
                          "Mode: Only improvement limitation is active.\n")
        evoset.set('NGEN', 10)
        evoset.set('PATIENCE', 10)
        self.assertEquals(evoset.get_limitation_rules()[1],
                          ("Mode: Generation and improvement limitations " +
                          "are both active.\n"))


if __name__ == '__main__':
    unittest.main()