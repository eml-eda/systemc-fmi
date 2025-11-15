#include "adder_int.h"

void ADDER_INT::operate() {    
    while (true) {
        wait();
        result.write(op1.read() + op2.read());
    }
}