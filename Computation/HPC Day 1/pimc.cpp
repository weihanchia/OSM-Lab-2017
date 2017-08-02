// #include <iostream>
#include <random>
#include <stdio.h>


//generate random numbers in [0,1]
#include <iostream>
using namespace std;

int main ()
{
  //!.....uniform distributed [0..1]
  	unsigned seed_unif1 = 3;
  	std::default_random_engine generator_unif(seed_unif1);
  	std::uniform_real_distribution<double> distribution_unif(0.0,1.0);

  	int No_random_numbers = 10000;
  	double x, y, pi = 0.0;
    int circle = 0;

    for(int numbers = 1; numbers <=No_random_numbers; numbers++)
  	{
  	  x = distribution_unif(generator_unif);
      y = distribution_unif(generator_unif);
      if (x*x + y*y <= 1) circle ++;
    }
     pi = double(circle)/No_random_numbers*4;

  cout << "Pi from Monte Carlo = " << pi << endl;
  return 0;
}
