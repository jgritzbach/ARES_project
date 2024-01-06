The ARES_project enables you to retrieve data about economic subjects in the Czech Republic from a state public register called "ARES".

In the Czech Republic, each company is assigned a unique eight-digit ID number on its registration. This ID number is called "IČO" and it serves as a primary identification that can be used to track the company in the ARES register.

The main idea of this project is to retrieve the full business name and official address of a company (or other registered subject) with just a unique ID number known. 

The core function of this project takes an ID number as a parameter and performs a request to the ARES register. If the subject is successfully found by the ID number, the function returns the whole description of the company.

For example, if you pass 00001350 to the function, it returns:
"Československá obchodní banka, a. s., IČO 00001350, sídlem Radlická 333/150, Radlice, 15000 Praha 5"

This is useful especially when the law or your internal regulations require you to write a full description of the subject. This happens a lot in formal communication, in court decisions, or when filing a lawsuit.

Since the core function simply returns the full name, ID number, and address as a string, its usage is quite universal. You can simply write the output to the console. 

If you write some more code (and I might write this code later on myself), you may use the ARES core function to perform subsequent operations such as filling the result in your text editor after you enter just the ID number.

It can also be used to check whether the company's name and address is still valid in your database. Perhaps you have a list of companies that you maintain contact with. As long as you store their unique ID numbers somewhere, you can use the core function of this project to check, whether your contact information is not out of date.
