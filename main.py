from transformations import test_transformation
from express_config import print_config
import tests  # check tests.py for example transformations!

# The following will take the first 5 characters and therefore return "someI"
# t = {"type": "takeStart", "inputs": 0, "length": 5}
# test_transformation(t, "someInput")

t = {"type": "identity", "inputs": ["!", 0, ""]}
test_transformation(t, "someInput")
test_transformation(t, "012389492")

print_config(t)
