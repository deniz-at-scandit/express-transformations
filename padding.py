import math


def lrpad(s, left, width, fill):
  if width <= len(s):
    return s

  d = width - len(s)
  x = math.ceil(d / len(fill))
  filling = (x * fill)[:d]

  if left:
    return filling + s
  else:
    return s + filling


def lpad(s, width, fill):
  return lrpad(s, True, width, fill)


def rpad(s, width, fill):
  return lrpad(s, False, width, fill)


assert lpad("someInput", 12, "0") == "000someInput"
assert lpad("someInput", 12, "01") == "010someInput"
assert rpad("someInput", 12, "0") == "someInput000"
assert rpad("someInput", 12, "01") == "someInput010"
