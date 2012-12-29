=========
Supa Dupa
=========

WARNING: THIS IS NOT QUITE YET ALPHA. DANGEROUS TO ALL.

Supa Dupa is a class generation system written in python. It allows you to use wrapped json data to generate source code for classes based on the json data. So if you have json data like:

``{"count" : 1, "name" : "party time"}``

you can wrap it with a root key that is the class name like:

``{"PartyCounter" : {"count" : 1, "name" : "party time"}}``

You can pass this new json object to Supa Dupa, which will generate a class named PartyCounter with the included fields (with appropriate types, if needed).

Status
======

Currently, Supa Dupa only supports Objective-C as an output languages. I'll probably add java or something soon after. If you have somehow stumbled upon this project and want to add a language, follow the Objective-C example.

License
=======

Apache 2.0
