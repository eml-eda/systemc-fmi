#ifndef _INITIATOR_H
#define _INITIATOR_H

#include "payload.h"
#include <systemc>
#include <tlm>
#include <tlm_utils/simple_initiator_socket.h>

class Initiator : public sc_core::sc_module {
  public:
    tlm_utils::simple_initiator_socket<Initiator> initiator_socket;

    SC_HAS_PROCESS(Initiator);
    Initiator(sc_core::sc_module_name name);

    // Change to return the result instead of modifying the input
    alu_data_t send_data(const alu_data_t &data);
};

#endif