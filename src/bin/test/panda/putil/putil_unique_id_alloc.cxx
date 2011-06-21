
#include <iostream>
#include <map>
#include <cassert>
using namespace std;

#include "uniqueIdAllocator.h"


int main(int argc, char** argv) {
        cout <<"UniqueIdAllocator Test"<<endl;
        UniqueIdAllocator b=UniqueIdAllocator(2, 9);
        b.output(cout);
        b.allocate(); b.output(cout);
        b.allocate(); b.output(cout);
        b.allocate(); b.output(cout);
        b.allocate(); b.output(cout);
        b.allocate(); b.output(cout);
        b.allocate(); b.output(cout);
        b.free(2); b.output(cout);
        b.free(3); b.output(cout);
        b.free(4); b.output(cout);
        b.free(5); b.output(cout);
        b.allocate(); b.output(cout);
        b.allocate(); b.output(cout);
        b.allocate(); b.output(cout);
        b.free(3); b.output(cout);
        b.free(2); b.output(cout);

        b.allocate(); b.output(cout);
        b.allocate(); b.output(cout);
        b.allocate(); b.output(cout);
        b.allocate(); b.output(cout);
        b.allocate(); b.output(cout);
        b.allocate(); b.output(cout);
        b.allocate(); b.output(cout);

        b.free(4); b.output(cout);
        b.free(3); b.output(cout);

        b.allocate(); b.output(cout);

        return 0;
}
