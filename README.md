# THE ARES PROJECT

The ARES project enables you to ***retrieve data about economic subjects in the Czech Republic from a state public register called "ARES"***.<br><br>

It is a custom project crafted by a self-taught developer who also happens to be a senior court officer in the Czech Republic. Feel free to raise any issue about the code quality and suggest improvements!

## Main idea

In the Czech Republic, each company is assigned a unique eight-digit ID number on its registration. This ID number is called ***"IČO"*** and it serves as a primary identification that can be used to track the company in public registers.

The main idea of this project is to be able to retrieve (up to date!) data of economic subjects from ARES register with the IČO alone.

This may come handy for business lawyers, advocates, judges, insolvency administrators, entrepreneurs, accountants and many more people dealing with official company data 

## Usage

The main logic is wrapped into the ***AresApiClient class***, equipped with *get_subject_by_ico()* and *get_subject_formal_description()* methods. You can use this class in other parts of your programs without any user interaction at all.

Then there is the ***AresApiClientManager*** class with its *interact()* method, which serves as an interactive cycle with the user through the CLI, prompting him to enter IČO and receive the subject's full description from ARES register.


**If you run the *ares*.py module directly** by *'python -m ares'* command, you will enter **the interactive mode**.

### AresApiClient.get_subject_by_ico()
**The core method** of *AresApiClient* is the *get_subject_by_ico()* method. **It takes an *IČO* (ID number)** as a parameter and requests the ARES register. If the subject is successfully found by the ID number, **the function returns the subject data** as a dictionary. This includes all the data, like a full name, address, and many more attributes that you may or may not need. 

This alone may be useful to you as a single component for your other programs. Perhaps you have a list of companies that you maintain contact with? You can use this method on a huge data set to check whether your contact information is not out of date. 

Suppose you store your contact data in a database, f.e. In that case, you can use this method to generate a report on subjects with contact information out of date, or even automatically update their data. This of course demands some further coding. I might write some code for this in the future as well!

### AresApiClient.get_subject_formal_description()
Sometimes the Czech laws (or simply common conventions) require proper identification of the subject. Usually, the whole name, IČO and full address are required to identify the subject reliably. This happens a lot in formal communication, in court decisions, or when filing a lawsuit.

 *get_subject_formal_description()* method **takes ico**, retrieves data from ARES **and returns formal description of the subject as it is expected to look like in a formal human written communication**.

For example, if you pass 00001350 to the function, it returns:
"Československá obchodní banka, a. s., IČO 00001350, sídlem Radlická 333/150, Radlice, 15000 Prague 5"

Reliable identification of the subject is an important part of lawsuits or court decisions. Identifying subjects manually can be cumbersome and typo-prone. This method removes that burden and also ensures that the data are up to date.

Since the company name or address can change anytime without you being notified, this is a secure way to be sure that the data are up-to-date. Don't underestimate this as a lawyer! Your whole insolvency petition might be rejected by the court if the subject description is not correct.



## Requirements
Please note that you will need a *python3 interpreter* (see https://www.python.org/). 
The project also relies on the *requests* library. Either install it separately by typing 'pip install requests' (without the quotation marks) into your console, or write 'pip install -r requirements.txt' after you clone the repository to install all required dependencies.
List of requirements may change if additional features are added in the future. See requirements.txt.


## Issues

I hope you will find this project useful! If you don't or if you have trouble using it, please suggest an improvement, either here in issues or via my email jgritzbach@gmail.com