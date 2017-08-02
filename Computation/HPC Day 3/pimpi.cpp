#include <stdio.h>
#include <stdlib.h>
#include <math.h>
#include <iostream>
#include <mpi.h>

using namespace std;
int main(int argc, char *argv[])
{
    int i, master = 0;
    int myid, tasks, ierr;
    unsigned int seed = 0;
    MPI_Comm comm;
    MPI_Status status;

    comm = MPI_COMM_WORLD;

    ierr = MPI_Init(&argc,&argv);
    MPI_Comm_rank(comm, &myid);
    MPI_Comm_size(MPI_COMM_WORLD, &tasks);

    int my_value = 1, result = 0;
    double niter = 10000000;
    double pi;
    double x,y,z;
    double iters = niter/tasks;
    seed = myid*iters*2;

    for (i=0; i<iters; ++i) {
        //get random points
      x = (double) rand_r(&seed)/RAND_MAX;
      y = (double) rand_r(&seed)/RAND_MAX;
      seed += 1;
      z = sqrt((x*x)+(y*y));
      //check to see if point is in unit circle
      if (z <= 1) {
        my_value+=1 ;
      }
    }

    printf("Value: %i\n", my_value);
    MPI_Barrier(comm);

    MPI_Reduce(&my_value, &result, 1, MPI_INT, MPI_SUM, 0, comm);

    if (myid==0){
      pi = result*tasks;
      printf("pi = %d\n", pi);
    }

    MPI_Finalize();
}
