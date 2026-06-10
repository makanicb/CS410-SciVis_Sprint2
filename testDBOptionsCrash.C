#include "DBOptionsAttributes.h"
#include <vector>
#include <string>
#include <iostream>

using namespace std;
int main(int argc, char **argv)
{
	cout << "Creating DBOptionsAttributes" << endl;
	DBOptionsAttributes *opts = new DBOptionsAttributes();	

	// Create enum options
	vector<string> my_strings = {"one", "two", "three"};

	cout << "Calling SetEnumStrings before SetEnum. Crash Expected." << endl;
	//opts->SetEnum("test", 0);
	opts->SetEnumStrings("test", my_strings);

	return 0;

}
