def calibration_value_part_one(line):
    """The solution for the first part is a two-line function."""
    digits = list(filter(str.isdigit, line))
    return int(f"{digits[0]}{digits[-1]}")


# the solution for the second part is a bit more fiddly

digit_names = {
    1: "one",
    2: "two",
    3: "three",
    4: "four",
    5: "five",
    6: "six",
    7: "seven",
    8: "eight",
    9: "nine",
}


def digit_name_starting(string):
    for digit, name in digit_names.items():
        if string.startswith(name):
            return digit, name
    return None, None


def test_digit_name_in_string():
    assert digit_name_starting("one") == (1, "one")
    assert digit_name_starting("twoone") == (2, "two")
    assert digit_name_starting("nintwo2one") == (None, None)


class Decoder:
    def __init__(self, line):
        self.index = 0
        self.line = line

    def __iter__(self):
        return self

    def __next__(self):
        while self.index < len(self.line):
            # if it's a digit, return it
            character = self.line[self.index]
            if character.isdigit():
                self.index += 1
                return int(character)

            # if there's a digit name in the rest of the string, return the digit
            digit, named = digit_name_starting(self.line[self.index :])
            if named:
                self.index += 1  # len(named)
                return digit

            # else keep going
            self.index += 1

        self.index = 0
        raise StopIteration


def digits_or_names(line):
    return list(Decoder(line))


def test_digits_or_names():
    assert digits_or_names("one") == [1]
    assert digits_or_names("one2three") == [1, 2, 3]


def calibration_value(line):
    digits = digits_or_names(line)
    return int(f"{digits[0]}{digits[-1]}")


with open("2023/1/input.txt") as fi:
    answer = sum([calibration_value(line) for line in fi])
    print(answer)
