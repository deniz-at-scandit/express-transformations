import re
from padding import lpad, rpad


def test_transformation(t, input):
  output = apply_transformation(t, input)
  print(f"{repr(input)} --trafo--> {repr(output)}")


def resolve_transformation(trafo):
  if type(trafo) == int:
    return {"type": "dynamic", "index": trafo}
  if type(trafo) == list:
    return {"type": "identity", "inputs": trafo}
  if type(trafo) == str:
    return {"type": "static", "value": trafo}
  if trafo["type"] == "takeStart":
    base = {"type": "regex", "inputs": trafo["inputs"], "output": 0}
    if "length" in trafo:
      base["regex"] = ".{" + str(trafo['length']) + "}"
      return base
    if "characters" in trafo:
      base["regex"] = "[" + trafo['characters'] + "]*"
      return base
  if trafo["type"] == "takeEnd":
    base = {"type": "regex", "inputs": trafo["inputs"], "output": 0}
    if "length" in trafo:
      base["regex"] = ".{" + str(trafo['length']) + "}$"
      return base
    if "characters" in trafo:
      base["regex"] = "[" + trafo['characters'] + "]*$"
      return base

  return trafo


def apply_transformation(trafo, s, debug=False):
  trafo = resolve_transformation(trafo)
  if debug:
    print(f"apply_transformation: {trafo} <- {s}")

  if not type(s) == list:
    s = [s]

  def call_subtransformation(subtrafo):
    return apply_transformation(subtrafo, s, debug)

  t = trafo["type"]
  if t == "identity":
    inputs = trafo["inputs"]
    return "".join([call_subtransformation(i) for i in inputs])

  if t == "dynamic":
    index = trafo["index"]
    return s[index]

  if t == "static":
    return trafo["value"]

  if t == "regex":
    input = call_subtransformation(trafo["inputs"])
    regex = trafo["regex"]
    match = re.search(trafo["regex"], input)
    if match is None:
      raise ValueError(f"Regex failed! {input} vs. {regex}")
    else:
      return match[trafo["output"]]

  if t == "validation":
    input = call_subtransformation(trafo["inputs"])
    regex = trafo["regex"]
    match = re.search(regex, input)
    if match is None:
      raise ValueError(f"Validation failed! {input} vs. {regex}")
    else:
      return ""

    return match[trafo["output"]]

  if t == "padStart":
    input = call_subtransformation(trafo["inputs"])
    return lpad(input, trafo["length"], trafo["padding"])

  if t == "padEnd":
    input = call_subtransformation(trafo["inputs"])
    return rpad(input, trafo["length"], trafo["padding"])

  raise ValueError(f"Unknown transformation type '{t}'")
