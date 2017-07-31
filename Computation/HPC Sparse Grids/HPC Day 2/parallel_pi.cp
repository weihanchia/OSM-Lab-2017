#include <stdio.h>
#include <stdlib.h>
#include <math.h>

void main()
{
    double niter = 10000000;
    double x,y;
    int i;
    int count=0;
    double z;
    double pi;
    //srand(time(NULL));
    double time = -omp_get_wtime();
    //main loop

    #pragma omp parallel private(x, y, z)
    {
      #pragma omp parallel for reduction(+:count)
      for (i=0; i<niter; ++i)
      {
        //get random points
        x = (double)random()/RAND_MAX;
        y = (double)random()/RAND_MAX;
        z = sqrt((x*x)+(y*y));
        count += (z <= 1)
      }
    }
    time += omp_get_wtime();

    pi = ((double)count/(double)niter)*4.0;          //p = 4(m/n)
    //printf("Pi: %f\n", pi);
    std::cout << niter
              << " iterations approximates pi as : "
              << pi
              << std::endl;
    std::cout << "the solution took " << time << " seconds" <<std::endl;
}
