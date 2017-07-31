#######################################################################

all: normalize_vec.exec dot_prod.exec parallel_pi.exec

#######################################################################


## Exercise 1
normalize_vec.exec : normalize_vec.cpp
	g++ normalize_vec.cpp -fopenmp -o normalize_vec.exec

## Exercise 2
dot_prod.exec : dot_prod.cpp
	g++ dot_prod.cpp -fopenmp -o dot_prod.exec

## Exercise 3
parallel_pi.exec : parallel_pi.cpp
	g++ parallel_pi.cpp -fopenmp -o parallel_pi.exec

clean :
	rm -f *.exec
