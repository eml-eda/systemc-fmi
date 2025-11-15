/***********************************************************************
 * ALU
 ***********************************************************************/
#include "systemc.h"

SC_MODULE(ADDER_INT) {
    sc_in<bool> clk;
    sc_in<int> op1, op2;
    sc_out<int> result;

    void operate();

    SC_CTOR(ADDER_INT) {
        SC_THREAD(operate);
        sensitive << clk.pos();
    }
};