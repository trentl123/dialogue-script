# Dialogue Script
Python interpreter for an NPC dialogue orientated file format.
------
___Example 1 - Basic dialogue___
```
-- This is a comment
@ JumpPoint 1 -- JumpPoint with an ID of 1
> Dialogue "Hello, nice to meet you." -- Anything marked 'dialogue' will be displayed to the user
> JumpTo 2 "Goodbye" -- Adds an option for the user to type. The number '2' represents the ID of the jump point to move to 
* End -- Required

@ JumpPoint 2 -- Second jump point with an ID of 2
> Dialogue "Goodbye, safe travels!" -- Prints out dialogue to the user
> JumpTo Exit "You too!" -- Instead of a number, 'Exit' is used to 
* End -- Required
```
------
___Example 2 - Advanced dialogue___
```
@ JumpPoint 1
~ Key "greeting" is "Hello there!" -- Creates a variable called 'greeting' and assigns it the value 'Hello there!'
> Dialogue #greeting -- References the variable in the dialogue
~ Wait 1 -- Waits 1 second before continuing
> Dialogue "How are you?"
> JumpTo 2 "Good!"
> JumpTo 3 "Not so good."
~ Key "greeting" isnt -- Using 'isnt' deletes the variable, can also be written as "isn't"
* End

@ JumpPoint 2
> Dialogue "Great!"
> JumpTo Exit "Done"
* End

@ JumpPoint 3
> Dialogue "Sorry to hear that."
> JumpTo Exit "Done"
* End
```
------
___Interpreting your dialogue scripts___
First, start by importing the interpreter module.
```
import dsinterpreter
```
Next, create a new instance of the interpreter object linked to your script's filepath and use 'run' to run it.
```
x = dsinterpreter.DialogueScript('script.ds')
x.run()
```
