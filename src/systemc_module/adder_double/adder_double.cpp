#include "adder_double.h"

void ADDER_DOUBLE::operate() {    
    while (true) {
        wait();
        result.write(op1.read() + op2.read());
    }
}