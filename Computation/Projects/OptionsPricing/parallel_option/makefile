#######################################################################

all: BSpar.cpp.exec BSApar.cpp.exec

#######################################################################

BSpar.cpp.exec : BSpar.cpp
	g++ BSpar.cpp -fopenmp -o BSpar.cpp.exec

BSApar.cpp.exec : BSApar.cpp
		g++ BSApar.cpp -fopenmp -o BSApar.cpp.exec

clean :
	rm -f *.exec
