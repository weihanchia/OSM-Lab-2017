#include <stdio.h>
#include <stdlib.h>
#include <math.h>
#include <iostream>
#include <omp.h>
#include <random>

using namespace std;
int main()
{
    int niter = 10000000;
    double x,y;
    int i;
    int count=0;
    double z;
    double pi;
    //srand(time(NULL));
    //main loop
    double time = -omp_get_wtime();

    #pragma omp parallel private(x,y,z) shared(count)
    {
      unsigned seed_unif1 = omp_get_thread_num();
    	std::default_random_engine generator_unif(seed_unif1);
    	std::uniform_real_distribution<double> distribution_unif(0.0,1.0);

      #pragma omp for reduction (+: count)
      for (i=0; i<niter; ++i) {
          //get random points
        x = (double)distribution_unif(generator_unif);
        y = (double)distribution_unif(generator_unif);
        z = sqrt((x*x)+(y*y));
        //check to see if point is in unit circle
        count += (z <= 1);
    }
  }

    pi = ((double)count/(double)niter)*4.0;          //p = 4(m/n)
    //printf("Pi: %f\n", pi);
    time += omp_get_wtime();
    cout << niter
               << " iterations approximates pi as : "
               << pi
               << std::endl;
    cout << "the solution took " << time << " seconds" <<endl;
  return 0;
}
