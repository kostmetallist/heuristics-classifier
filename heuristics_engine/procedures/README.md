# Procedures

This catalog comprises base heuristic abstract class and its implementations 
for custom and individual log data processing. One may be puzzled with the 
question why *classes* are stored under `procedures/` catalog. Conceptually, 
in the scope of the underlying theoretical investigation, it was defined that 
heuristic should be interpreted as a mix of criteria and techniques to 
infer log event attributes' assignment to a set of data domains - which is 
referred to as classification, to some extent. Given that, heuristic as a 
mathematical object could be represented in the form of mapping of non-empty 
element from the power set of log message's attributes to the multiple of 
data domains.
