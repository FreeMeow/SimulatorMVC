from model.utils.constants import CONSTANTS

def time_function(t): # target function (Check 'target function' in documentation for more details)
  if t < 0:
    return 0
  else:
    return (t ** CONSTANTS['B'])

def price(t, p): # target function (Check 'target function' in documentation for more details)
  return p * time_function(t)

