#include <stdio.h>
#include <stdlib.h>
#include <math.h>
#include <iostream>
#include <omp.h>

using namespace std;
int main(void)
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

    for (i=0; i<niter; ++i) {
        //get random points
        x = (double)random()/RAND_MAX;
        y = (double)random()/RAND_MAX;
        z = sqrt((x*x)+(y*y));
        //check to see if point is in unit circle
        count += (z <= 1);
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
