ifndef VERBOSE
.SILENT:
endif

CC = g++ -std=c++2a

default: run
build: main.o solution.o
	${CC} -o main main.o solution.o
main.o: main.cc
	${CC} -c main.cc
solution.o: solution.cc
	${CC} -c solution.cc
clean:
	rm main.o solution.o main
run: build
	./main
