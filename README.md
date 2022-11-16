# Ramen
## What is Ramen?
Ramen is a stupid language that I create to prove that I'm not very stupid at programming. This programming language compiler is created using Python and running in NekoVM. It's kinda stupid that I'm using nekoVM while I can target the Python itself. Well I could actually do It in less than 1 hour by just adding an API for the AST. But nah, since I want to self-host Ramen in NekoVM in the future (and It's just cute NekoRamen LOL).

## Version
Current Version is 1.0 which this version is just for showoff. The real release version will be the 2.0 where I have done all the TODO list below

## Installing
The Ramen Language is actually supporting all platform that NekoVM support just download the latest version of NekoVM and you will need Python

## How To Use
Since I am not building the python into executable yet You will need to run the compiler using python.
- To Build a program: **python ramen.py compile [filename]**
- To Run a program: **python ramen.py run [filename]**

## TODO
- Add Indexing features for HashMap
	To get a value from a hashmap currently you can't use something like **identifier[key]** but you should do it using the API which is **get(identifier, key)** or **set(identifier, key, value)**

- Repair the bundling features
	My design for the language is that there's no import or include or the other kind keyword for modularity. Instead we bundle your code in the compiler so you will need to tell the compiler which code to be bundled before compiling it.

- Fix some small threat in the AST
	I found some small threat in the AST but I think it's not a big problem for now because I just want to show off this programming language

- Make the package/namespace system works
	There will be a namespacing system in Ramen. The syntax is **pack identifier { // the body // }**. 
	You can actually write It and will not get any error but It's currently has no impact on your program

- Create an installer to setup the Ramen
	I will created soon but you will need python to run the setup.py. The installer should also build the NekoVM and build the compiler into executable

- Add another standard library like http, graphics, etc

- Create a better Compiler Error
	This is actually the most frustating feature to be added for the compiler. Some common error that you will found

- Self Host Ramen
	Write Ramen Compiler with Ramen itself :)