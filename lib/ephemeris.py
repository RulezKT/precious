#!/usr/bin/env python

# Used to obtain data from the [Swiss Ephemeris](http://www.astro.com/swisseph).<br/>
# More easily invoked with [Eden](http://astrolin.com/to/eden),
# which also offers extra output options.

import sys
import json
import swisseph as swe

# Expects json as the first and only argument, containing instructions about what is needed.

if not sys.argv[1:]:
  print >>sys.stderr, sys.argv[0] + " is useless without input"
  sys.exit(1)
else:
  try:
    re = json.loads(sys.argv[1])
  except ValueError, e:
    print >>sys.stderr, "Could not load JSON object from argv[1]: " + sys.argv[1]
    sys.exit(1)

# Rarely used, pprint is imported only upon such request for output.
# It also substitutes swe.get_planet_name - can be handy on occasion.

if re["out"] == "pprint":
  from pprint import pprint


if __name__ == "__main__":

    # The data files, which may not be in the
    # [sin repo](https://github.com/astrolet/sin) /
    # [gravity pakage](http://search.npmjs.org/#/gravity).
    swe.set_ephe_path(re["data"])

    # This is a minimal e[phemeris].
    e = {"1": {}, "2": {}, "3": {}, "4": {}}

    # Is using the Gregorian calendar flag correct?
    # If calendar type is conditional, is it easier to determine here (with the help of swe)?
    t = swe.utc_to_jd(re["ut"][0],
                      re["ut"][1],
                      re["ut"][2],
                      re["ut"][3],
                      re["ut"][4],
                      re["ut"][5],
                      1 #re["ut"][6]
                      )
    # <!---
    # e["jd-ut1"] = swe.jdut1_to_utc(t[1], 1)
    # --->
    #
    # Ask for what is precious:
    #
    # 1. majors (the main things / points for astrology)
    # 2. minors (other objects - e.g. some "minor planets")
    # 3. angles (ascmc) = 8 of 10 doubles (unused 8 & 9)
    # 4. houses (cusps) = 12 of 13 doubles (unused zero)
    #

    for o in [{"what": "1", "offset": 0}, {"what": "2", "offset": 10000}]:
      for w in re["stuff"][int(o["what"])]:
        result = swe.calc_ut(t[1], (w + o["offset"]))
        output = {}
        for out in re["stuff"][0]:
          output[out] = result[out]
        e[o["what"]][w] = output

    # The angles & houses are possible only if given geo location.
    if re["geo"]["lat"] and re["geo"]["lon"]:
      e["4"], e["3"] = swe.houses(t[1],
                                  float(re["geo"]["lat"]),
                                  float(re["geo"]["lon"]),
                                  str(re["houses"]))

    # Print standard output.
    if re["out"] == "print":
      print(e)
    elif re["out"] == "pprint":
      for (what, offset) in {"1": 0, "2": 10000}.iteritems():
        replace = {}
        for (key, val) in e[what].iteritems():
          replace[str(key) + '-' + swe.get_planet_name(key + offset)] = val
        e[what] = replace
      pprint(e)
    else:
      print json.JSONEncoder().encode(e)

    # Necessary when called from Node / Eden.
    sys.stdout.flush()
