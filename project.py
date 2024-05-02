#Authors: Shakeb Siddiqui and Rukshang Verma
import itertools #need for testing

class Automaton:
    def __init__(self, filename):
        self.states = {}
        self.start_state = None
        self.accept_states = set()
        self.alphabet = set()  # Initialize an empty set to store the alphabet
        self.load_from_file(filename)

    def load_from_file(self, filename):
        with open(filename, 'r') as file:
            alphabet = file.readline().strip()
            self.alphabet = set(alphabet)  # Store the alphabet
            num_states = int(file.readline().strip())
            for _ in range(num_states):
                state_name = file.readline().strip()
                self.states[state_name] = {}
            self.start_state = file.readline().strip()
            num_accept_states = int(file.readline().strip())
            for _ in range(num_accept_states):
                self.accept_states.add(file.readline().strip())
            num_transitions = int(file.readline().strip())
            for _ in range(num_transitions):
                transition = file.readline().strip().split(',')
                p, q, l = transition[0], transition[1], transition[2]
                if l not in self.states[p]:
                    self.states[p][l] = []
                self.states[p][l].append(q)

    def epsilon_closure(self, states):
        stack = list(states)
        closure = set(states)
        while stack:
            state = stack.pop()
            if 'EPSILON' in self.states[state]:
                for next_state in self.states[state]['EPSILON']:
                    if next_state not in closure:
                        closure.add(next_state)
                        stack.append(next_state)
        return closure

    def transition(self, state, symbol):
        if symbol in self.states[state]:
            return set(self.states[state][symbol])
        return set()

    def process_string_dfa(self, input_string):
        current_state = self.start_state
        for symbol in input_string:
            transitions = self.states[current_state]
            if symbol in transitions:
                current_state = transitions[symbol][0]
            else:
                return False
        return current_state in self.accept_states

    def process_string_nfa(self, input_string):
        current_states = self.epsilon_closure({self.start_state})
        for symbol in input_string:
            next_states = set()
            for state in current_states:
                next_states.update(self.transition(state, symbol))
            current_states = self.epsilon_closure(next_states)
        return any(state in self.accept_states for state in current_states)


def find_first_accepted_string(dfa_file, inputs_file):
    automaton = Automaton(dfa_file) 
    with open(inputs_file, 'r') as file: 
        for line in file:  
            input_string = line.strip()  
            if automaton.process_string_dfa(input_string): 
                return input_string 
    return None  # Return None if no accepted string is found

def generate_strings(length, alphabet):
    return [''.join(p) for p in itertools.product(alphabet, repeat=length)]


def test_dfalarge(): #for Advanced Quiz
    automaton = Automaton('dfalarge.txt')
    test_inputs = [
        "1111111111000000",
        "111111111111111111110000",
        "111111111100000000",
        "11111111111111111111000000000000",
        "0000000000000000",
        "00000000000000000000111111",
        "11111111111111111111000000",
        "00000000000000000000111111111111",
        "11111111111111111111111111111111",
        "111111000000"
    ]

    for input_str in test_inputs:
        is_accepted = automaton.process_string_dfa(input_str)
        print(f"Input: {input_str} - Accepted: {is_accepted}")

def test_nfalarge():
    automaton = Automaton('nfalarge.txt')
    test_inputs = [
        "11111000000",
        "1111000",
        "111100022222",
        "11110000000",
        "1111100",
        "1111000000",
        "111110",
        "1000",
        "111122222",
        "111000000",
        "11111000",
        "00022222"
    ]

    for input_str in test_inputs:
        is_accepted = automaton.process_string_nfa(input_str)
        print(f"Input: {input_str} - Accepted: {is_accepted}")


if __name__ == "__main__":

    #for advanced quiz
    #test_dfalarge()
    #test_nfalarge()
    
    # nfa_description_file = 'nfabr.txt'  
    # automaton = Automaton(nfa_description_file)  # Initialize automaton with the NFA description
    # test_strings = ["a", "b", "c", "dc", "d", "ab"]
    # accepted_count = 0

    # for s in test_strings:
    #     if automaton.process_string_nfa(s):
    #         accepted_count += 1
    #         print(f"String '{s}' is accepted.")
    #     else:
    #         print(f"String '{s}' is rejected.")

    # print(f"Total accepted strings: {accepted_count}")
    # print()


    # print(f"Total accepted strings: {accepted_count}")
    # nfa_description_file = 'nfadesc.txt'  
    # automaton = Automaton(nfa_description_file)  
    #test_string = "aabbbbbb"
    # # Test the string "aabaabaa" with the NFA
    # is_accepted_nfa = automaton.process_string_nfa(test_string)
    # print(f"String '{test_string}' is {'accepted' if is_accepted_nfa else 'rejected'} by the NFA")

    # length = 3
    # strings = generate_strings(length, automaton.alphabet)
    # accepted_count = 0
    # #Finding the first accepted string from inputs.txt

    # #testing below for Beginner Quiz

    # input_strings_file = 'inputs.txt'
    # first_accepted_string = find_first_accepted_string(dfa_description_file, input_strings_file)
    # if first_accepted_string:
    #     print(f"The first accepted string is: {first_accepted_string}")
    # else:
    #     print("No accepted strings found.")
    
   # Testing strings of specified length (Quiz 1)
    # for s in strings:
    #     if automaton.process_string_nfa(s):  # Should this be DFA or NFA? Assuming DFA as per context.
    #         accepted_count += 1
    #         print(f"String '{s}' is accepted.")
    #     else:
    #         print(f"String '{s}' is rejected.")

    # print(f"Total accepted strings of length {length}: {accepted_count}")
    print()