/***********************************************************************
 * ALU
 ***********************************************************************/
#include "systemc.h"

SC_MODULE(ADDER_DOUBLE) {
    sc_in<bool> clk;
    sc_in<double> op1, op2;
    sc_out<double> result;

    void operate();

    SC_CTOR(ADDER_DOUBLE) {
        SC_THREAD(operate);
        sensitive << clk.pos();
    }
};