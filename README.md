# Refactoring Kata
This is an implementation for Emily Bache's version of the original kata by Terry Hughes.

The original repository [can be found here](https://github.com/emilybache/GildedRose-Refactoring-Kata).

# How to run
You can simply run `test_gilded_rose.py` and `texttest_fixture.py` to see the code in action. 
`texttest_fixture.py` has been configured to run for 30 days with buffer flushing at each print.  
  
For easier before/after comparisons, you can set the logging level in `gilded_rose.py` to DEBUG.

TextTest is no longer run as part of the GitHub Actions, but the output of texttest_fixture.py should be fully conformant (except for first and exit code row).  
  
There was a bug in `stdout.gr` where the behaviour of ConjuredItems wasn't according to spec.  
  
You can find both outputs in the `results` directory (with first and exit rows removed from the output). There is no diff between the two files.
