from transformations import apply_transformation
import pytest

assert apply_transformation(0, "hallo") == "hallo"
assert apply_transformation([0], "hallo") == "hallo"
assert apply_transformation(["abc", 0, "xyz"], "hallo") == "abchalloxyz"

# https://scandit.atlassian.net/wiki/spaces/DC/pages/5466619905/Regex+Transformation
# The following will return the input if it is 13 characters long.
t = {"type": "regex", "inputs": 0, "regex": ".{13}", "output": 0}
assert apply_transformation(t, "1234567890123") == "1234567890123"
assert apply_transformation(t, "12345678901234") == "1234567890123"
with pytest.raises(ValueError):
  apply_transformation(t, "123456789012")

# This example would concatenate the dynamic inputs 0 and 1 and check that they are 13 characters long and return them.
t = {"type": "regex", "inputs": [0, 1], "regex": ".{13}", "output": 0}
assert apply_transformation(t, ["123456789", "01234"]) == "1234567890123"

# Instead of returning the entire match, we can return just a capture group, for example just the first 3 characters.
t = {"type": "regex", "inputs": [0, 1], "regex": "(.{3}).{10}", "output": 1}
assert apply_transformation(t, ["123456789", "01234"]) == "123"

# https://scandit.atlassian.net/wiki/spaces/DC/pages/5466619912/Take+Transformation

# The following will take the first 5 characters and therefore return "someI"
t = {"type": "takeStart", "inputs": "someInput", "length": 5}
assert apply_transformation(t, "") == "someI"

# We can also take characters instead, so if we take all the characters inside "mostu" we will get "som" for a takeStart
t = {"type": "takeStart", "inputs": "someInput", "characters": "mostu"}
assert apply_transformation(t, "") == "som"

# For a take at the end we will get "ut".
t = {"type": "takeEnd", "inputs": "someInput", "characters": "mostu"}
assert apply_transformation(t, "") == "ut"

#https://scandit.atlassian.net/wiki/spaces/DC/pages/5466619914/Pad+Transformation
# The following will pad the input by zeros to reach a length of 12, the result is therefore "000someInput"

t = {"type": "padStart", "inputs": "someInput", "length": 12, "padding": "0"}
assert apply_transformation(t, "") == "000someInput"

# If the padding is longer than 1 it will simply repeat until it reaches a length of 12, the result here would be "010someInput"

t = {"type": "padStart", "inputs": "someInput", "length": 12, "padding": "01"}
assert apply_transformation(t, "") == "010someInput"

# Additional for someInput000
t = {"type": "padEnd", "inputs": "someInput", "length": 12, "padding": "0"}
assert apply_transformation(t, "") == "someInput000"

# Additional for someInput010
t = {"type": "padEnd", "inputs": "someInput", "length": 12, "padding": "01"}
assert apply_transformation(t, "") == "someInput010"

#https://scandit.atlassian.net/wiki/spaces/DC/pages/5466619907/Validation+Transformation
t = {"type": "validation", "inputs": 0, "regex": ".{13}"}
assert apply_transformation(t, "1234567890123") == ""
with pytest.raises(ValueError):
  apply_transformation(t, "123456789012")
# Question: Should this match as full match?
