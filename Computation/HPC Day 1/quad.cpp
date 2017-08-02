#include <iostream>
#include <cmath>

int main()
{
  using namespace std;
  cout << "Enter a: ";
  float a, b, c, root1, root2;
  cin >> a;
  cout << "Enter b: ";
  cin >> b;
  cout << "Enter c: ";
  cin >> c ;
  root1 = (-b + sqrt(b*b - 4*a*c)) / (2*a);
  root2 = (-b - sqrt(b*b - 4*a*c)) / (2*a);
  cout << "Root 1 " << root1 << endl;
  cout << "Root 2 " << root2 << endl;
  return 0;
}
