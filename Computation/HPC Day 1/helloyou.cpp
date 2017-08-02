#include <iostream>
int main()
{
  using namespace std;
  cout << "Enter your Name : ";
  string yourname;
  getline(cin, yourname);
  cout << "Hello " << yourname << " how are you?\n";
  return 0;
}
