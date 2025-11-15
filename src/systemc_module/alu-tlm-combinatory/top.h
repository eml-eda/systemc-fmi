#ifndef TOP_H
#define TOP_H

#include "payload.h"
#include <systemc>

// Forward declarations
class Initiator;
class Alu;

class Top : public sc_core::sc_module {
  public:
    Top(sc_core::sc_module_name name);
    ~Top();
    alu_data_t send_data(const alu_data_t &data);

  private:
    Initiator *init;
    Alu *alu;
};

#endif