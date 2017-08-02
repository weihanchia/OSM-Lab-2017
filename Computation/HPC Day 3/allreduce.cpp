#include <stdio.h>
#include <mpi.h>


int main (int argc, char *argv[])
{
    int my_rank, size;
    int sum;


    MPI_Init(&argc, &argv);

    MPI_Comm_rank(MPI_COMM_WORLD, &my_rank);

    MPI_Comm_size(MPI_COMM_WORLD, &size);

    printf ("Rank %i:\tSum = %i\n", my_rank, size);

    MPI_Reduce(&size, &sum, 1, MPI_INT, MPI_SUM, 0, MPI_COMM_WORLD);

    if (my_rank ==0){
      printf("Sum of ranks = %i\n", sum);
    }

    MPI_Finalize();
    return 0;
}
