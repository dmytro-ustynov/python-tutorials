MORSE = {
    ".-": "a",
    "-...": "b",
    "-.-.": "c",
    "-..": "d",
    ".": "e",
    "..-.": "f",
    "--.": "g",
    "....": "h",
    "..": "i",
    ".---": "j",
    "-.-": "k",
    ".-..": "l",
    "--": "m",
    "-.": "n",
    "---": "o",
    ".--.": "p",
    "--.-": "q",
    ".-.": "r",
    "...": "s",
    "-": "t",
    "..-": "u",
    "...-": "v",
    ".--": "w",
    "-..-": "x",
    "-.--": "y",
    "--..": "z",
    "-----": "0",
    ".----": "1",
    "..---": "2",
    "...--": "3",
    "....-": "4",
    ".....": "5",
    "-....": "6",
    "--...": "7",
    "---..": "8",
    "----.": "9",

}

MORSE_REVERSE = {v: k for k, v in MORSE.items()}

def encode_morse(text):
    """
    Return encoded with morse text, where "." is morse dot and "-" is morse dash, and
    each character is separated with space.
    Double space -  is for space between words.
    :param text: text to encode
    :return: morse sequence, e.g "SOS" --> "... --- ..."
    """
    seq = []
    for letter in text:
        seq.append(MORSE_REVERSE.get(letter.lower(), ' '))
    return ''.join(seq)

def decode_morse(sequence):
    """
    Decode valid morse sequence of dots and dashes to readable text
    Example: "... --- ..." --> "sos"
    :param sequence:  valid morse sequence to decode
    :type sequence: str
    :return: decoded text
    :type: str
    """
    text = ''
    try:
        for morse_letter in sequence.split(' '):
            decoded = MORSE.get(morse_letter, ' ')
            text += decoded
    except KeyError:
        print('Invalid morse sequence')
    return text



if __name__ == '__main__':
    print(encode_morse("SOS"))

    print(encode_morse("Hello Morse!"))

    print(decode_morse('--. --- --- -..  . ...- . -. .. -. --.  .-- .  .- .-. .  ..-. '
                       '.-. --- --  ..- -.- .-. .- .. -. .'))
    print(decode_morse('.-. ..- ... ... .. .- -.  .-- .- .-. ... .... .. .--.  --. '
                       '---  ....- -.-. -.-  -.-- --- ..- .-. ... . .-.. ..-.'))
    print(decode_morse('..  .- --  - .... .  -... . ... -  .--. -.-- - .... --- -.  '
                       '-.. . ...- . .-.. --- .--. . .-.  . ...- . .-. '))
    print(decode_morse('-.-. --- -.. .. -. --.  .- -. -..  -.. . -.-. --- -.. '
                       '.. -. --.  -- --- .-. ... .  -.-. --- -.. .  .. ...  .- .-- . ... --- -- .'))
