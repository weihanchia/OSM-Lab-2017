#######################################################################

all: BSA.cpp.exec BSApar.cpp.exec

#######################################################################

BSA.cpp.exec : BSA.cpp
	g++ BSA.cpp -fopenmp -o BSA.cpp.exec

BSApar.cpp.exec : BSApar.cpp
	g++ BSApar.cpp -fopenmp -o BSApar.cpp.exec


clean :
	rm -f *.exec
