#ifndef _PAYLOAD_H
#define _PAYLOAD_H

#include <systemc.h>

// Port direction enumeration
enum PortDirection {
    PORT_INPUT,
    PORT_OUTPUT
};

// ALU transaction payload
typedef struct {
    int opcode;
    int op1;
    int op2;
    int result;
    
    // Direction information for each field
    PortDirection opcode_dir = PORT_INPUT;
    PortDirection op1_dir = PORT_INPUT;
    PortDirection op2_dir = PORT_INPUT;
    PortDirection result_dir = PORT_OUTPUT;
} alu_data_t;

#endif