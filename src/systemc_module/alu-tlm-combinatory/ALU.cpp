#include "Alu.h"
#include <iostream>

Alu::Alu(sc_module_name name)
    : sc_module(name), target_socket("target_socket") {
    target_socket(*this);
}

void Alu::b_transport(tlm::tlm_generic_payload &trans, sc_time &t) {
    if (trans.get_data_length() != sizeof(alu_data_t)) {
        trans.set_response_status(tlm::TLM_GENERIC_ERROR_RESPONSE);
        return;
    }

    alu_data_t *data_ptr = reinterpret_cast<alu_data_t *>(trans.get_data_ptr());

    if (trans.is_write()) {
        switch (data_ptr->opcode) {
        case 0:
            data_ptr->result = data_ptr->op1 + data_ptr->op2;
            break;
        case 1:
            data_ptr->result = data_ptr->op1 - data_ptr->op2;
            break;
        default:
            // Throw an error if the opcode is not supported
            throw std::runtime_error("Unsupported opcode");
        }

        trans.set_response_status(tlm::TLM_OK_RESPONSE);
    } else if (trans.is_read()) {
        std::cout << "  [ALU:] Read command not supported" << std::endl;
        trans.set_response_status(tlm::TLM_GENERIC_ERROR_RESPONSE);
    }
}

// must be implemented to be compliant with the interface
// not used for now - just ignore them

bool Alu::get_direct_mem_ptr(tlm::tlm_generic_payload &trans, tlm::tlm_dmi &dmi_data) {
    trans.set_response_status(tlm::TLM_GENERIC_ERROR_RESPONSE);
    return false;
}

tlm::tlm_sync_enum Alu::nb_transport_fw(tlm::tlm_generic_payload &trans, tlm::tlm_phase &phase, sc_time &t) {
    trans.set_response_status(tlm::TLM_GENERIC_ERROR_RESPONSE);
    return tlm::TLM_COMPLETED;
}

unsigned int Alu::transport_dbg(tlm::tlm_generic_payload &trans) {
    trans.set_response_status(tlm::TLM_GENERIC_ERROR_RESPONSE);
    return 0;
}