# Caesar Cracker

This little GTK application enables encrypting text with the
Caesar method (shifting a→b, b→ c, ..., z→ a) as well as
decrypting text encrypted with Caesar without knowledge of
the number of shifts. This is done by comparing the
frequency of letters with the common English letter
frequencies and searching for the smallest mean square error
in the difference of frequencies.

# Building and Usage

Clone the repository and open it with GNOME Builder. Then, run or
install. The button "encrypt" shifts the text in the field
by one, "decrypt" tries to reverse the effects. Make sure
the text is long enough for the statistical methods to be
successful.
