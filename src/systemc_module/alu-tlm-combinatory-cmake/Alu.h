#ifndef __ALU_H__
#define __ALU_H__

#include "payload.h"
#include <systemc.h>
#include <tlm.h>

class Alu
    : public sc_module,
      public virtual tlm::tlm_fw_transport_if<> {
  private:
    alu_data_t data;

  public:
    tlm::tlm_target_socket<> target_socket;

    virtual void b_transport(tlm::tlm_generic_payload &trans, sc_time &t);

    virtual bool get_direct_mem_ptr(tlm::tlm_generic_payload &trans, tlm::tlm_dmi &dmi_data);
    virtual tlm::tlm_sync_enum nb_transport_fw(tlm::tlm_generic_payload &trans, tlm::tlm_phase &phase, sc_time &t);
    virtual unsigned int transport_dbg(tlm::tlm_generic_payload &trans);

    SC_HAS_PROCESS(Alu);
    Alu(sc_module_name name);
};

#endif
