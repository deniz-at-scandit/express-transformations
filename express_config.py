import json


def make_config(trafo):
  d = dict(wedge=dict(barcodeTransformations=trafo))
  s = json.dumps(d, indent=4)
  return s


def print_config(trafo):
  s = make_config(trafo)
  print("======== Part of Express Config ========")
  print(s)
  print("======== End of Express Config ========")
