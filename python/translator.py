import sys

# Mapping of the alphabet and numbers to Braille. 
# 'O' represents a raised dot and '.' represents no dot.
braille_alphabet = {
    'a': 'O.....', 'b': 'O.O...', 'c': 'OO....', 'd': 'OO.O..', 'e': 'O..O..', 'f': 'OOO...',
    'g': 'OOOO..', 'h': 'O.OO..', 'i': '.OO...', 'j': '.OOO..', 'k': 'O...O.', 'l': 'O.O.O.',
    'm': 'OO..O.', 'n': 'OO.OO.', 'o': 'O..OO.', 'p': 'OOO.O.', 'q': 'OOOOO.', 'r': 'O.OOO.',
    's': '.OO.O.', 't': '.OOOO.', 'u': 'O...OO', 'v': 'O.O.OO', 'w': '.OOO.O', 'x': 'OO..OO',
    'y': 'OO.OOO', 'z': 'O..OOO', ' ': '......'  # Handle spaces
}

# Special symbols for capitalization and numbers in Braille
braille_capital = '.....O'  # This indicates the next letter is capitalized
braille_number = '.O.OOO'   # This indicates a shift to number mode
braille_numbers = {
    '0': '.OOO..', '1': 'O.....', '2': 'O.O...', '3': 'OO....', '4': 'OO.O..', '5': 'O..O..',
    '6': 'OOO...', '7': 'OOOO..', '8': 'O.OO..', '9': '.OO...'
}

# Reverse dictionaries for decoding Braille back to English
english_alphabet = {v: k for k, v in braille_alphabet.items()}
english_numbers = {v: k for k, v in braille_numbers.items()}

# Determine if the input is Braille (only contains 'O' and '.')
def is_braille(input_string):
    return all(c in ['O', '.'] for c in input_string)

# Convert English to Braille
def translate_to_braille(input_string):
    result = []
    number_mode = False  # Tracks if we are in number mode

    for char in input_string:
        if char.isdigit() and not number_mode:
            result.append(braille_number)  # Start number mode
            number_mode = True
        elif char.isalpha() and number_mode:
            number_mode = False  # Exit number mode when a letter is found
        
        if char.isupper():
            result.append(braille_capital)  # Add capital symbol before uppercase letters
            result.append(braille_alphabet[char.lower()])
        elif char.isdigit():
            result.append(braille_numbers[char])  # Convert digit to Braille
        else:
            result.append(braille_alphabet[char])  # Convert letter or space to Braille

    return ''.join(result)  # Return the Braille translation

# Convert Braille to English
def translate_to_english(braille_string):
    result = []
    i = 0
    capital_mode = False  # Tracks if the next letter should be capitalized
    number_mode = False   # Tracks if we are in number mode

    # Iterate through the Braille string 6 characters at a time (one Braille symbol)
    while i < len(braille_string):
        symbol = braille_string[i:i+6]  # Take 6-character chunks
        
        # Check for special Braille symbols
        if symbol == braille_capital:
            capital_mode = True
            i += 6
            continue
        elif symbol == braille_number:
            number_mode = True
            i += 6
            continue
        
        # Handle numbers if we're in number mode
        if number_mode:
            result.append(english_numbers[symbol])
            # Exit number mode when a space is found
            if braille_string[i + 6:i + 12] == '......':
                number_mode = False
        # Handle letters, considering capitalization if needed
        elif capital_mode:
            result.append(english_alphabet[symbol].upper())
            capital_mode = False  # Reset capital mode after using it once
        else:
            result.append(english_alphabet[symbol])  # Add regular lowercase letters

        i += 6  # Move to the next Braille character

    return ''.join(result)  # Return the English translation

# Main function that figures out if the input is Braille or English and calls the right translator
def braille_translator(input_string):
    if is_braille(input_string):
        return translate_to_english(input_string)  # Braille to English
    else:
        return translate_to_braille(input_string)  # English to Braille

# Entry point for the script; takes input from the command line
if __name__ == "__main__":
    if len(sys.argv) > 1:
        input_string = sys.argv[1]  # Grab the input passed to the program
        output = braille_translator(input_string)
        print(output)  # Print only the translated result
    else:
        print("Please provide a string to translate.")  # Error if no input provided
